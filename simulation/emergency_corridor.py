# ============================================================
# Q-FLOW SENTINEL
# EMERGENCY GREEN CORRIDOR
# ============================================================

import networkx as nx


def create_emergency_network():
    """
    Create the road network used by the emergency vehicle system.
    """

    network = nx.Graph()

    roads = [
        ("J1", "J3"),
        ("J2", "J3"),
        ("J3", "J4"),
        ("J3", "J5"),
        ("J5", "J6")
    ]

    network.add_edges_from(roads)

    return network


def find_emergency_route(
    start_junction,
    destination_junction,
    blocked_junctions=None
):
    """
    Find the shortest emergency route while avoiding
    blocked junctions.

    blocked_junctions:
        List of junctions that cannot be used because of
        active road closures.
    """

    network = create_emergency_network()

    if blocked_junctions is None:
        blocked_junctions = []

    # Remove blocked junctions from the network
    for junction in blocked_junctions:

        if junction in network:
            network.remove_node(junction)

    # If start or destination is blocked,
    # an emergency route cannot be created.
    if start_junction not in network:
        return []

    if destination_junction not in network:
        return []

    try:

        route = nx.shortest_path(
            network,
            source=start_junction,
            target=destination_junction
        )

        return route

    except nx.NetworkXNoPath:

        return []


def calculate_normal_travel_time(intersections, route):
    """
    Estimate normal travel time through the route.
    """

    if not route:
        return 0

    total_time = 0

    for junction in route:

        traffic = intersections[junction]["traffic"]

        junction_time = 5 + (traffic * 0.10)

        total_time += junction_time

    return round(total_time, 1)


def calculate_emergency_travel_time(intersections, route):
    """
    Estimate emergency travel time when the green
    corridor is active.
    """

    if not route:
        return 0

    total_time = 0

    for junction in route:

        traffic = intersections[junction]["traffic"]

        junction_time = 3 + (traffic * 0.05)

        total_time += junction_time

    return round(total_time, 1)


def get_green_corridor(route):
    """
    Return the junctions that should receive
    emergency green priority.
    """

    return route


def calculate_time_saving(normal_time, emergency_time):
    """
    Calculate estimated time saved by the
    emergency green corridor.
    """

    if normal_time <= 0:
        return 0

    saving = normal_time - emergency_time

    return round(max(0, saving), 1)