from random import choice

def search_in_L_and_get_secret_bit(test_frame, L1, L2):
    # if test_frame is in L1
    if (test_frame in L1) or (test_frame[::-1] in L1):
        return 1
    # if test_frame is in L2
    elif (test_frame in L2) or (test_frame[::-1] in L2):
        return 0
    
def attack(L1, L2):
    shared_secret = [-1] * len(L1)
    pivot = choice(L1)[0]
    
    for i in range(len(L1)):
        if pivot != L1[i][0]:
            test_frame = (pivot, L1[i][0])
            shared_secret[i] = search_in_L_and_get_secret_bit(test_frame, L1, L2)
        else:
            # if pivot == L1[i][0], we can conclude instantly? YES!
            shared_secret[i] = 0

    shared_secret = "".join([ str(bit) for bit in shared_secret])
    return shared_secret