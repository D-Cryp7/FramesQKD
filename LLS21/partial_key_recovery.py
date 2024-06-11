from helpers import MATCHING_RESULTS
from itertools import product, combinations
from copy import deepcopy

FRAMES_STRUCTURES = {
    "111,110": [("X", "Z", "Z"), ("Z", "X", "X")],
    "111,011": [("Z", "Z", "X"), ("X", "X", "Z")],
    "110,110": [("X", "Z", "X"), ("Z", "X", "Z")],
    "110,011": [("X", "Z", "X"), ("Z", "X", "Z")],
    "101,111": [("Z", "Z", "X"), ("X", "Z", "Z")],
    "101,100": [("X", "X", "Z"), ("X", "Z", "Z")],
    "101,001": [("Z", "X", "X"), ("Z", "Z", "X")],
    "100,111": [("X", "X", "X"), ("Z", "X", "Z")],
    "100,100": [("X", "X", "X"), ("X", "Z", "X")],
    "100,010": [("X", "X", "X"), ("Z", "X", "Z")],
    "100,001": [("X", "X", "X"), ("X", "Z", "X")],
    "011,111": [("X", "X", "Z"), ("Z", "X", "X")],
    "011,100": [("Z", "X", "X"), ("Z", "Z", "X")],
    "011,010": [("X", "Z", "Z"), ("Z", "Z", "X")],
    "011,001": [("X", "Z", "Z"), ("X", "X", "Z")],
    "010,111": [("X", "Z", "X"), ("Z", "Z", "Z")],
    "010,100": [("Z", "X", "Z"), ("Z", "Z", "Z")],
    "010,010": [("Z", "Z", "Z"), ("X", "Z", "X")],
    "010,001": [("Z", "Z", "Z"), ("Z", "X", "Z")],
    "001,110": [("Z", "Z", "X"), ("X", "X", "Z")],
    "000,110": [("Z", "Z", "Z"), ("X", "X", "X")],
    "000,011": [("Z", "Z", "Z"), ("X", "X", "X")]
}

class RECOVERED_FRAMES:
    def __init__(self, frames):
        self.recovered_frames_and_orientations = {}
        self.recovered_frames = {}
        self.frames = frames

    def search_2x2_block(self, SS1, SS2, OP1, OP2, OT1, OT2, MODE = "IDLE-MOVE"):
        # Searches for a complete 2x2 frame inside a 3x2 one
        # SS1: Pivot Frames SS
        # SS2: Target Frames SS
        # OP1: Orientation 1 por Pivot Frame
        # OP2: Orientation 2 for Pivot Frame
        
        # OT1: Orientation 1 for Target Frame
        # OT2: Orientation 2 for Target Frame
    
        # MODE: Search mode

        if SS1 not in self.recovered_frames_and_orientations.keys():
            self.recovered_frames_and_orientations[SS1] = set()
            self.recovered_frames[SS1] = set()

        if SS2 not in self.recovered_frames_and_orientations.keys():
            self.recovered_frames_and_orientations[SS2] = set()
            self.recovered_frames[SS2] = set()

        if SS1 not in self.frames.keys() or SS2 not in self.frames.keys():
            return
            
        PF = self.frames[SS1]
        TF = self.frames[SS2]

        for s, f in product(PF, TF):
            conditions = [False, False]
            
            if MODE == "IDLE-MOVE":
                if   s[:2] == f[:2] and OP1 and OT1: conditions[0] = True
                elif s[:2] == f[1:] and OP2 and OT2: conditions[1] = True

            elif MODE == "IDLE_DOWN-MOVE":
                if   (s[1:] == f[:2] or s[1:] == f[:2][::-1]) and OP1 and OT1: conditions[0] = True
                elif (s[1:] == f[1:] or s[1:] == f[1:][::-1]) and OP2 and OT2: conditions[1] = True

            elif MODE == "MOVE-IDLE":
                if   s[:2] == f[1:] and OP1 and OT1: conditions[0] = True
                elif s[1:] == f[1:] and OP2 and OT2: conditions[1] = True

            elif MODE == "MOVE-MOVE":
                if   (s[:2] == f[:2]) or (s[:2] == f[:2][::-1]) and OP1 and OT1: conditions[0] = True
                elif (s[1:] == f[1:]) or (s[1:] == f[1:][::-1]) and OP2 and OT2: conditions[1] = True

            elif MODE == "IDLE-SPLIT":
                if   (s[:2] == f[::2]) or (s[:2] == f[::2][::-1]) and OP1 and OT1: conditions[0] = True


            if conditions[0]: 
                self.recovered_frames_and_orientations[SS1].add((s, OP1))
                self.recovered_frames_and_orientations[SS2].add((f, OT1))
                self.recovered_frames[SS1].add(s)
                self.recovered_frames[SS2].add(f)

            elif conditions[1]:
                self.recovered_frames_and_orientations[SS1].add((s, OP2))
                self.recovered_frames_and_orientations[SS2].add((f, OT2))
                self.recovered_frames[SS1].add(s)
                self.recovered_frames[SS2].add(f)

    def recover_from_known_frame(self):
        known_SS = self.recovered_frames_and_orientations.keys()

        recovered_frames_and_orientations = deepcopy(self.recovered_frames_and_orientations)
        recovered_frames = deepcopy(self.recovered_frames)
        
        for SS in known_SS:
            for known_frame_and_orientation in self.recovered_frames_and_orientations[SS]:
                for ss, frames in self.frames.items():
                    for frame in frames:
                        if ss not in self.recovered_frames.keys() or ss not in FRAMES_STRUCTURES.keys():
                            continue
                        elif frame not in self.recovered_frames[ss]:
                            super_frame = known_frame_and_orientation[0] + frame
                            index = [i % 3 for i in range(6) if super_frame.count(super_frame[i]) > 1]
                            orientations = FRAMES_STRUCTURES[ss]

                            if len(index) == 2:
                                if known_frame_and_orientation[1][index[0]] == orientations[0][index[1]] and orientations[0][index[1]] != orientations[1][index[1]]:
                                    recovered_frames_and_orientations[ss].add((frame, orientations[0]))
                                    recovered_frames[ss].add(frame)

                                elif known_frame_and_orientation[1][index[0]] == orientations[1][index[1]] and orientations[0][index[1]] != orientations[1][index[1]]:
                                    recovered_frames_and_orientations[ss].add((frame, orientations[1]))
                                    recovered_frames[ss].add(frame)

                            elif len(index) == 4:
                                if known_frame_and_orientation[1][index[0]] == orientations[0][index[2]] and orientations[0][index[2]] != orientations[1][index[2]]:
                                    recovered_frames_and_orientations[ss].add((frame, orientations[0]))
                                    recovered_frames[ss].add(frame)

                                elif known_frame_and_orientation[1][index[0]] == orientations[1][index[2]] and orientations[0][index[2]] != orientations[1][index[2]]:
                                    recovered_frames_and_orientations[ss].add((frame, orientations[1]))
                                    recovered_frames[ss].add(frame)

                                elif known_frame_and_orientation[1][index[1]] == orientations[0][index[3]] and orientations[0][index[3]] != orientations[1][index[3]]:
                                    recovered_frames_and_orientations[ss].add((frame, orientations[0]))
                                    recovered_frames[ss].add(frame)

                                elif known_frame_and_orientation[1][index[1]] == orientations[1][index[3]] and orientations[0][index[3]] != orientations[1][index[3]]:
                                    recovered_frames_and_orientations[ss].add((frame, orientations[1]))
                                    recovered_frames[ss].add(frame)



        self.recovered_frames_and_orientations = recovered_frames_and_orientations
        self.recovered_frames = recovered_frames

    def to_list(self):
        recovered_frames_and_orientations = []
        for set_ in self.recovered_frames_and_orientations.values():
            set_ = list(set_)
            for el in set_:
                recovered_frames_and_orientations.append(el)
        return recovered_frames_and_orientations
             

def attack(usable_frames, sifting_string, measured_string, DEBUG = True):
    assert len(usable_frames) == len(sifting_string), "Each frame must have its associated sifting bits"
    assert len(usable_frames) == len(measured_string), "Each frame must have its associated measured bits"

    SS = [ f"{sifting_string[i]},{measured_string[i]}" for i in range(len(usable_frames)) ]
    
    key_recovered = ["   "] * len(usable_frames)

    # ---------- Target frames ----------
    frames = {}
    
    for i in range(len(usable_frames)):
        if SS[i] not in frames.keys():
            frames[SS[i]] = []

        frames[SS[i]].append(usable_frames[i])
    # -----------------------------------

    rec = RECOVERED_FRAMES(frames)
    
    # -------------------------------------------- Recovered frames with 111,110 as Pivot --------------------------------------------
    rec.search_2x2_block("111,110", "101,111", ("X", "Z", "Z"), ("Z", "X", "X"), ("X", "Z", "Z"), ("Z", "Z", "X"))
    rec.search_2x2_block("101,100", "111,110", None, ("X", "X", "Z"), None, ("Z", "X", "X"))
    rec.search_2x2_block("111,110", "101,010", ("Z", "X", "X"), ("Z", "X", "X"), ("X", "X", "Z"), ("Z", "X", "X"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "101,001", None, ("Z", "X", "X"), None, ("Z", "X", "X"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "010,001", None, ("X", "Z", "Z"), None, ("Z", "Z", "Z"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "010,010", ("X", "Z", "Z"), ("X", "Z", "Z"), ("Z", "Z", "Z"), ("Z", "Z", "Z"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "010,100", ("X", "Z", "Z"), None, ("Z", "Z", "Z"), None, "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "011,001", None, ("X", "Z", "Z"), None, ("X", "Z", "Z"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "011,010", ("X", "Z", "Z"), ("X", "Z", "Z"), ("Z", "Z", "X"), ("X", "Z", "Z"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "011,100", ("X", "Z", "Z"), None, ("Z", "Z", "X"), None, "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "100,001", None, ("Z", "X", "X"), None, ("X", "X", "X"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "100,010", ("Z", "X", "X"), ("Z", "X", "X"), ("X", "X", "X"), ("X", "X", "X"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "100,100", ("Z", "X", "X"), None, ("X", "X", "X"), None, "IDLE_DOWN-MOVE")
    rec.search_2x2_block("111,110", "100,111", ("Z", "X", "X"), ("X", "Z", "Z"), ("Z", "X", "Z"), ("Z", "X", "Z"))
    rec.search_2x2_block("111,110", "011,111", ("Z", "X", "X"), ("X", "Z", "Z"), ("Z", "X", "X"), ("X", "X", "Z"))
    rec.search_2x2_block("111,110", "010,111", ("X", "Z", "Z"), ("Z", "X", "X"), ("X", "Z", "X"), ("X", "Z", "X"))
    # --------------------------------------------------------------------------------------------------------------------------------

    # -------------------------------------------- Recovered frames with 101,111 as Pivot --------------------------------------------
    rec.search_2x2_block("101,111", "001,110", ("Z", "Z", "X"), None, ("Z", "Z", "X"), None)
    rec.search_2x2_block("101,111", "000,011", None, ("Z", "Z", "X"), None, ("Z", "Z", "Z"))
    # rec.search_2x2_block("101,111", "000,101", ("Z", "Z", "X"), None, ("Z", "X", "Z"), None, "IDLE-SPLIT")
    rec.search_2x2_block("101,111", "001,011", ("Z", "Z", "X"), ("X", "Z", "Z"), ("X", "Z", "Z"), ("X", "Z", "Z"), "MOVE-IDLE")
    # rec.search_2x2_block("101,111", "010,111", None, ("Z", "Z", "X"), None, ("Z", "Z", "Z"))
    rec.search_2x2_block("000,110", "101,111", ("Z", "Z", "Z"), ("Z", "Z", "Z"), ("Z", "Z", "X"), ("X", "Z", "Z"))
    rec.search_2x2_block("000,110", "101,111", ("Z", "Z", "Z"), ("Z", "Z", "Z"), ("Z", "Z", "X"), ("X", "Z", "Z"))
    # --------------------------------------------------------------------------------------------------------------------------------
    
    # -------------------------------------------- Recovered frames with 010,001 as Pivot --------------------------------------------
    rec.search_2x2_block("001,011", "010,001", None, ("X", "Z", "Z"), None, ("Z", "X", "Z"))
    rec.search_2x2_block("010,001", "001,110", None, ("Z", "X", "Z"), None, ("Z", "Z", "X"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("010,010", "010,001", ("X", "Z", "X"), None, ("Z", "X", "Z"), None)
    rec.search_2x2_block("010,001", "100,100", None, ("Z", "X", "Z"), None, ("X", "Z", "X"))
    rec.search_2x2_block("010,001", "110,011", ("Z", "X", "Z"), None, ("X", "Z", "X"), None, "IDLE_DOWN-MOVE")
    rec.search_2x2_block("010,001", "110,110", None, ("Z", "X", "Z"), None, ("X", "Z", "X"), "IDLE_DOWN-MOVE")
    rec.search_2x2_block("010,001", "111,011", ("Z", "Z", "Z"), None, ("Z", "Z", "X"), None, "IDLE_DOWN-MOVE")
    # --------------------------------------------------------------------------------------------------------------------------------

    rec.recover_from_known_frame()
    
    recovered_frames_and_orientations = rec.to_list()
    recovered_frames = [ el[0] for el in recovered_frames_and_orientations ]
    orientations = { el[0]: el[1] for el in recovered_frames_and_orientations }
    
    for i in range(len(usable_frames)):
        if usable_frames[i] in recovered_frames:
            key_recovered[i] = MATCHING_RESULTS[orientations[usable_frames[i]]]
        else:
            continue
            
    if DEBUG:
        print(f"Recovered '11' frames: {orientations}")
        # print(f"Recovered '00' frames: {zero_frames_orientations}")
    
    return ''.join(key_recovered), rec