from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PulpSolverError

def optimize_table_assignment(reservations, tables, penalty_unassigned=1000):
    """
    Asigna reservas a mesas disponibles minimizando:
    - sillas sin usar
    - reservas sin asignar (penalizadas)

    Parámetros
    ----------
    reservations : list of (id, guests)
    tables : list of (id, capacity)
    penalty_unassigned : int
        Penalización por cada reserva no asignada (λ)

    Retorna
    -------
    assignments : list[dict]
        Lista de reservas que fueron asignadas a una mesa.
    """

    feasible_pairs = [
        (i, j)
        for i, (_, guests) in enumerate(reservations)
        for j, (_, capacity) in enumerate(tables)
        if capacity >= guests
    ]

    if not feasible_pairs:
        return []

    x = LpVariable.dicts("assign", feasible_pairs, cat=LpBinary)
    y = LpVariable.dicts("assigned", range(len(reservations)), cat=LpBinary)

    prob = LpProblem("Minimize_Unused_Seats_And_Unassigned", LpMinimize)

    # 🎯 Objetivo: sillas sin usar + penalización por reservas no asignadas
    prob += (
        lpSum(x[(i, j)] * (tables[j][1] - reservations[i][1]) for (i, j) in feasible_pairs)
        + lpSum((1 - y[i]) * penalty_unassigned for i in range(len(reservations)))
    )

    # Vincular x[i,j] con y[i]
    for i in range(len(reservations)):
        prob += lpSum(
            x[(i, j)] for j in range(len(tables)) if (i, j) in feasible_pairs
        ) == y[i]

    # Cada mesa a lo sumo una reserva
    for j in range(len(tables)):
        prob += lpSum(
            x[(i, j)] for i in range(len(reservations)) if (i, j) in feasible_pairs
        ) <= 1

    try:
        prob.solve()
    except PulpSolverError:
        return []

    assignments = []
    for (i, j) in feasible_pairs:
        if x[(i, j)].value() == 1:
            assignments.append({
                "reservation_id": reservations[i][0],
                "table_id": tables[j][0],
                "guests": reservations[i][1],
                "capacity": tables[j][1]
            })

    return assignments
