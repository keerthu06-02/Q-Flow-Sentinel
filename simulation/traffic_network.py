# ============================================================
# MULTI-INTERSECTION TRAFFIC NETWORK
# ============================================================

def create_traffic_network():
    """
    Create the connected multi-intersection road network.
    """

    roads = [
        ("J1", "J3"),
        ("J2", "J3"),
        ("J3", "J4"),
        ("J3", "J5"),
        ("J5", "J6")
    ]

    return roads


def calculate_neighbor_traffic(intersections):
    """
    Calculate traffic pressure coming from connected
    neighboring intersections.
    """

    roads = create_traffic_network()

    neighbor_traffic = {}

    for junction in intersections:
        neighbor_traffic[junction] = 0

    for junction_a, junction_b in roads:

        traffic_a = intersections[junction_a]["traffic"]
        traffic_b = intersections[junction_b]["traffic"]

        neighbor_traffic[junction_a] += traffic_b
        neighbor_traffic[junction_b] += traffic_a

    return neighbor_traffic


def propagate_traffic(intersections, propagation_rate=0.10):
    """
    Simulate traffic spreading between connected intersections.

    A small percentage of traffic pressure from each neighboring
    intersection is transferred to the current intersection.
    """

    roads = create_traffic_network()

    traffic_change = {}

    for junction in intersections:
        traffic_change[junction] = 0

    for junction_a, junction_b in roads:

        traffic_a = intersections[junction_a]["traffic"]
        traffic_b = intersections[junction_b]["traffic"]

        difference = traffic_a - traffic_b

        transfer = difference * propagation_rate

        traffic_change[junction_a] -= transfer
        traffic_change[junction_b] += transfer

    for junction in intersections:

        new_traffic = (
            intersections[junction]["traffic"]
            + traffic_change[junction]
        )

        new_traffic = max(0, new_traffic)

        intersections[junction]["traffic"] = round(new_traffic)

        intersections[junction]["queue"] = round(
            new_traffic * 0.30
        )

    return intersections


def get_network_congestion(intersections):
    """
    Calculate total traffic and queue across the
    complete multi-intersection network.
    """

    total_traffic = 0
    total_queue = 0

    for data in intersections.values():

        total_traffic += data["traffic"]
        total_queue += data["queue"]

    return {
        "Total Traffic": round(total_traffic),
        "Total Queue": round(total_queue)
    }