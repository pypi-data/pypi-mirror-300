from ngsolve import *
try:
    from ngbem import *
except ImportError:
    print("WARNING: ngbem import failed")
import numpy as np
import scipy

def stray_PREP(mesh: Mesh, intorder: int = 12, eps: float = 1e-6) -> dict:
    """
    Produces the matrices required for the `stray_field` function.\n
    Specifically, produces a dictionary for the internal problem,\n
    a dictionary for the projection step,\n
    and a dictionary for the external problem.

    Parameters:
        mesh (Mesh): The `mesh` to be integrated over.
        intorder (int): The integration order to be used in the double layer potential (default `12`)
        eps (float): epsilon parameter used in double layer potential operator compression (default `1e-6`)

    Returns:
        prep (dict): Dictionary containing dictionaries of matrices using keys:\n
        prep = {"internal", "DL", "external"}
        internal = {"A_int", "precon_int"}
        DL = {"DL_pot", "DL_mass"}
        external = {"a_ext", "f_ext", "precon_ext"}
    """
    # build internal dictionary
    V = H1(mesh, order=1)
    N = NumberSpace(mesh)  # used for enforcing zero mean value, constant FE space
    X = V * N
    (u, lam), (v, mu) = X.TnT()
    a = BilinearForm(X)
    a += InnerProduct(Grad(u), Grad(v)) * dx
    a += (u * mu + v * lam) * dx  # enforces zero mean value condition

    with TaskManager():
        a.Assemble()
        rows, cols, vals = a.mat.COO()
        A_int = scipy.sparse.csc_matrix((vals, (rows, cols)))
        M2 = scipy.sparse.linalg.spilu(A_int)  # spilu preconditioner
        M_int = scipy.sparse.linalg.LinearOperator(A_int.shape, M2.solve)
    
    dict_int = {"A_int": A_int,
                "precon_int": M_int}
    # build projection dictionary
    u, v = V.TnT()

    with TaskManager():
        DL_pot = DoubleLayerPotentialOperator(
            V, V, intorder=intorder, method="aca", eps=eps
        )
        DL_mass = BilinearForm(u.Trace() * v.Trace() * ds(bonus_intorder=2)).Assemble()
    
    dict_DL = {"DL_pot": DL_pot,
               "DL_mass": DL_mass}
    # build external dictionary
    fes = H1(mesh, order=1, dirichlet=all_boundaries(mesh))
    with TaskManager():
        u, v = fes.TnT()
        a = BilinearForm(Grad(u) * Grad(v) * dx).Assemble()
        f = LinearForm(fes)
        f.Assemble()
        c = Preconditioner(a, "local")  # <- Jacobi preconditioner
        c.Update()
    dict_ext = {"a_ext": a,
                "f_ext": f,
                "precon_ext": c}
    # put into a dictionary
    dictofdict = {"internal": dict_int,
                  "DL": dict_DL,
                  "external": dict_ext}
    return dictofdict


def stray_field(
    mag_func: GridFunction,
    mesh: Mesh,
    prep: dict,
    check_error: bool = False,
    exacu1: CoefficientFunction = None,
    prev: list = [None, None, None]
) -> CoefficientFunction:
    """
    Computes the stray field of the input `mag_func`, using the current `mesh`.
    Uses the FEMBEM method (see D. Fredkin, T. Koehler, 1990)
    via `NG-Bem`.
    Taken from Algorithm 12, Praetorius 2018 CAMWA (https://doi.org/10.1016/j.camwa.2017.11.028)

    Parameters:
        mag_func (ngsolve.comp.GridFunction): A `VectorH1` `GridFunction`.
        mesh (Mesh): The `mesh` to be integrated over.
        prep (dict): The dictionary of prepared matrices.
        check_error (bool): Displays convergence information, default is `False`.
        exacu1 (CoefficientFunction): The exact solution u1 to the internal problem.
        prev (list): A list containing previously used vector values for functions, `[u1p, gp, u2p]` to be used as initial guesses in the solvers. Defaults to `[None, None, None]`

    Returns:
        strayfield (ngsolve.comp.CoefficentFunction): A `CoefficientFunction` describing the stray field.
    """
    u1_full = compute_internal(mag_func, mesh, prep["internal"], check_error=check_error, exac=exacu1, u1p=prev[0])
    u1 = u1_full.components[0]
    g = DL_boundary_two(u1, mesh, prep["DL"], check_error=check_error, gp=prev[1])
    u2 = compute_external(g, mesh, prep["external"], check_error=check_error, u2p=prev[2])
    strayfield = -Grad(u1) - Grad(u2)
    strayfield = (
        strayfield.Compile()
    )  # compile strayfield into sequence of steps for SPEED!
    newprev = [u1_full.vec.FV().NumPy()[:], g.vec.FV().NumPy()[:], u2.vec.FV().NumPy()[:]]
    print("rizzcler")
    return strayfield, newprev


def compute_internal(
    mag_func: GridFunction,
    mesh: Mesh,
    dict_int: dict,
    order: int = 1,
    check_error: bool = False,
    exac: CoefficientFunction = None,
    u1p: np.ndarray = None
) -> GridFunction:
    """
    Solve internal problem, u_1. Specifically, solves\n
        <∇u_1,∇v> = <m,∇v>,\n where u_1, v satisfy ∫u dx =∫v dx = 0.

    Parameters:
        mag_func (ngsolve.comp.GridFunction): An `H1` grid function.
        mesh (Mesh): The `mesh` to be integrated over.
        order (int): The polynomial order to be used, defaults to 1.
        check_error (bool): Displays convergence information, default is `False`.
        exac (CoefficientFunction): The exact solution for `u1`. Should have nearly zero average.

    Returns:
        u (ngsolve.comp.GridFunction): A `H1` grid function describing the internal potential.
    """
    V = H1(mesh, order=order)
    N = NumberSpace(mesh)  # used for enforcing zero mean value, constant FE space
    X = V * N
    (u, lam), (v, mu) = X.TnT()
    f = LinearForm(X)
    f += mag_func * Grad(v) * dx

    gfu = GridFunction(X)
    with TaskManager():
        A = dict_int["A_int"]
        f.Assemble()
        F = f.vec.FV().NumPy()[:]
        gfu.vec.FV().NumPy()[:], exitCode = scipy.sparse.linalg.gmres(
            A, F, M=dict_int["precon_int"], rtol=1e-13, x0=u1p
        )
    u = gfu.components[0]

    if check_error is True:
        print(f"exitCode = {exitCode}")
        print(f"∫u = {Integrate(u, mesh, VOL)}")
        print(
            f"internal residual = {np.linalg.norm(A.dot(gfu.vec.FV().NumPy()[:]) - F)}"
        )
        if exac is not None:
            integrand = InnerProduct(exac - u, exac - u)
            print(f"||u_1,h - exac|| = {sqrt(Integrate(integrand, mesh, VOL))}")

        integrand = InnerProduct(mag_func - Grad(u), Grad(u))
        print(f"<∇u_1,h - m_h, ∇u_1,h> = {Integrate(integrand, mesh, VOL)}")
        integrand = InnerProduct(mag_func - Grad(u), mag_func - Grad(u))
        print(f"||∇u_1,h - m_h|| = {sqrt(Integrate(integrand, mesh, VOL))}")
    return gfu


def DL_boundary_two(
    pot_int: GridFunction,
    mesh: Mesh,
    dict_DL: dict,
    check_error: bool = False,
    gp: np.ndarray = None
) -> GridFunction:
    """
    Given an `H1` function `u1`, compute an `H1` function `g` such that the trace of `g` is (K-M/2)u1

    Done by solving `Mg = (K - M/2)u1` for `g`, where `u1` is the internal potential.

    Very similar to the NGBem `Dirichlet Laplace Direct Method` tutorial.

    Parameters:
        pot_int (ngsolve.comp.GridFunction): An `H1` grid function.
        mesh (Mesh): The `mesh` to be integrated over.
        check_error (bool): Displays convergence information, default is `False`.

    Returns:
        g (ngsolve.comp.GridFunction): An `H1` grid function describing the internal potential.
    """
    fesH1 = H1(mesh, order=1)
    g = GridFunction(fesH1)

    with TaskManager():
        K = dict_DL["DL_pot"]
        mass = dict_DL["DL_mass"]
        rhs = ((K.mat - 0.5 * mass.mat) * pot_int.vec).Evaluate()

        rows, cols, vals = mass.mat.COO()
        A = scipy.sparse.csc_matrix((vals, (rows, cols)))
        F = rhs.FV().NumPy()[:]
        g.vec.FV().NumPy()[:], exitCode = scipy.sparse.linalg.cg(A, F, rtol=1e-10, x0=gp)
        if check_error is True:
            print(f"exitCode = {exitCode}")
            print(
                f"DL boundary proj, residual = {np.linalg.norm(A.dot(g.vec.FV().NumPy()[:])- F)}"
            )
    return g


def all_boundaries(mesh: Mesh) -> str:
    """
    Fetches all the boundary names for a `mesh`,
    and returns it in regex format used for building Dirichlet FE spaces\n
    i.e. `a|b|c|d|e`
    """
    bound_list = mesh.GetBoundaries()
    word = bound_list[0]
    for i in range(1, len(bound_list)):
        word = word + "|" + bound_list[i]
    return word


def compute_external(
    g: GridFunction,
    mesh: Mesh,
    dict_ext: dict,
    order: int = 1,
    check_error: bool = False,
    u2p: np.ndarray = None
) -> GridFunction:
    """
    Returns the external potential `u_2`
    Parameters:
        g (ngsolve.comp.GridFunction): A `SurfaceL2` grid function.
        mesh (Mesh): The `mesh` to be integrated over.
        order (int): The polynomial order to be used, defaults to 1.
        check_error (bool):  Displays convergence information, default `False`.

    Returns:
        u2 (ngsolve.comp.GridFunction): A `VectorH1` grid function describing the internal potential.

    """
    fes = H1(mesh, order=order, dirichlet=all_boundaries(mesh))
    u2 = GridFunction(fes)
    with TaskManager():
        u2.Set(g, BND)

        solvers.BVP(
            bf=dict_ext["a_ext"], lf=dict_ext["f_ext"], gf=u2, pre=dict_ext["precon_ext"], maxsteps=1000, tol=1e-13, print=check_error
        )
        if check_error is True:
            integrand = InnerProduct(u2 - g, u2 - g)
            print(f"||u_2,h - g||_L²(∂Ω) = {sqrt(Integrate(integrand, mesh, BND))}")

    return u2


def stray_field_L2(
    mag_func: GridFunction,
    mesh: Mesh,
    intorder: int = 12,
    check_error: bool = False,
    exacu1: CoefficientFunction = None,
    eps: float = 0.000001,
) -> CoefficientFunction:
    """
    Computes the stray field of the input `mag_func`, using the current `mesh`.
    Uses the FEMBEM method (see D. Fredkin, T. Koehler, 1990)
    via `NG-Bem`.
    Taken from Algorithm 12, Praetorius 2018 CAMWA (https://doi.org/10.1016/j.camwa.2017.11.028)\n
    Uses discontinuous elements `SurfaceL2` and a lagrange approach for the external potential."""

    u1 = compute_internal_legacy(mag_func, mesh, check_error=check_error, exac=exacu1)
    g = DL_boundary_projection(u1, mesh, order=intorder, check_error=True)
    u2 = compute_external_lag(g, mesh, check_error=check_error)
    strayfield = -Grad(u1) - Grad(u2)
    strayfield = (
        strayfield.Compile()
    )  # compile strayfield into sequence of steps for SPEED!
    return strayfield


def compute_internal_legacy(
    mag_func: GridFunction,
    mesh: Mesh,
    order: int = 1,
    check_error: bool = False,
    exac: CoefficientFunction = None,
) -> GridFunction:
    """
    Solve internal problem, u_1. Specifically, solves\n
        <∇u_1,∇v> = <m,∇v>,\n where u_1, v satisfy ∫u dx =∫v dx = 0.

        Parameters:
        mag_func (ngsolve.comp.GridFunction): A H1 grid function.
        mesh (Mesh): The mesh to be integrated over.
        order (int): The polynomial order to be used, defaults to 1.
        check_error (bool): Displays convergence information, default is `False`.
        exac (CoefficientFunction): The exact solution for u1. Should have nearly zero average.

    Returns:
        u (ngsolve.comp.GridFunction): A H1 grid function describing the internal potential.
    """

    V = H1(mesh, order=order)
    N = NumberSpace(mesh)  # used for enforcing zero mean value, constant FE space
    X = V * N
    (u, lam), (v, mu) = X.TnT()
    a = BilinearForm(X)
    a += InnerProduct(Grad(u), Grad(v)) * dx
    a += (u * mu + v * lam) * dx  # enforces zero mean value condition
    f = LinearForm(X)
    f += mag_func * Grad(v) * dx

    gfu = GridFunction(X)
    with TaskManager():
        a.Assemble()
        f.Assemble()
        rows, cols, vals = a.mat.COO()
        A = scipy.sparse.csc_matrix((vals, (rows, cols)))
        F = f.vec.FV().NumPy()[:]
        M2 = scipy.sparse.linalg.spilu(A)  # spilu preconditioner
        M = scipy.sparse.linalg.LinearOperator((F.size, F.size), M2.solve)
        gfu.vec.FV().NumPy()[:], exitCode = scipy.sparse.linalg.gmres(
            A, F, M=M, rtol=1e-13
        )
    u = gfu.components[0]

    if check_error is True:
        print(f"exitCode = {exitCode}")
        print(f"∫u = {Integrate(u, mesh, VOL)}")
        print(
            f"internal residual = {np.linalg.norm(A.dot(gfu.vec.FV().NumPy()[:]) - F)}"
        )
        if exac is not None:
            integrand = InnerProduct(exac - u, exac - u)
            print(f"||u_1,h - exac|| = {sqrt(Integrate(integrand, mesh, VOL))}")

        integrand = InnerProduct(mag_func - Grad(u), Grad(u))
        print(f"<∇u_1,h - m_h, ∇u_1,h> = {Integrate(integrand, mesh, VOL)}")
        integrand = InnerProduct(mag_func - Grad(u), mag_func - Grad(u))
        print(f"||∇u_1,h - m_h|| = {sqrt(Integrate(integrand, mesh, VOL))}")
    return u


def compute_external_lag(g: GridFunction, mesh: Mesh, order: int = 1, check_error: bool = False) -> GridFunction:
    """
    Compute u2 using a lagrange multiplier to deal\n
    with the boundary condition."""
    V = H1(mesh, order=order)
    Q = H1(mesh, order=order)
    X = V*Q

    with TaskManager():
        u, lam = X.TrialFunction()
        v, mu = X.TestFunction()

        a = BilinearForm(X)
        a += Grad(u)*Grad(v) * dx
        a += (u.Trace()*mu.Trace() + v.Trace()*lam.Trace())*ds

        f = LinearForm(g.Trace()*mu.Trace()*ds)
        a.Assemble()
        f.Assemble()
        gfu = GridFunction(X)
        rows, cols, vals = a.mat.COO()
        A = scipy.sparse.csc_matrix((vals, (rows, cols)))
        F = f.vec.FV().NumPy()[:]
        # print(F)
        # from matplotlib.pyplot import spy, show
        # spy(A)
        # show()
        gfu.vec.FV().NumPy()[:], exitCode = scipy.sparse.linalg.gmres(
            A, F, rtol=1e-13
        )
    
    u2 = gfu.components[0]
    if check_error is True:
            integrand = InnerProduct(u2 - g, u2 - g)
            print(f"||u_2,h - g||_L²(∂Ω) = {sqrt(Integrate(integrand, mesh, BND))}")
    return u2


def DL_boundary_projection(
    pot_int: GridFunction, mesh: Mesh, order: int, check_error: bool = False
) -> GridFunction:
    """
    Computes an L^2 projection of the double layer potential of the internal solution.

    Done by solving `Mg = (K - M/2)u1` for `g`, where `u1` is the internal potential.

    Very similar to the NGBem `Dirichlet Laplace Direct Method` tutorial.

    Parameters:
        pot_int (ngsolve.comp.GridFunction): A H1 grid function.
        mesh (Mesh): The mesh to be integrated over.
        order (int): The integral rule order to be used for building the `DoubleLayerPotentialOperator`
        check_error (bool): Displays convergence information, default is `False`.

    Returns:
        g (ngsolve.comp.GridFunction): A `SurfaceL2` grid function describing the internal potential.
    """
    fesL2 = SurfaceL2(
        mesh, order=1, dual_mapping=True
    )  # unsure if `dual_mapping=True` actually does anything
    u, v = fesL2.TnT()
    fesH1 = H1(mesh, order=1)
    uH1, vH1 = fesH1.TnT()
    g = GridFunction(fesL2)
    with TaskManager():
        # surface mass matrix
        # can write `ds(bonus_intorder=3)` instead of `ds` for additional accuracy, but it doesn't seem to do anything
        M_SURF = BilinearForm(
            u.Trace() * v.Trace() * ds(bonus_intorder=2)
        ).Assemble()  # <u_trace, v_trace>, N_surface x N_surface
        M_H1 = BilinearForm(
            uH1.Trace() * v.Trace() * ds(bonus_intorder=2)
        ).Assemble()  # <uH1_trace, v_trace>, N_surface x N_vol
        K = DoubleLayerPotentialOperator(
            fesH1, fesL2, intorder=order
        )  # double layer potential, rectangular matrix N_surface x N_vol
        f = ((K.mat - 0.5 * M_H1.mat) * pot_int.vec).Evaluate()  # (K - M/2)u_1
        rows, cols, vals = M_SURF.mat.COO()
        A = scipy.sparse.csc_matrix((vals, (rows, cols)))
        F = f.FV().NumPy()[:]
        M2 = scipy.sparse.linalg.spilu(A)  # spilu preconditioner
        M = scipy.sparse.linalg.LinearOperator((F.size, F.size), M2.solve)
        g.vec.FV().NumPy()[:], exitCode = scipy.sparse.linalg.cg(A, F, M=M, rtol=1e-13)
        if check_error is True:
            print(f"exitCode = {exitCode}")
            print(
                f"DL boundary proj, residual = {np.linalg.norm(A.dot(g.vec.FV().NumPy()[:])- F)}"
            )
    return g


def stray_fieldBEM(
    mag_func: GridFunction,
    mesh: Mesh,
    order: int,
    eps: float = 1e-8,
    intorder: int = 12,
    check_error: bool = False,
):
    """
    Uses Weggler style FEM-BEM Coupling to solve for the stray field.

    Parameters:
        mag_func (ngsolve.comp.GridFunction): A `SurfaceL2` grid function.
        mesh (Mesh): The mesh to be integrated over.
        order (int): The polynomial order to be used, defaults to 1.
        eps (float): The tolerance used for the ACA algorithm, defaults to 1e-8.
        intorder (int):  Order used for the integration of layer potentials, defaults to 12.
        check_error (bool): Displays convergence information, default `False`.

    Returns:
        u2 (ngsolve.comp.GridFunction): A `VectorH1` grid function describing the internal potential.
    """
    fesH1 = H1(
        mesh, order=order
    )  # H^1 conforming elements with H^(1/2) conforming elements on boundary
    print("H1-ndof = ", fesH1.ndof)

    l2bounddef = mesh.Boundaries(all_boundaries(mesh))
    u, v = fesH1.TnT()
    with TaskManager():
        a = BilinearForm(
            Grad(u) * Grad(v) * dx
        ).Assemble()  # system matrix of variational formulation in Omega
        f = LinearForm(fesH1)
        f += mag_func * Grad(v) * dx
        # f += -div(mag_func) * v * dx
        f.Assemble()
        fesL2 = SurfaceL2(
            mesh, order=order, dual_mapping=True, definedon=l2bounddef
        )  # H^(-1/2) conforming elements
        f2 = LinearForm(fesL2).Assemble()  # vector of 0's

    print("L2-ndof = ", fesL2.ndof)
    with TaskManager():
        print("building potential operators", flush=True)
        V = SingleLayerPotentialOperator(
            fesL2, intorder=intorder, eps=eps, method="aca"
        )
        K = DoubleLayerPotentialOperator(
            fesH1,
            fesL2,
            trial_definedon=l2bounddef,
            test_definedon=l2bounddef,
            intorder=intorder,
            eps=eps,
            method="aca",
        )
        # D = HypersingularOperator(fesH1, definedon=l2bounddef, intorder=12, eps=1e-10, method="aca")
        print("building linear system")
        M = BilinearForm(
            fesH1.TrialFunction() * fesL2.TestFunction().Trace() * ds(l2bounddef)
        ).Assemble()
        # sym = BlockMatrix ([[a.mat+D.mat, (-0.5*M.mat+K.mat).T],[(-0.5*M.mat+K.mat), -V.mat]])
        rhs = BlockVector([f.vec, f2.vec])
        nonsym = BlockMatrix([[a.mat, -M.mat.T], [(-0.5 * M.mat + K.mat), -V.mat]])
    print("building preconditioner")
    with TaskManager():
        l2mass = BilinearForm(
            fesL2.TrialFunction().Trace() * fesL2.TestFunction().Trace() * ds
        ).Assemble()
        astab = BilinearForm(
            (Grad(u) * Grad(v) + 1e-10 * u * v) * dx
        ).Assemble()  # probably need to change to another preconditioner!
        pre = BlockMatrix(
            [
                [
                    astab.mat.Inverse(
                        freedofs=fesH1.FreeDofs(), inverse="sparsecholesky"
                    ),
                    None,
                ],
                [None, l2mass.mat.Inverse(freedofs=fesL2.FreeDofs())],
            ]
        )
        print("solving linear system", flush=True)
        sol = ngsolve.solvers.GMRes(
            A=nonsym, b=rhs, pre=pre, tol=1e-8, maxsteps=10_000, printrates=True
        )

    gfu = GridFunction(fesH1)
    gfu.vec[:] = sol[0]
    return -Grad(gfu)
