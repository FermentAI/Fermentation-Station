EQUATIONS = dict(
    PRES = 'dP = -F*P/V + self.Rp(X,S)/Yxs'
    CONC = 'dC = (q/V)*(Cf - C) - self.k(T)*C',
    TEMP = 'dT = (q/V)*(Tf - T) + (-dHr/rho/Cp)*self.k(T)*C + (UA/V/rho/Cp)*(Tc - T)',
    TCRIT = 'dTc = (qc/Vc)*(Tc0 - Tc) + (UA/Vc/rho/Cp)*(T - Tc)',

)
