import numpy as np
import unittest 

class KF:
    def __init__(self, initial_x, initial_v):
        # Mean state of Gaussian random variable
        self.x = np.array([initial_x, initial_v])
        
        # covariance of Gaussian random variable
        self.P = np.eye(2)