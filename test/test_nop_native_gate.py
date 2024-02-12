#!/usr/bin/env python


# Setup:
#   python -m venv _env_qiskit
#   source _env_qiskit/bin/activate
#   pip install -r requirements.txt
#   pip install qiskit
#   # pip install qiskit[visualization]
#   pip install -e . # to get the qiskit-ionq package


API_KEY="<YOUR_SECRET_KEY>"


# Note: Imports are done in the below example functions
#       to illustrate the dependencies of each (and ease of
#       copy and paste to external files).

def qc_example_load(qpy_filename = "example_circ_no_delay.qpy"):
    """
    Load a Qiskit exported .qpy circuit
    """
    from qiskit import QuantumCircuit, qpy
    with open(qpy_filename, 'rb') as fd:
        circuit = qpy.load(fd)[0]
    return circuit


def qc_example_qis_gates():
    """
    Create a basic Bell State qis circuit
    """
    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def qc_example_native_gates():
    """
    Create a native gate circuit with a nop gate
    """
    from qiskit import QuantumCircuit
    # import ionq native gates
    from qiskit_ionq import GPIGate, GPI2Gate, MSGate

    # initialize a quantum circuit
    circuit = QuantumCircuit(2, 2)
    # add gates
    circuit.append(MSGate(0, 0), [0, 1])
    circuit.append(GPIGate(0), [0])
    circuit.append(GPI2Gate(1), [1])
    circuit.measure([0, 1], [0, 1])
    return circuit


def qc_example_native_gates_with_nop():
    """
    Create a native gate circuit with a nop gate
    """
    from qiskit import QuantumCircuit
    # import ionq native gates
    from qiskit_ionq import GPIGate, GPI2Gate, MSGate, NOPGate

    # initialize a quantum circuit
    circuit = QuantumCircuit(2, 2)
    # add gates
    circuit.append(MSGate(0, 0), [0, 1])
    circuit.append(GPIGate(0), [0])
    circuit.append(NOPGate(1.2))
    circuit.append(GPI2Gate(1), [1])
    circuit.measure([0, 1], [0, 1])
    return circuit


from qiskit_ionq import IonQProvider
provider = IonQProvider(API_KEY)

# >> Run the qis circuit on IonQ's simulator <<
#qpu = provider.get_backend("ionq_simulator", gateset="qis")    # IonQ's simulator backend; note gateset="native" can be used also
#job = qpu.run(qc_example_qis_gates(), shots=100)

# >> Run the native circuit on IonQ's qpu hardware <<
#qpu = provider.get_backend("ionq_qpu.aria-1", gateset="native") # IonQ's aria-1 (system5) production backend
qpu = provider.get_backend("ionq_qpu.harmony-1", gateset="native") # IonQ's retired system3 used for q-ctrl job submission testing
job = qpu.run(qc_example_native_gates_with_nop(), shots=100)

# print the counts
print(job.get_counts())

# The simulator provides the ideal probabilities from the circuit, and the provider
# creates “counts” by randomly sampling from these probabilities. The raw (“true”)
# probabilities are also accessible by calling get_probabilities():
print(job.get_probabilities())

# Get results with a different aggregation method when de-biasing
# is applied as an error mitigation strategy
print(job.result(sharpen=True).get_counts())

