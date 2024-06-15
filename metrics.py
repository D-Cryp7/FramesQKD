def key_recovery(execute_qkd, Alice, Bob, pairs, Attack, dim, VALID_SS, DEBUG_QKD = False, depolarize_probability = 0, DEBUG_ATCK = False):
    public, private = execute_qkd(Alice, Bob, pairs, DEBUG_QKD, depolarize_probability)
    
    if not public and not private: return None 
    
    double_matchings, usable_frames, sifting_string, measured_string = public
    _, alice_key, bob_key = private

    SS = [ f"{sifting_string[i]},{measured_string[i]}" for i in range(len(sifting_string)) ]
    
    key_recovered = Attack(usable_frames, SS, DEBUG_ATCK)
    
    private_key_blocks = [ bob_key[i : i + dim] for i in range(0, len(bob_key), dim)  ]
    key_recovered_blocks = [ key_recovered[i : i + dim] for i in range(0, len(key_recovered), dim)  ]
    
    key_blocks = []
    key_recovered = []
    
    SS_LEFT = []
    for i in range(len(SS)):
        if SS[i] in VALID_SS:
            key_blocks.append(private_key_blocks[i])
            key_recovered.append(key_recovered_blocks[i])
            if key_recovered_blocks[i] == " " * dim:
                SS_LEFT.append(SS[i])
        else:
            continue
    
    if not key_blocks: return None
    
    bits_recovered = 0
    for x, y in zip(key_blocks, key_recovered):
        if x != y and y != " " * dim:
            print(x, y)
        elif x == y:
            bits_recovered += dim

    return {
        "double_matchings": double_matchings,
        "bits_recovered": bits_recovered,
        "bits": dim * len(key_blocks),
        "%": bits_recovered / (dim * len(key_blocks)),
        "SS_left": SS_LEFT
    }