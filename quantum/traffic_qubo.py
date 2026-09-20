# ============================================================
# Q-FLOW SENTINEL
# QUANTUM TRAFFIC OPTIMIZATION
# QUBO MODEL
# ============================================================


# ============================================================
# CREATE GREEN-TIME OPTIONS
# ============================================================

def create_green_time_options(
    minimum_green=15,
    maximum_green=60,
    step=15
):
    """
    Create the possible green-light timing options.

    Example:

        15 seconds
        30 seconds
        45 seconds
        60 seconds
    """

    options = []

    current = minimum_green

    while current <= maximum_green:

        options.append(current)

        current += step

    return options


# ============================================================
# CREATE BINARY VARIABLES
# ============================================================

def create_binary_variables(
    intersections,
    green_time_options
):
    """
    Create binary decision variables.

    Each variable represents one possible
    green-light timing for one junction.

    Example:

        J1_15
        J1_30
        J1_45
        J1_60
    """

    variables = {}

    for junction in intersections:

        variables[junction] = {}

        for green_time in green_time_options:

            variable_name = (
                f"{junction}_{green_time}"
            )

            variables[junction][
                green_time
            ] = variable_name

    return variables


# ============================================================
# CALCULATE TRAFFIC PRESSURE
# ============================================================

def calculate_traffic_pressure(
    intersections
):
    """
    Calculate traffic pressure at each junction.

    Traffic pressure combines:

        traffic volume
        +
        queue length
    """

    pressure = {}

    for junction, data in intersections.items():

        traffic = data["traffic"]

        queue = data["queue"]

        pressure[junction] = (
            traffic + (2 * queue)
        )

    return pressure


# ============================================================
# CREATE QUBO COEFFICIENTS
# ============================================================

def create_qubo_coefficients(
    intersections,
    green_time_options
):
    """
    Create the QUBO objective coefficients.

    Lower cost is preferred.

    Higher traffic pressure receives
    lower cost for longer green times.
    """

    pressure = calculate_traffic_pressure(
        intersections
    )

    coefficients = {}

    for junction in intersections:

        coefficients[junction] = {}

        for green_time in green_time_options:

            # Longer green time reduces the
            # cost for a busy junction.

            cost = (
                pressure[junction]
                / green_time
            )

            coefficients[junction][
                green_time
            ] = round(cost, 4)

    return coefficients


# ============================================================
# CREATE QUBO MODEL
# ============================================================

def create_qubo_model(
    intersections,
    green_time_options=None
):
    """
    Create the complete QUBO representation.

    Returns:

        {
            "variables": ...,
            "linear": ...,
            "quadratic": ...,
            "offset": ...,
            "green_time_options": ...
        }
    """

    if green_time_options is None:

        green_time_options = (
            create_green_time_options()
        )

    variables = create_binary_variables(

        intersections,

        green_time_options

    )

    coefficients = create_qubo_coefficients(

        intersections,

        green_time_options

    )

    linear = {}

    quadratic = {}

    offset = 0

    # --------------------------------------------------------
    # LINEAR TERMS
    # --------------------------------------------------------

    for junction in intersections:

        for green_time in green_time_options:

            variable = variables[
                junction
            ][green_time]

            linear[variable] = coefficients[
                junction
            ][green_time]

    # --------------------------------------------------------
    # ONE-TIMING-PER-JUNCTION CONSTRAINT
    # --------------------------------------------------------
    #
    # We want exactly ONE green-time option
    # selected for every junction.
    #
    # Constraint:
    #
    # (x1 + x2 + x3 + x4 - 1)^2
    #
    # This creates:
    #
    # linear penalty terms
    # +
    # quadratic penalty terms
    #
    # --------------------------------------------------------

    penalty = 100

    for junction in intersections:

        junction_variables = []

        for green_time in green_time_options:

            variable = variables[
                junction
            ][green_time]

            junction_variables.append(
                variable
            )

            # Linear part of the constraint

            linear[variable] += -penalty

        # Quadratic part

        for i in range(
            len(junction_variables)
        ):

            for j in range(
                i + 1,
                len(junction_variables)
            ):

                variable_a = (
                    junction_variables[i]
                )

                variable_b = (
                    junction_variables[j]
                )

                key = (
                    variable_a,
                    variable_b
                )

                quadratic[key] = (
                    quadratic.get(key, 0)
                    + 2 * penalty
                )

        # Constant part

        offset += penalty

    return {

        "variables": variables,

        "linear": linear,

        "quadratic": quadratic,

        "offset": offset,

        "green_time_options":
            green_time_options

    }


# ============================================================
# CALCULATE QUBO COST
# ============================================================

def calculate_qubo_cost(
    model,
    solution
):
    """
    Calculate the cost of a QUBO solution.

    solution should contain:

        variable_name -> 0 or 1
    """

    linear = model["linear"]

    quadratic = model["quadratic"]

    offset = model["offset"]

    cost = offset

    # --------------------------------------------------------
    # LINEAR TERMS
    # --------------------------------------------------------

    for variable, coefficient in linear.items():

        value = solution.get(
            variable,
            0
        )

        cost += (
            coefficient * value
        )

    # --------------------------------------------------------
    # QUADRATIC TERMS
    # --------------------------------------------------------

    for (
        variable_a,
        variable_b
    ), coefficient in quadratic.items():

        value_a = solution.get(
            variable_a,
            0
        )

        value_b = solution.get(
            variable_b,
            0
        )

        cost += (
            coefficient
            * value_a
            * value_b
        )

    return round(
        cost,
        4
    )


# ============================================================
# CREATE A SIMPLE CLASSICAL QUBO SOLUTION
# ============================================================

def create_classical_qubo_solution(
    model,
    intersections
):
    """
    Create a baseline solution by selecting
    the lowest-cost green-time option for
    every junction.

    This is NOT the quantum solution.

    It is only a simple reference solution
    for testing the QUBO model.
    """

    solution = {}

    variables = model["variables"]

    green_time_options = (
        model["green_time_options"]
    )

    pressure = calculate_traffic_pressure(
        intersections
    )

    selected_times = {}

    for junction in intersections:

        best_time = None

        best_cost = float("inf")

        for green_time in green_time_options:

            cost = (
                pressure[junction]
                / green_time
            )

            if cost < best_cost:

                best_cost = cost

                best_time = green_time

        selected_times[junction] = (
            best_time
        )

    # --------------------------------------------------------
    # Convert selected timings into binary
    # variables.
    # --------------------------------------------------------

    for junction in intersections:

        for green_time in green_time_options:

            variable = variables[
                junction
            ][green_time]

            if (
                green_time
                == selected_times[junction]
            ):

                solution[variable] = 1

            else:

                solution[variable] = 0

    return solution, selected_times