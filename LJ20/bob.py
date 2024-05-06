from helpers import MATCHING_RESULTS
from qiskit import Aer, execute
from secrets import randbits

class Bob:
    def __init__(self):
        self.measurement_basis = {}
        self.measurement_results = {}
        self.backend = Aer.get_backend("qasm_simulator")
        
    def measure(self, pairs):
        double_matchings = []
        
        for i in range(len(pairs)):
            basis = randbits(1)
            if basis: # "X" basis measurement
                pairs[i][0].h(0)
                pairs[i][1].h(0)
                
            pairs[i][0].measure(0, 0)
            pairs[i][1].measure(0, 0)
            
            bits = ''.join([ list(execute(circuit, self.backend, shots = 1).result().get_counts().keys())[0] for circuit in pairs[i] ])
            
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
            
    
    def compute_sifting_string(self, usable_frames):
        sifting_string = []
        for frame in usable_frames:
            sifting_bits = self.compute_sifting_bits(frame)
            sifting_string.append(sifting_bits)
        return sifting_string
    
    def generate_shared_key(self, usable_frames):
        shared_secret = ""
        for frame in usable_frames:
            basis_orientation = (self.measurement_basis[frame[0]], self.measurement_basis[frame[1]])
            shared_secret += MATCHING_RESULTS[basis_orientation]
        return shared_secret
            
            