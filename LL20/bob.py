from helpers import MATCHING_RESULTS
from secrets import randbits
from qiskit import transpile
from qiskit_aer import Aer
from qiskit_aer.noise.errors import pauli_error, depolarizing_error
from qiskit_aer.noise import NoiseModel

class Bob:
    def __init__(self, depolarize_probability = 0):
        self.depolarize_probability = depolarize_probability
        
        self.measurement_basis = {}
        self.measurement_results = {}
        self.backend = Aer.get_backend("qasm_simulator")

    def get_noise(self, p, qubits = 1):
        # This creates the depolarizing error channel,
        # epsilon(P) = (1-P)rho + (P/3)(XrhoX + YrhoY + ZrhoZ).
        depo_err_chan = depolarizing_error(4 * p / 3, qubits)

        # Creating the noise model to be used during execution.
        noise_model = NoiseModel()

        noise_model.add_all_qubit_quantum_error(depo_err_chan, "measure") # measurement error is applied to measurements

        return noise_model
        
    def measure(self, pairs):
        double_matchings = []

        noise_model = None
        if self.depolarize_probability:
            noise_model = self.get_noise(self.depolarize_probability)
        
        for i in range(len(pairs)):
            basis = randbits(1)
            if basis: # "X" basis measurement
                pairs[i][0].h(0)
                pairs[i][1].h(0)
                
            pairs[i][0].measure(0, 0)
            pairs[i][1].measure(0, 0)
            
            bits = ''.join([ list(self.backend.run(transpile(circuit, self.backend), noise_model = noise_model).result().get_counts().keys())[0] for circuit in pairs[i] ])
            
            if bits[0] == bits[1]: double_matchings.append(i)
            
            self.measurement_results[i] = bits
            self.measurement_basis[i] = "X" if basis else "Z"
        
        return double_matchings
    
    def compute_sifting_bits(self, frame):
        sifting_bits = {
            "X": 0, 
            "Z": 0
        }
        
        for pair in frame:
            sifting_bits[self.measurement_basis[pair]] ^= int(self.measurement_results[pair][0])
            
        return ''.join(map(str, sifting_bits.values()))

    def compute_measured_bits(self, frame):
        measured_bits = []

        for pair in frame:
            measured_bits.append(self.measurement_results[pair][0]) # since both bits are equal due to the double matching event

        return ''.join(measured_bits)
            
    
    def compute_sifting_string(self, usable_frames):
        sifting_string = []
        for frame in usable_frames:
            sifting_bits = self.compute_sifting_bits(frame)
            sifting_string.append(sifting_bits)
        return sifting_string

    def compute_measured_string(self, usable_frames):
        measured_string = []
        for frame in usable_frames:
            measured_bits = self.compute_measured_bits(frame)
            measured_string.append(measured_bits)
        return measured_string
    
    def generate_shared_key(self, usable_frames):
        shared_secret = ""
        for frame in usable_frames:
            basis_orientation = (self.measurement_basis[frame[0]], self.measurement_basis[frame[1]])
            shared_secret += MATCHING_RESULTS[basis_orientation]
        return shared_secret
            
            