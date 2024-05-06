from helpers import USABLE_FRAMES, MATCHING_RESULTS_DERIVATION
from itertools import combinations
from qiskit import QuantumCircuit
from secrets import randbits

class Alice:
    def __init__(self, pairs):
        self.pairs = pairs
        self.pairs_data = {}
        
        self.usable_frames = USABLE_FRAMES
        self.usable_frames_iterable = list(self.usable_frames.keys())
        
        self.generate_pairs()
        
    def generate_pairs(self):
        for i in range(self.pairs):
            x, z = [ randbits(1) for _ in range(2) ]
            self.pairs_data[i] = str(x) + "x," + str(z) + "z"
            
    def generate_circuits(self, pair):
        x, z = [ int(state[0]) for state in pair.split(",") ]
        circuits = [ QuantumCircuit(1, 1) for _ in range(2) ]
        
        if x: circuits[0].x(0)
        if z: circuits[1].x(0)
        
        circuits[0].h(0)
        
        return circuits
    
    def prepare(self):
        pairs = []
        for i in range(self.pairs):
            circuits = self.generate_circuits(self.pairs_data[i])
            pairs.append(circuits)
        return pairs
    
    def public_frame_to_private_frame(self, frame):
        return (self.pairs_data[frame[0]], self.pairs_data[frame[1]])
        
    
    def compute_usable_frames(self, double_matchings):
        usable_frames = []
        usable_frames_types = []
        
        public_frames = list(combinations(double_matchings, 2))
        for public_frame in public_frames:
            private_frame = self.public_frame_to_private_frame(public_frame)
            if private_frame in self.usable_frames_iterable:
                usable_frames.append(public_frame)
                usable_frames_types.append(self.usable_frames[private_frame])
                
        return usable_frames, usable_frames_types
    
    def generate_shared_key(self, usable_frames_types, sifting_string):
        shared_secret = ""
        for i in range(len(sifting_string)):
            shared_secret += MATCHING_RESULTS_DERIVATION[usable_frames_types[i]][sifting_string[i]]
        
        return shared_secret
        
        
            