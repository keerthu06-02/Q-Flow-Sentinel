# ============================================================
# Q-FLOW SENTINEL
# SIMPLE QUANTUM TRAFFIC SOLVER
# ============================================================

import math

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# ============================================================
# QUBO COST
# ============================================================

def calculate_solution_cost(model, bitstring):

    variables = list(model["linear"].keys())

    bits = bitstring[::-1]

    values = {}

    for i, variable in enumerate(variables):

        if i < len(bits):
            values[variable] = int(bits[i])
        else:
            values[variable] = 0

    cost = model["offset"]

    for variable, coefficient in model["linear"].items():

        cost += (
            coefficient
            * values.get(variable, 0)
        )

    for (
        variable_a,
        variable_b
    ), coefficient in model["quadratic"].items():

        cost += (
            coefficient
            * values.get(variable_a, 0)
            * values.get(variable_b, 0)
        )

    return cost


# ============================================================
# SIMPLE QAOA CIRCUIT
# ============================================================

def create_qaoa_circuit(
    number_of_qubits,
    gamma,
    beta
):

    circuit = QuantumCircuit(
        number_of_qubits,
        number_of_qubits
    )

    # Put all qubits into superposition
    for qubit in range(number_of_qubits):
        circuit.h(qubit)

    # Simple QAOA cost/mixer layer
    for qubit in range(number_of_qubits):

        circuit.rz(
            2 * gamma,
            qubit
        )

        circuit.rx(
            2 * beta,
            qubit
        )

    # Measure
    circuit.measure(
        range(number_of_qubits),
        range(number_of_qubits)
    )

    return circuit


# ============================================================
# RUN SIMPLE QAOA
# ============================================================

def run_simple_qaoa(
    model,
    gamma=math.pi / 4,
    beta=math.pi / 4,
    shots=32
):

    number_of_qubits = len(
        model["linear"]
    )

    circuit = create_qaoa_circuit(
        number_of_qubits,
        gamma,
        beta
    )

    simulator = AerSimulator()

    job = simulator.run(
        circuit,
        shots=shots
    )

    result = job.result()

    counts = result.get_counts()

    # Find the lowest-cost measured solution
    best_bitstring = None
    best_cost = float("inf")

    for bitstring in counts:

        cost = calculate_solution_cost(
            model,
            bitstring
        )

        if cost < best_cost:

            best_cost = cost
            best_bitstring = bitstring

    return {
        "bitstring": best_bitstring,
        "cost": round(best_cost, 4),
        "gamma": gamma,
        "beta": beta,
        "counts": counts
    }


# ============================================================
# DECODE GREEN TIMES
# ============================================================

def decode_green_times(
    bitstring,
    variables,
    green_time_options
):

    bits = bitstring[::-1]

    selected_times = {}

    position = 0

    for junction in variables:

        selected_times[junction] = None

        for green_time in green_time_options:

            if position < len(bits):

                if bits[position] == "1":

                    selected_times[
                        junction
                    ] = green_time

            position += 1

    return selected_times