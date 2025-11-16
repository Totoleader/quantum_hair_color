from qiskit import QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram


def build_n_hair_coulours_quantum_circuit(num_players: int) -> QuantumCircuit:
    """
    Builds a quantum circuit for the 2 hair color problem with num_players players.

    Args:
        num_players (int): Total number of players.

    Returns:
        QuantumCircuit: Circuit representing the 2 hair color problem for num_players players.
    """
    participant_register = QuantumRegister(num_players)
    reasoning_register = QuantumRegister(num_players)

    circuit = QuantumCircuit(participant_register, reasoning_register)

    for participant_index in range(num_players):
        circuit.h(participant_register[participant_index])

    for turn in range(1, num_players):
        num_targets = num_players - turn
        control_qubit = turn - 1

        for i in range(num_targets):
            circuit.cx(participant_register[turn + i], reasoning_register[control_qubit])

        for i in range(num_targets):
            circuit.cx(reasoning_register[control_qubit], reasoning_register[turn + i])

    circuit.measure_all()
    return circuit


def run_circuit(circuit: QuantumCircuit, shots: int = 10_000) -> dict:
    """
    Runs a quantum circuit with a specified number of shots.

    Args:
        circuit (QuantumCircuit): Circuit to be run.
        shots (int): Number of times we want to run the simulation.

    Returns:
        dict: dictionnary containing bit strings mapped to their number of occurences in the output.
    """
    simulator = AerSimulator()
    pass_manager = generate_preset_pass_manager(backend=simulator)
    isa_circuit = pass_manager.run(circuit)

    job = simulator.run(isa_circuit, shots=shots)
    counts = job.result().get_counts()

    return counts


def plot_quantum_circuit_result(circuit_output: dict) -> None:
    """
    Plots the output of running a quantum circuit as an histogram.

    Args:
        circuit_output (dict): Circuit output to be plotted.
    """
    fig = plot_histogram(circuit_output)
    fig.savefig("quantum_circuit_histogram.png") #optional
    print(fig)


def main() -> None:
    num_players = 4
    qc = build_n_hair_coulours_quantum_circuit(num_players)
    
    circuit_output = run_circuit(qc)
    plot_quantum_circuit_result(circuit_output)


if __name__ == "__main__":
    main()

