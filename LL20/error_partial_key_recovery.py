from helpers import MATCHING_RESULTS
from itertools import product

def search_2x2_block(F1, F2, O1, OT1, O2, OT2, inverted = False):
    recovered_frames = []
    for s, f in product(F1, F2):
        if inverted: f = f[::-1]

        if s[:2] == f[:2] and O1 and O2:
            recovered_frames.append((s, O1))
            recovered_frames.append((f, O2))
            
        elif s[:2] == f[1:] and OT1 and OT2:
            recovered_frames.append((s, OT1))
            recovered_frames.append((f, OT2))
    
    return recovered_frames

def attack(usable_frames, sifting_string, measured_string, DEBUG = True):
    assert len(usable_frames) == len(sifting_string), "Each frame must have its associated sifting bits"
    assert len(usable_frames) == len(measured_string), "Each frame must have its associated measured bits"
    
    key_recovered = ["   "] * len(usable_frames)
    
    frames_111_110 = []
    frames_101_111 = []
    frames_100_111 = []
    frames_011_111 = []
    frames_010_111 = []
    frames_001_110 = []
    frames_001_011 = []

    # 101_111 - 001_011
    # 101_111 - 000_110
    
    # fill lists
    for i in range(len(usable_frames)):
        if sifting_string[i] == "111" and measured_string[i] == "110": frames_111_110.append(usable_frames[i])
        elif sifting_string[i] == "101" and measured_string[i] == "111": frames_101_111.append(usable_frames[i])
        elif sifting_string[i] == "100" and measured_string[i] == "111": frames_100_111.append(usable_frames[i])
        elif sifting_string[i] == "011" and measured_string[i] == "111": frames_011_111.append(usable_frames[i])
        elif sifting_string[i] == "010" and measured_string[i] == "111": frames_010_111.append(usable_frames[i])
        elif sifting_string[i] == "001" and measured_string[i] == "110": frames_001_110.append(usable_frames[i])
        else: continue
        
    
    recovered_frames_and_orientations = list(set(search_2x2_block(frames_111_110, frames_101_111, ("X", "Z", "Z"), ("Z", "X", "X"), ("X", "Z", "Z"), ("Z", "Z", "X"))))
    recovered_frames_and_orientations += list(set(search_2x2_block(frames_111_110, frames_100_111, ("Z", "X", "X"), ("X", "Z", "Z"), ("Z", "X", "Z"), ("Z", "X", "Z"))))
    recovered_frames_and_orientations += list(set(search_2x2_block(frames_111_110, frames_011_111, ("Z", "X", "X"), ("X", "Z", "Z"), ("Z", "X", "X"), ("X", "X", "Z"))))
    recovered_frames_and_orientations += list(set(search_2x2_block(frames_111_110, frames_010_111, ("Z", "X", "X"), ("X", "Z", "Z"), ("X", "Z", "X"), ("X", "Z", "X"))))
    
    recovered_frames_and_orientations += list(set(search_2x2_block(frames_101_111, frames_001_110, ("Z", "Z", "X"), None, ("Z", "Z", "X"), None)))

    recovered_frames_and_orientations = set(recovered_frames_and_orientations)
    
    recovered_frames = [ el[0] for el in recovered_frames_and_orientations ]
    orientations = { el[0]: el[1] for el in recovered_frames_and_orientations }
    
    # recovered_zero_frames_and_orientations = set(zero_search(recovered_frames, orientations, zero_frames))
    # recovered_zero_frames = [ el[0] for el in recovered_zero_frames_and_orientations ]
    # zero_frames_orientations = { el[0]: el[1] for el in recovered_zero_frames_and_orientations }
    
    for i in range(len(usable_frames)):
        if usable_frames[i] in recovered_frames:
            key_recovered[i] = MATCHING_RESULTS[orientations[usable_frames[i]]]
        else:
            continue
            
    if DEBUG:
        print(f"Recovered '11' frames: {orientations}")
        # print(f"Recovered '00' frames: {zero_frames_orientations}")
    
    return ''.join(key_recovered)