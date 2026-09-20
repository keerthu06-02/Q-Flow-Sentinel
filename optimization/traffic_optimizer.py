# ============================================================
# Q-FLOW SENTINEL
# CLASSICAL TRAFFIC OPTIMIZATION
# ============================================================


def calculate_traffic_pressure(intersections):
    """
    Calculate the traffic pressure at every junction.

    Traffic pressure is based on:
        - current traffic
        - queue length
    """

    pressure = {}

    for junction, data in intersections.items():

        traffic = data["traffic"]

        queue = data["queue"]

        pressure[junction] = (
            traffic + (queue * 2)
        )

    return pressure


# ============================================================
# CALCULATE OPTIMAL GREEN TIMES
# ============================================================

def calculate_optimal_green_times(
    intersections,
    minimum_green=15,
    maximum_green=60
):
    """
    Calculate a classical traffic-signal solution.

    Higher traffic pressure receives more green time.

    The result is returned as a dictionary.
    """

    pressure = calculate_traffic_pressure(
        intersections
    )

    total_pressure = sum(
        pressure.values()
    )

    optimized_times = {}

    # --------------------------------------------------------
    # Avoid division by zero
    # --------------------------------------------------------

    if total_pressure == 0:

        for junction in intersections:

            optimized_times[junction] = minimum_green

        return optimized_times

    # --------------------------------------------------------
    # Allocate green time
    # --------------------------------------------------------

    for junction in intersections:

        junction_pressure = pressure[junction]

        share = (
            junction_pressure
            / total_pressure
        )

        green_time = (
            minimum_green
            + share * 90
        )

        green_time = max(
            minimum_green,
            green_time
        )

        green_time = min(
            maximum_green,
            green_time
        )

        optimized_times[junction] = round(
            green_time
        )

    return optimized_times


# ============================================================
# APPLY OPTIMIZED SIGNAL TIMINGS
# ============================================================

def apply_optimized_green_times(
    intersections,
    optimized_times
):
    """
    Apply optimized green-light timings
    to the traffic network.
    """

    for junction in intersections:

        if junction in optimized_times:

            intersections[junction][
                "green_time"
            ] = optimized_times[junction]

    return intersections


# ============================================================
# CALCULATE TOTAL GREEN TIME
# ============================================================

def calculate_total_green_time(
    intersections
):
    """
    Calculate the total green time
    across all junctions.
    """

    total = 0

    for data in intersections.values():

        total += data["green_time"]

    return total


# ============================================================
# CALCULATE ESTIMATED WAITING TIME
# ============================================================

def calculate_estimated_waiting_time(
    intersections
):
    """
    Estimate total waiting time.

    More traffic and longer queues increase
    estimated waiting time.

    Higher green time reduces the estimated wait.
    """

    total_waiting_time = 0

    for data in intersections.values():

        traffic = data["traffic"]

        queue = data["queue"]

        green_time = data["green_time"]

        effective_green = max(
            green_time,
            1
        )

        waiting_time = (
            traffic
            + (queue * 2)
        ) / effective_green

        total_waiting_time += waiting_time

    return round(
        total_waiting_time,
        2
    )


# ============================================================
# OPTIMIZATION SUMMARY
# ============================================================

def get_optimization_summary(
    intersections,
    optimized_times
):
    """
    Create a summary of the optimized
    traffic signal plan.
    """

    summary = []

    for junction in intersections:

        current_time = intersections[
            junction
        ]["green_time"]

        optimized_time = optimized_times[
            junction
        ]

        summary.append({

            "Junction": junction,

            "Current Green Time":
                current_time,

            "Optimized Green Time":
                optimized_time,

            "Change":
                optimized_time - current_time

        })

    return summary