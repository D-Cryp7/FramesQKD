def execute_qkd(Alice, Bob, pairs, DEBUG = True, depolarize_probability = 0):
    # Initialization
    alice = Alice(pairs)
    bob = Bob(depolarize_probability)
    
    # Send pairs
    pairs = alice.prepare()

    # Measure each pair and retrieve double matchings
    double_matchings = bob.measure(pairs)
    
    # Verify that there's double matchings
    if not len(double_matchings):
        print("Key exchange failed, there's no double matchings. Please, try again.")
        return (), ()
    
    # Compute usable frames for Bob
    usable_frames, usable_frames_types = alice.compute_usable_frames(double_matchings)
    
    # Veirfy that there's usable frames
    if not len(usable_frames):
        print("Key exchange failed, there's no usable frames. Please, try again.")
        return (), ()

    # Compute sifting string
    sifting_string = bob.compute_sifting_string(usable_frames)

    # Compute measured string
    measured_string = bob.compute_measured_string(usable_frames)

    # Bob computes secret key
    bob_key = bob.generate_shared_key(usable_frames)

    # Alice computes secret key
    alice_key = alice.generate_shared_key(usable_frames_types, sifting_string)
    
    if alice_key == bob_key:
        if DEBUG:
            print("Key exchange completed, here's the data:")
            print(f"Alice send pairs: {alice.pairs_data}")
            print(f"Bob send double matchings: {double_matchings}")
            print(f"Alice send usable frames: {usable_frames}")
            print(f"Bob send sifting string: {sifting_string}")
            print(f"Bob send measured string: {measured_string}")
            print(f"Bob shared key: {bob_key}")
            print(f"Alice shared key: {alice_key}")
    else:
        print("Key exchange failed, both keys are not equal. Please, try again.")

    return (double_matchings, usable_frames, sifting_string, measured_string), (alice.pairs_data, alice_key, bob_key)