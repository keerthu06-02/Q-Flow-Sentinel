# ============================================================
# Q-FLOW SENTINEL
# TRAFFIC EVENT SIMULATOR
# ============================================================


# ============================================================
# APPLY TRAFFIC EVENT
# ============================================================

def apply_event(intersections, event_type, junction):
    """
    Apply a simulated traffic event to one intersection.

    Supported events:
        🚧 Accident
        🚫 Road Closure
        🚗 Traffic Surge
    """

    # --------------------------------------------------------
    # CHECK JUNCTION
    # --------------------------------------------------------

    if junction not in intersections:
        return intersections


    # --------------------------------------------------------
    # ACCIDENT
    # --------------------------------------------------------

    if event_type == "🚧 Accident":

        # Increase traffic because vehicles
        # are being blocked by the accident.
        intersections[junction]["traffic"] += 50

        # Accident creates a larger queue.
        intersections[junction]["queue"] = int(
            intersections[junction]["traffic"] * 0.40
        )


    # --------------------------------------------------------
    # ROAD CLOSURE
    # --------------------------------------------------------

    elif event_type == "🚫 Road Closure":

        # A closed road redirects traffic
        # toward this intersection.
        intersections[junction]["traffic"] += 70

        # Road closure produces a large queue.
        intersections[junction]["queue"] = int(
            intersections[junction]["traffic"] * 0.50
        )


    # --------------------------------------------------------
    # TRAFFIC SURGE
    # --------------------------------------------------------

    elif event_type == "🚗 Traffic Surge":

        # Sudden increase in vehicles.
        intersections[junction]["traffic"] += 30

        # Calculate larger queue.
        intersections[junction]["queue"] = int(
            intersections[junction]["traffic"] * 0.35
        )


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if intersections[junction]["traffic"] < 0:

        intersections[junction]["traffic"] = 0


    return intersections


# ============================================================
# CLEAR TRAFFIC EVENT
# ============================================================

def clear_event(intersections, event_type, junction):
    """
    Remove the effect of a previously applied event.
    """

    # --------------------------------------------------------
    # CHECK JUNCTION
    # --------------------------------------------------------

    if junction not in intersections:
        return intersections


    # --------------------------------------------------------
    # REMOVE ACCIDENT EFFECT
    # --------------------------------------------------------

    if event_type == "🚧 Accident":

        intersections[junction]["traffic"] -= 50


    # --------------------------------------------------------
    # REMOVE ROAD CLOSURE EFFECT
    # --------------------------------------------------------

    elif event_type == "🚫 Road Closure":

        intersections[junction]["traffic"] -= 70


    # --------------------------------------------------------
    # REMOVE TRAFFIC SURGE EFFECT
    # --------------------------------------------------------

    elif event_type == "🚗 Traffic Surge":

        intersections[junction]["traffic"] -= 30


    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if intersections[junction]["traffic"] < 0:

        intersections[junction]["traffic"] = 0


    # --------------------------------------------------------
    # RECALCULATE QUEUE
    # --------------------------------------------------------

    intersections[junction]["queue"] = int(
        intersections[junction]["traffic"] * 0.30
    )


    return intersections


# ============================================================
# GET EVENT DESCRIPTION
# ============================================================

def get_event_description(event_type):

    descriptions = {

        "🚧 Accident":
            "An accident is blocking part of the road and increasing congestion.",

        "🚫 Road Closure":
            "A road closure is redirecting vehicles and increasing traffic.",

        "🚗 Traffic Surge":
            "A sudden increase in vehicles is causing additional congestion."
    }


    return descriptions.get(
        event_type,
        "Unknown traffic event."
    )


# ============================================================
# GET EVENT TRAFFIC INCREASE
# ============================================================

def get_event_impact(event_type):

    impacts = {

        "🚧 Accident": 50,

        "🚫 Road Closure": 70,

        "🚗 Traffic Surge": 30
    }


    return impacts.get(
        event_type,
        0
    )