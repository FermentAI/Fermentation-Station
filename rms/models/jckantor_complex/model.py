import rms.engine
from rms.engine import Subroutine
from pyfoomb import BioprocessModel
import numpy as np

class MyModel(BioprocessModel):
    """
    Defines the model class. Always named MyModel. Always inherits from BioprocessModel
    
    Must define rhs(self,t,y) as a system of ODEs.
    """
    def rhs(self, t, y):
        """
        An exothermic stirred tank reactor where the objective is to control the reactor temperature
        through manipulation of cooling water through the reactor cooling jacket.
        \n By Jeffrey Kantor
        \n https://jckantor.github.io/CBE30338/04.11-Implementing-PID-Control-in-Nonlinear-Simulations.html
    
        """
        # Unpacks the state vector. The states are alphabetically ordered.
        C,T,Tc = y

        # Unpacks the model parameters.
        # Here both manipualted variables and parameters are considered "model_parameters"

        q = self.model_parameters['q']
        Cf = self.model_parameters['Cf']
        Tf = self.model_parameters['Tf']
        Tcf = self.model_parameters['Tcf']
        qc = self.model_parameters['qc']
        Vc = self.model_parameters['Vc']

        
        V = self.model_parameters['V']
        rho = self.model_parameters['rho']
        Cp = self.model_parameters['Cp']
        dHr = self.model_parameters['dHr']
        UA = self.model_parameters['UA']

        # Defines the derivatives.
        dCdt = (q/V)*(Cf - C) - self.k(T)*C
        dTdt = (q/V)*(Tf - T) + (-dHr/rho/Cp)*self.k(T)*C + (UA/V/rho/Cp)*(Tc - T)
        dTcdt = (qc/Vc)*(Tcf - Tc) + (UA/Vc/rho/Cp)*(T - Tc)

        # Returns the derivative as list (or numpy array).
        # The order corresponds to the state vector.
        return [dCdt, dTdt, dTcdt]

    ###############################################
    """
    Other methods can also be defined
    """
    # Arrhenius rate expression
    def k(self,T):
        Ea = self.model_parameters['Ea']
        R = self.model_parameters['R']
        k0 = self.model_parameters['k0']
        return k0*np.exp(-Ea/R/T)
    


class MySubroutines(Subroutine):
    """
    Defines the subroutine class. Always named MySubroutines. Always inherits from Subroutine.

    The Subroutine class runs all its NOT underscored functions before iterating at every time step.
    """
    def _initialization(self):
        '''
        This will only be run once in the first integration iteration.
        Useful for initializing variables.
        '''
        # initialize errors for discrete time calculations
        self.qLog = []
        self.TLog = []

        eP_, _, eD_ = self._temperature_error()
        self._update_error([eP_,eD_,eD_])


    def temperature_pid_coolant_flowratea(self):
        '''
        Discrete time PID implementation
        '''
        dt = self.simulator_vars['dt']
        
        kp = self.subroutine_vars['kp']
        ki = self.subroutine_vars['ki']
        kd = self.subroutine_vars['kd']
        new_qc = self.model_parameters['qc']

        # calculate current error
        eP, eI, eD = self._temperature_error() 

        # calculate manipulated varibale based on error
        new_qc -= kp*(eP - self.eP_) + ki*dt*eI + kd*(eD - 2*self.eD_ + self.eD__)/dt

        # check for saturation
        new_qc = self._coolant_flowrate_saturation(new_qc)

        # update manipulated variable
        self.model_parameters['qc'] = new_qc
        self.qLog.append(new_qc)

        # update errors
        self._update_error([eP,eD,self.eD_]) 
        return True

    # other helper functions for Temperature PID
    def _update_error(self, new_error):
        self.eP_ = new_error[0]  
        self.eD_ = new_error[1] 
        self.eD__ = new_error[2]

    def _temperature_error(self):
        '''
        Reactor temperature error with setpoint weighting
        '''
        T = self.model_state['T']
        Tsp = self.subroutine_vars['Tsp']
        beta = self.subroutine_vars['beta']
        gamma = self.subroutine_vars['gamma']
        
        eP = beta*Tsp - T
        eI = Tsp - T
        eD = gamma*Tsp - T
        
        self.TLog.append(T)

        return eP,eI,eD

    def _coolant_flowrate_saturation(self, qc):
        '''
        Clamping of coolant flowrate
        '''
        qc_min = self.subroutine_vars['qc_min']
        qc_max = self.subroutine_vars['qc_max']

        return max(qc_min, min(qc_max,qc))
 
