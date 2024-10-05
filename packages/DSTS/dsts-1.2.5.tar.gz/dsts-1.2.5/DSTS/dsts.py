import numpy as np
from DSTS.calibration import *
from DSTS.mixup import *
from DSTS.y1_generation import *
from DSTS.utils import NNsorting

class dsts:
    def __init__(self, method, feature_match = False):
        """
        Initialize the dsts class with the specified method.
        
        Parameters:
        method (str): The method to use for data synthesis. Possible values are 'sorting', 'condGMM', 'LR'.
        feature_match (bool): Whether to match feature order using NN.
        """
        self.method = method
        self.feature_match = feature_match


    def fit(self, data):
        try:
            self.data = np.array(data)
        except :
            raise ValueError("Data cannot be converted to numpy ndarray")
        self.data = self.__test(self.data)


    def generate(self, ite=3, tot_iter=4, aug=5, n_comp=2) -> np.ndarray:
        """
        Synthesizes a new time series using DS2 algorithms.

        Parameters:
        ite (int, optional): The number of calibration iterations for each timestamp. 
                             Defaults to 3. 
        tot_iter (int, optional): The number of calibration loops for whole time series. 
                                  Default to 4.
        aug (int): The multiplier for the size of the synthesized data relative to the original data. 
                   Defaults to 5.
        n_comp (int, optional): The number of mixture components in GMM. 
                                Default is 2.
        
        Returns:
        np.ndarray: The synthesized data array of shape (size * aug, length).

        """
        size = self.data.shape[0]
        length = self.data.shape[1]
        k = aug+2

        # handle sorting method
        if self.method=='sorting':
            sort = True
        else:
            sort = False

        rstar = make_rstar(self.data, k, sort)    
        
        # method to use for generating y1
        if self.method=='sorting':
            y1 = dt_draw_y1(self.data, rstar, sort=True)

        elif self.method=='condGMM':
            sort = False
            y1 = condGMM_draw_y1(self.data, rstar, n_comp, sort)

        elif self.method=='LR':
            sort=False
            y1 = lr_draw_y1(self.data, rstar, sort)

        synth = np.ones((size*k,length))
        synth[:,0] = y1 
        synth[:,1:] = (y1*rstar.T).T
        calib_data = calibration(self.data, synth, ite, tot_iter, aug)
        final_data = calib_data
        final_data[:,0]-= self.epsilon

        if self.feature_match ==True:
            sorted_data = NNsorting(aug, np.reshape(calib_data, (aug, size, length)), self.data)
            sorted_data[:,0] -= self.epsilon
            final_data = sorted_data

        return final_data
       

    def __test(self, data):
        # Check if data contains any NaN values
        if np.isnan(data).any():
            raise ValueError("Your data must not contain any NaN values.")
        
        # Check if first timestamp contains any non-positive values
        self.epsilon = 0
        if np.any(data[:,0]<=0):
            print("WARNING! First timestamp of your data contains non-positive values. Epsilon added.")
            self.epsilon=np.abs(data[:,0].min())+1
            data[:,0] = data[:,0]+self.epsilon

        return data
        