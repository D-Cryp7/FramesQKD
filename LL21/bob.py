import sys
sys.path.append('..')

from LL20 import bob

class Bob(bob.Bob):
    def compute_conjugate_sifting_bits(self, frame):
        conjugate_sifting_bits = {
            "X": 0, 
            "Z": 0
        }
        
        for pair in frame:
            conjugate_sifting_bits[self.measurement_basis[pair]] ^= ~int(self.measurement_results[pair][0]) % 2
            
        return ''.join(map(str, conjugate_sifting_bits.values()))
    
    def compute_conjugate_sifting_string(self, usable_frames):
        conjugate_sifting_string = []
        for frame in usable_frames:
            conjugate_sifting_bits = self.compute_conjugate_sifting_bits(frame)
            conjugate_sifting_string.append(conjugate_sifting_bits)
        return conjugate_sifting_string