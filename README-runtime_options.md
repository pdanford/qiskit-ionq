Specifying runtime_options with IonQ jobs
================================================================================

Note that the `runtime_options` parameter is currently (2024-02) only supported in IonQ native gate circuits.

### Qiskit


This is an example Qiskit python script that shows how to attach runtime options to a circuit composed of IonQ native gates:

```
#!/usr/bin/env python

# Requires:
#     python3
#     requirements.txt
#
# Setup:
#     0. cd qiskit-ionq
#     1. git checkout custom-features
#     2. python -m venv _env_qiskit && source _env_qiskit/bin/activate
#     3. pip install -e .   # to install this custom qiskit-ionq package
#
# Running:
#   0. cd qiskit-ionq
#   1. source _env_qiskit/bin/activate
#   2. fill in SECRET_API_KEY below
#   3. ./<this_python_script.py>


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


from qiskit_ionq import IonQProvider

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
                                                    0.03593138382089995,
                                                    0.058692626385449094
                                                ]
                                            }
                                        }
                                    }
                                }
                            """

job = qpu.run(qc_example_native_gates(), shots=100, runtime_options_json=our_runtime_options_json)

# print the counts and probabilities
# print(job.get_counts())
# print(job.get_probabilities())
```

### curl

This shows how to attach runtime options to a job submission via `curl` to a circuit composed of IonQ native gates:

```
JOB_ID=$(
curl -X POST "${CLOUD_URL}/v0.3/jobs/"                  \
     --header "Content-Type: application/json"          \
     --header "Authorization: apiKey ${SECRET_API_KEY}" \
     -d '{
             "target": "ionq_qpu.system-1",
             "input":
             {
                 "format": "ionq.circuit.v0",
                 "qubits": 11,
                 "gateset": "native",
                 "circuit":
                 [
                     {
                         "gate": "ms",
                         "targets":
                         [
                             0,
                             1
                         ],
                         "phases":
                         [
                             0,
                             0
                         ]
                     },
                     {
                         "gate": "nop",
                         "time": 1
                     },
                     {
                         "gate": "gpi",
                         "target": 2,
                         "phase": 0.25
                     }
                 ],
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
         }' \
| tee | jq -r '.id') ; echo ${JOB_ID}
```

###### For a "large" program:

```
JOB_ID=$(
curl -X POST "${CLOUD_URL}/v0.3/jobs/"                  \
     --header "Content-Type: application/json"          \
     --header "Authorization: apiKey ${SECRET_API_KEY}" \
     --data "@cloud.ore"                                \
| tee | jq -r '.id') ; echo ${JOB_ID}
```
