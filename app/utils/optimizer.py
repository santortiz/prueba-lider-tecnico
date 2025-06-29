from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PulpSolverError

def optimize_table_assignment(reservations, tables):
    """
    Asigna reservas a mesas disponibles minimizando la cantidad total de sillas sin ocupar.

    Parámetros
    ----------
    reservations : list of tuples (id, guests)
        Lista de reservas con su id y número de invitados.
    tables : list of tuples (id, capacity)
        Lista de mesas con su id y capacidad.

    Retorna
    -------
    assignments : list of dict
        Lista con diccionarios que mapean reserva → mesa asignada.
    """

    # Generar las parejas factibles
    feasible_pairs = [
        (i, j)
        for i, (_, guests) in enumerate(reservations)
        for j, (_, capacity) in enumerate(tables)
        if capacity >= guests
    ]

    if not feasible_pairs:
        return []

    # Variables de decisión
    x = LpVariable.dicts("assign", feasible_pairs, cat=LpBinary)

    # Crear problema
    prob = LpProblem("Minimize_Unused_Seats", LpMinimize)

    # Objetivo: minimizar sillas sin usar
    prob += lpSum(
        x[(i, j)] * (tables[j][1] - reservations[i][1])
        for (i, j) in feasible_pairs
    )

    # Cada reserva se asigna exactamente a una mesa
    for i in range(len(reservations)):
        prob += lpSum(
            x[(i, j)] for j in range(len(tables)) if (i, j) in feasible_pairs
        ) == 1

    # Cada mesa se asigna a lo sumo a una reserva
    for j in range(len(tables)):
        prob += lpSum(
            x[(i, j)] for i in range(len(reservations)) if (i, j) in feasible_pairs
        ) <= 1

    try:
        prob.solve()
    except PulpSolverError:
        return []

    # Recuperar asignaciones óptimas
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
