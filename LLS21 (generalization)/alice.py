import sys
sys.path.append('..')

from LL20 import alice
from itertools import combinations

class Alice(alice.Alice):
    def public_frame_to_private_frame(self, frame):
        return (self.pairs_data[frame[0]], self.pairs_data[frame[1]], self.pairs_data[frame[2]])
    
    def compute_usable_frames(self, double_matchings):
        usable_frames = []
        usable_frames_types = []
        
        public_frames = list(combinations(double_matchings, 3))
        for public_frame in public_frames:
            private_frame = self.public_frame_to_private_frame(public_frame)
            if private_frame in self.usable_frames_iterable:
                usable_frames.append(public_frame)
                usable_frames_types.append(self.usable_frames[private_frame])
                
        return usable_frames, usable_frames_types