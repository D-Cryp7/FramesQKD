import sys
sys.path.append('..')

from LL20 import bob
from helpers import MATCHING_RESULTS

class Bob(bob.Bob):

    def compute_sifting_bits(self, frame):
        sifting_bits = {
            "X": 0, 
            "Z": 0
        }

        frame_basis = []
        
        for pair in frame:
            sifting_bits[self.measurement_basis[pair]] ^= int(self.measurement_results[pair][0])
            frame_basis.append(self.measurement_basis[pair])

        sifting_bits = ''.join(map(str, sifting_bits.values()))

        if frame_basis == ["X", "X", "X"] or frame_basis == ["Z", "Z", "Z"] or frame_basis == ["X", "Z", "X"] or frame_basis == ["Z", "X", "Z"]:
            sifting_bits += "0"
        else:
            sifting_bits += "1"       
            
        return sifting_bits

    def compute_sifting_string(self, usable_frames):
        sifting_string = []
        for frame in usable_frames:
            sifting_bits = self.compute_sifting_bits(frame)
            sifting_string.append(sifting_bits)
        return sifting_string
    
    def generate_shared_key(self, usable_frames):
        shared_secret = ""
        for frame in usable_frames:
            basis_orientation = (self.measurement_basis[frame[0]], self.measurement_basis[frame[1]], self.measurement_basis[frame[2]])
            shared_secret += MATCHING_RESULTS[basis_orientation]
        return shared_secret