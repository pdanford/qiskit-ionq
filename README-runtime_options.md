Specifying runtime_options with IonQ jobs
================================================================================

Note that the `runtime_options` parameter is currently (2024-12) only supported in IonQ native gate circuits.

### Qiskit


This is an example Qiskit python script that shows how to attach runtime options to a circuit composed of IonQ native gates:

```
#!/usr/bin/env python

# Requires:
#     python3 (tested on python 3.9 through 3.12)
#     requirements.txt
#
# Setup:
#     0. git clone https://github.com/pdanford/qiskit-ionq.git
#     1. cd qiskit-ionq
#     2. git checkout custom-features
#     3. python -m venv _env_qiskit && source _env_qiskit/bin/activate
#     4. pip install -e .   # to install this custom qiskit-ionq package
#
# Running:
#     0. cd qiskit-ionq
#     1. source _env_qiskit/bin/activate
#     2. fill in SECRET_API_KEY below
#     3. ./<this_python_script.py>


SECRET_API_KEY="<YOUR_SECRET_KEY>"


# Note: Imports are done in the below example functions instead
#       of here to illustrate the dependencies of each function.


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


from qiskit_ionq import IonQProvider, ErrorMitigation

provider = IonQProvider(SECRET_API_KEY)

# >> Run the native circuit on IonQ's qpu hardware <<
qpu = provider.get_backend("ionq_qpu.system-1", gateset="native")

# >> Minimal example of attaching runtime_options
#    Note: in real world use, our_runtime_options_json would typically be loaded from a file due to size.
our_runtime_options_json =  """
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
                                                    0.011111111111111111,
                                                    0.022222222222222222
                                                ]
                                            }
                                        }
                                    }
                                }
                            """

job = qpu.run(qc_example_native_gates(),
             shots=100,
             error_mitigation=ErrorMitigation.NO_DEBIASING,
             runtime_options_json=our_runtime_options_json)

# print the counts and probabilities
# print(job.get_counts())
# print(job.get_probabilities())
```

**Note:** To disable the usage of logical qubits and refer to the physical qubits for the gates, the `error_mitigation=ErrorMitigation.NO_DEBIASING` option must be used in the above `run` parameters. For more, see https://docs.ionq.com/sdks/qiskit/error-mitigation-qiskit#specifying-the-debiasing-settings
