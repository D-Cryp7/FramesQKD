from random import choice

class Alice:
    def __init__(self, bits_generator, basis_generator):
        self.bits = bits_generator()
        self.basis = basis_generator()
        self.shared_secret = ""
        self.INFO = []
        
    def generate_states_data(self, results):
        self.states_data = {}
        for i in range(len(results)):
            self.states_data[i] = results[i] + self.basis[i].lower()
    
    def is_f1_frame(self, frame):
        row1, row2 = frame[0], frame[1]
        if (self.states_data[row1[0]] == "0x") and (self.states_data[row1[1]] == "1z") and (self.states_data[row2[0]] == "1x") and (self.states_data[row2[1]] == "0z"):
            return True
        else:
            return False
        
    def is_f5_frame(self, frame):
        row1, row2 = frame[0], frame[1]
        if (self.states_data[row1[0]] == "1x") and (self.states_data[row1[1]] == "0z") and (self.states_data[row2[0]] == "0x") and (self.states_data[row2[1]] == "1z"):
            return True
        else:
            return False
        
    def search_in_L_and_get_secret_bit(self, test_frame, L1, L2):
        # if test_frame is in L1
        if (test_frame in L1) or (test_frame[::-1] in L1):
            return 1
        # if test_frame is in L2
        elif (test_frame in L2) or (test_frame[::-1] in L2):
            return 0
        
    def calculate_bob_basis(self, L1, L2):
        shared_secret = [-1] * len(L1)
        # find f1 and f5 frames
        f1 = []
        f5 = []
        for i in range(len(L1)):
            if self.is_f1_frame(L1[i]):
                f1.append(L1[i])
                shared_secret[i] = 0
            elif self.is_f5_frame(L1[i]):
                f5.append(L1[i])
                shared_secret[i] = 1
        
        if L1:
            self.INFO.append((len(f1) + len(f5), len(L1)))
        
        if f1:
            pivot = choice(f1)[0]
        elif f5:
            pivot = choice(f5)[1]
        else:
            return False

        
        for i in range(len(L1)):
            if (L1[i] not in f1) and (L1[i] not in f5):
                if pivot != L1[i][0]:
                    test_frame = (pivot, L1[i][0])
                    shared_secret[i] = self.search_in_L_and_get_secret_bit(test_frame, L1, L2)
                else:
                    # if pivot == L1[i][0], we can conclude instantly? YES!
                    shared_secret[i] = 0

        self.shared_secret += "".join([ str(bit) for bit in shared_secret])
        return True