import sys
sys.path.append('..')

from LL20 import bob

class Bob(bob.Bob):
    def compute_measured_bits(self, frame):
        # Compute conjugate sifting bits. We overwrite the compute_measured_bits function of the parent class.
        conjugate_sifting_bits = {
            "X": 0, 
            "Z": 0
        }
        
        for pair in frame:
            conjugate_sifting_bits[self.measurement_basis[pair]] ^= ~int(self.measurement_results[pair][0]) % 2
            
        return ''.join(map(str, conjugate_sifting_bits.values()))