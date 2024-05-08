from helpers import MATCHING_RESULTS
from itertools import product

def search(special_frames, frames, orientation):
    for s, f in product(special_frames, frames):
        super_frame = s + f
        index = [i for i in range(2) if super_frame.count(super_frame[i]) > 1] # 2 iterations instead of 4. A super frame always have 4 elements
        if index:
            if index[0]: yield s, orientation
            else: yield s, orientation[::-1]
            
def z_search(special_frames, z_frames):
    return search(special_frames, z_frames, ("X", "Z"))
            
def x_search(special_frames, x_frames):
    return search(special_frames, x_frames, ("Z", "X"))
            
def attack(usable_frames, sifting_string):
    assert len(usable_frames) == len(sifting_string), "Each frame must have its associated sifting bits"
    key_recovered = ["  "] * len(usable_frames)
    
    special_frames = []
    z_frames = []
    x_frames = []
    
    # fill lists
    for i in range(len(usable_frames)):
        if sifting_string[i] == "11": special_frames.append(usable_frames[i])
        elif sifting_string[i] == "01": z_frames.append(usable_frames[i])
        elif sifting_string[i] == "10": x_frames.append(usable_frames[i])
        else: continue
        
    # recover Z frames: (-  1z)
    recovered_z_frames_and_orientations = set(z_search(special_frames, z_frames))
    
    # recover X frames: (1x  -)
    recovered_x_frames_and_orientations = set(x_search(special_frames, x_frames))
    
    recovered_frames_and_orientations = set(list(recovered_z_frames_and_orientations) + list(recovered_x_frames_and_orientations))
    
    recovered_frames = [ el[0] for el in recovered_frames_and_orientations ]
    orientations = { el[0]: el[1] for el in recovered_frames_and_orientations }
    
    for i in range(len(usable_frames)):
        if usable_frames[i] in recovered_frames:
            key_recovered[i] = MATCHING_RESULTS[orientations[usable_frames[i]]]
    
    return ''.join(key_recovered)
                
            
    