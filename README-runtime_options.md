Specifying runtime_options with an Ionq native gate circuit
================================================================================

This is an example python script that shows how to attach runtime options to a program composed of IonQ native gates.

```
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


def qc_example_load(qpy_filename = "example_circ.qpy"):
    """
    Load a Qiskit exported .qpy circuit
    """
    from qiskit import QuantumCircuit, qpy
    with open(qpy_filename, 'rb') as fd:
        circuit = qpy.load(fd)[0]
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


from qiskit_ionq import IonQProvider
provider = IonQProvider(API_KEY)

# >> Run the native circuit on IonQ's qpu hardware <<
qpu = provider.get_backend("ionq_qpu.system-1", gateset="native")testing

# >> Minimal example of attaching runtime_options
#    Note: in real world use, runtime_options_json would typically be loaded from a file due to size.
runtime_options_json = """
                            {
                            "runtime_options":
                                {
                                    "custom_pulse_shapes":
                                    {
                                        "schema": "am-v4",
                                        "iteration": 0,
                                        "seed_source": "c2-am-v4-2023-07-18-lsrd-iq",
                                        "(0,1)":
                                        {
                                            "tag": "0+1:0",
                                            "durationUsec": 729.6,
                                            "scale": 0.6895113158792494,
                                            "amplitudes":
                                            [
                                                0.03593138382089995,
                                                0.058692626385449094
                                            ]
                                        }
                                    }
                                }
                            }
                            """

job = qpu.run(qc_example_native_gates(), shots=100, runtime_options_json=runtime_options_json)

# print the counts
print(job.get_counts())

print(job.get_probabilities())
```

