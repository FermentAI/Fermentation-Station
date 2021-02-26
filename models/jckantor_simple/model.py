from pyfoomb import BioprocessModel
import numpy as np

# Defines the model class
class Model(BioprocessModel):

    def rhs(self, t, y):
        # Unpacks the state vector. The states are alphabetically ordered.
        P,S,V,X = y

        # Unpacks the model parameters.
        Yxs = self.model_parameters['Yxs']
        Sf = self.model_parameters['Sf']
        F = self.model_parameters['F']

        # Defines the derivatives.
        dP = -F*P/V + self.Rp(X,S)
        dS = F*(Sf-S)/V - self.Rg(X,S)/Yxs
        dV = F
        dX = -F*X/V + self.Rg(X,S)

        # Returns the derivative as list (or numpy array).
        # The order corresponds to the state vector.
        return [dP,dS,dV,dX]
    
    # Monoid expression
    def mu(self,S):
        mu_max = self.model_parameters['mu_max']
        Ks = self.model_parameters['Ks']
        return mu_max*S/(Ks + S)
    
    # Cell growth rate
    def Rg(self, X, S):
        return self.mu(S)*X

    # Cell production rate
    def Rp(self, X, S):
        Ypx = self.model_parameters['Ypx']
        return Ypx*self.Rg(X,S)
    