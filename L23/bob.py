from itertools import combinations, product
from secrets import randbits
from random import shuffle

class Bob:
    def __init__(self, generator):
        self.basis = generator()
        self.shared_secret = []
        
    def basis_filter_and_pairs(self, ones, basis):
        # get only the states that where measured in a certain basis
        filtered = list(filter(lambda x: x[1] == basis, ones))
        return list(combinations([ filtered[i][0] for i in range(len(filtered)) ], 2))
        
    def product_filter(self, product):
        return list(filter(lambda x: x[0] != x[1], product))
    
    def generate_L1_and_L2(self, results):
        # get only "1" results
        ones = [ (i, self.basis[i]) for i in range(len(results)) if results[i] == "1" ]
        # get double matchings in Z basis
        Z = self.basis_filter_and_pairs(ones, "Z")
        # get double matchings in X basis
        X = self.basis_filter_and_pairs(ones, "X")
        
        # construct the L1 matrix, grouping two double matchings in different basis
        L1_INFO = []
        for z, x in product(Z, X):
            if randbits(1):
                L1_INFO.append( (x, z, 1) )
            else:
                L1_INFO.append( (z, x, 0) )
        
        shuffle(L1_INFO)
        
        shared_secret = [ FRAME_INFO[2] for FRAME_INFO in L1_INFO ]
        self.shared_secret.append("".join([ str(bit) for bit in shared_secret]))
        
        L1 = [ ( FRAME_INFO[0], FRAME_INFO[1] ) for FRAME_INFO in L1_INFO ]
        
        # construct the L2 matrix
        L2 = self.product_filter(product(Z, Z)) + self.product_filter(product(X, X))
        
        shuffle(L2)

        return L1, L2