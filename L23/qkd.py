from qiskit_aer.noise.errors import pauli_error, depolarizing_error
from qiskit_aer.noise import NoiseModel
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from secrets import randbits

from alice import Alice
from bob import Bob

backend = Aer.get_backend("qasm_simulator")

class QKD:
    def __init__(self, bits, rounds = 2, depolarize_probability = 0):
        self.bits = bits
        self.alice = Alice(self.generate_random_bits, self.generate_random_basis)
        self.bob = Bob(self.generate_random_basis)
        
        assert rounds == 1 or rounds == 2, "Rounds must be 1 or 2"
        self.rounds = rounds
        self.depolarize_probability = depolarize_probability
    
    def generate_random_bits(self):
        random_bits = ''.join([ str(randbits(1)) for _ in range(self.bits) ])
        return random_bits
    
    def generate_random_basis(self):
        random_bits = self.generate_random_bits()
        return [ "X" if eval(bit) else "Z" for bit in random_bits ]
    
    def get_noise(self, p, qubits = 1):
        # This creates the depolarizing error channel,
        # epsilon(P) = (1-P)rho + (P/3)(XrhoX + YrhoY + ZrhoZ).
        depo_err_chan = depolarizing_error(4 * p / 3, qubits)

        # Creating the noise model to be used during execution.
        noise_model = NoiseModel()

        noise_model.add_all_qubit_quantum_error(depo_err_chan, "measure") # measurement error is applied to measurements

        return noise_model
        
    def generate_circuit(self, bit):
        circuit = QuantumCircuit(1, 1)
        
        # Bit encoding circuit
        if bit: circuit.x(0)
        
        return circuit
    
    def get_counts(self):
        return self.alice.INFO
    
    def generate_raw_key(self):
        alice_raw_key = self.alice.bits
        bob_raw_key = ""
        
        noise_model = None
        if self.depolarize_probability:
            noise_model = self.get_noise(self.depolarize_probability)

        for i in range(self.bits):
            bit = int(alice_raw_key[i])
            circuit = self.generate_circuit(bit)
            if self.alice.basis[i] == "X": circuit.h(0)
            if self.bob.basis[i] == "X": circuit.h(0)

            circuit.measure(0, 0)
            
            job = backend.run(transpile(circuit, backend = backend), noise_model = noise_model)
            
            result = job.result()
            counts = result.get_counts()

            bit_result = list(counts.keys())[0]
            bob_raw_key += bit_result
            
        return alice_raw_key, bob_raw_key
            
    def generate_sifting_key(self, alice_raw_key, bob_raw_key):
        lists = {
            "L1": [],
            "L2": []
        }
        for _ in range(self.rounds):
            self.alice.generate_states_data(alice_raw_key)
            L1, L2 = self.bob.generate_L1_and_L2(bob_raw_key)
            verify = self.alice.calculate_bob_basis(L1, L2)
            if not verify:
                self.bob.shared_secret.pop()
            else:
                lists["L1"].append(L1)
                lists["L2"].append(L2)
            alice_raw_key = alice_raw_key.replace('1', '2').replace('0', '1').replace('2', '0')
            bob_raw_key = bob_raw_key.replace('1', '2').replace('0', '1').replace('2', '0')
        return self.alice.shared_secret, "".join(self.bob.shared_secret), lists