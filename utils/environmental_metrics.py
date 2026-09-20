# ============================================================
# ENVIRONMENTAL METRICS
# ============================================================

def calculate_throughput(intersections):
    """
    Estimate the number of vehicles processed
    during the simulation period.
    """

    total_throughput = 0

    for data in intersections.values():

        traffic = data["traffic"]
        green_time = data["green_time"]

        throughput = traffic * (green_time / 60)

        total_throughput += throughput

    return round(total_throughput)


def calculate_fuel_consumption(intersections):
    """
    Estimate fuel consumption based on traffic
    and waiting conditions.
    """

    total_fuel = 0

    for data in intersections.values():

        traffic = data["traffic"]
        queue = data["queue"]

        # Simple prototype estimation
        fuel = (traffic * 0.05) + (queue * 0.10)

        total_fuel += fuel

    return round(total_fuel, 2)


def calculate_co2_emissions(fuel_consumption):
    """
    Estimate CO2 emissions from fuel consumption.

    Approximation:
    1 litre of fuel = 2.31 kg CO2
    """

    co2 = fuel_consumption * 2.31

    return round(co2, 2)


def calculate_environmental_metrics(intersections):
    """
    Calculate all environmental metrics.
    """

    throughput = calculate_throughput(intersections)

    fuel = calculate_fuel_consumption(intersections)

    co2 = calculate_co2_emissions(fuel)

    return {
        "Throughput": throughput,
        "Fuel Consumption": fuel,
        "CO2 Emissions": co2
    }