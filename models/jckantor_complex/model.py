from pyfoomb import BioprocessModel
import numpy as np

# Defines the model class
class Model(BioprocessModel):

    def rhs(self, t, y):
        # Unpacks the state vector. The states are alphabetically ordered.
        C,T,Tc = y

        # Unpacks the model parameters.
        q = self.model_parameters['q']
        Cf = self.model_parameters['Cf']
        Tf = self.model_parameters['Tf']
        Tc0 = self.initial_values['Tc0']
        qc = self.model_parameters['qc']
        Vc = self.model_parameters['Vc']

        
        V = self.model_parameters['V']
        rho = self.model_parameters['rho']
        Cp = self.model_parameters['Cp']
        dHr = self.model_parameters['dHr']
        UA = self.model_parameters['UA']

        # Defines the derivatives.
        dC = (q/V)*(Cf - C) - self.k(T)*C
        dT = (q/V)*(Tf - T) + (-dHr/rho/Cp)*self.k(T)*C + (UA/V/rho/Cp)*(Tc - T)
        dTc = (qc/Vc)*(Tc0 - Tc) + (UA/Vc/rho/Cp)*(T - Tc)

        # Returns the derivative as list (or numpy array).
        # The order corresponds to the state vector.
        return [dC, dT, dTc]
    
    # Arrhenius rate expression
    def k(self,T):
        Ea = self.model_parameters['Ea']
        R = self.model_parameters['R']
        k0 = self.model_parameters['k0']
        return k0*np.exp(-Ea/R/T)
    