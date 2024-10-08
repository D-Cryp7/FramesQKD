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

def zero_search(recovered_frames, orientations, zero_frames):
    for s, f in product(recovered_frames, zero_frames):
        super_frame = s + f
        index = [i for i in range(2) if super_frame.count(super_frame[i]) > 1] # 2 iterations instead of 4. A super frame always have 4 elements
        if index:
            if index[0]:
                if orientations[s] == ("X", "Z"): yield f, ("Z", "Z")
                else: yield f, ("X", "X")
            else:
                if orientations[s] == ("X", "Z"): yield f, ("X", "X")
                else: yield f, ("Z", "Z")
    
            
def attack(usable_frames, SS, DEBUG = True):
    assert len(usable_frames) == len(SS), "Each frame must have its associated sifting bits"
    key_recovered = ["  "] * len(usable_frames)
    
    special_frames = []
    z_frames_01 = []
    z_frames_10 = []
    x_frames_01 = []
    x_frames_10 = []
    zero_frames_00 = []
    zero_frames_11 = []

    # fill lists
    for i in range(len(usable_frames)):
        if SS[i] == "11,11": special_frames.append(usable_frames[i])
        elif SS[i] == "01,01": z_frames_01.append(usable_frames[i])
        elif SS[i] == "01,10": z_frames_10.append(usable_frames[i])
        elif SS[i] == "10,01": x_frames_01.append(usable_frames[i])
        elif SS[i] == "10,10": x_frames_10.append(usable_frames[i])
        elif SS[i] == "00,00": zero_frames_00.append(usable_frames[i])
        elif SS[i] == "00,11": zero_frames_11.append(usable_frames[i])
        else: continue
        
    # recover Z frames: (-  1z)
    recovered_z_frames_and_orientations = set(z_search(special_frames, z_frames_01 + z_frames_10))
    
    # recover X frames: (1x  -)
    recovered_x_frames_and_orientations = set(x_search(special_frames, x_frames_01 + x_frames_10))

    # Same as below? (recovered_zero_frames_and_orientations)
    recovered_xx_frames_and_orientations = set(search(zero_frames_11, x_frames_01 + x_frames_10, ("X", "X")))
    recovered_zz_frames_and_orientations = set(search(zero_frames_11, z_frames_01 + z_frames_10, ("Z", "Z")))
    
    recovered_frames_and_orientations = set(list(recovered_z_frames_and_orientations) + list(recovered_x_frames_and_orientations) + list(recovered_xx_frames_and_orientations) + list(recovered_zz_frames_and_orientations))
    
    recovered_frames = [ el[0] for el in recovered_frames_and_orientations ]
    orientations = { el[0]: el[1] for el in recovered_frames_and_orientations }
    
    recovered_zero_frames_and_orientations = set(zero_search(recovered_frames, orientations, zero_frames_00 + zero_frames_11))
    recovered_zero_frames = [ el[0] for el in recovered_zero_frames_and_orientations ]
    zero_frames_orientations = { el[0]: el[1] for el in recovered_zero_frames_and_orientations }
    
    for i in range(len(usable_frames)):
        if usable_frames[i] in recovered_frames:
            key_recovered[i] = MATCHING_RESULTS[orientations[usable_frames[i]]]
        elif usable_frames[i] in recovered_zero_frames:
            key_recovered[i] = MATCHING_RESULTS[zero_frames_orientations[usable_frames[i]]]
        else:
            continue
            
    if DEBUG:
        print(f"Recovered '11' frames: {orientations}")
        print(f"Recovered '00' frames: {zero_frames_orientations}")
    
    return ''.join(key_recovered)
                
            
    