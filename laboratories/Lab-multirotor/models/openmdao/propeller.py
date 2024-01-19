import openmdao.api as om
import numpy as np


class Propeller(om.ExplicitComponent):
    def setup(self):
        self.add_input("beta_pro", val=np.nan)
        self.add_input("F_pro_to", val=np.nan, units="N")
        self.add_input("rho_air", val=np.nan, units="kg/m**3")
        self.add_input("ND_max", val=np.nan, units="m/s")
        self.add_input("k_ND", val=np.nan)
        self.add_input("M_pro_ref", val=np.nan, units="kg")
        self.add_input("D_pro_ref", val=np.nan, units="m")
        self.add_input("F_pro_hov", val=np.nan, units="N")

        self.add_output("C_t")
        self.add_output("C_p")
        self.add_output("D_pro", units="m")
        self.add_output("n_pro_to", units="Hz")
        self.add_output("Omega_pro_to", units="rad/s")
        self.add_output("M_pro", units="kg")
        self.add_output("P_pro_to", units="W")
        self.add_output("T_pro_to", units="N*m")
        self.add_output("n_pro_hov", units="Hz")
        self.add_output("Omega_pro_hov", units="rad/s")
        self.add_output("P_pro_hov", units="W")
        self.add_output("T_pro_hov", units="N*m")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        beta_pro = inputs["beta_pro"]
        F_pro_to = inputs["F_pro_to"]
        rho_air = inputs["rho_air"]
        ND_max = inputs["ND_max"]
        k_ND = inputs["k_ND"]
        M_pro_ref = inputs["M_pro_ref"]
        D_pro_ref = inputs["D_pro_ref"]
        F_pro_hov = inputs["F_pro_hov"]

        C_t = 4.27e-02 + 1.44e-01 * beta_pro  # Thrust coef with T=C_T.rho.n^2.D^4
        C_p = -1.48e-03 + 9.72e-02 * beta_pro  # Power coef with P=C_p.rho.n^3.D^5

        # Propeller selection with take-off scenario
        D_pro = (
            F_pro_to / (C_t * rho_air * (ND_max / k_ND) ** 2.0)
        ) ** 0.5  # [m] Propeller diameter
        n_pro_to = ND_max / k_ND / D_pro  # [Hz] Propeller speed
        Omega_pro_to = n_pro_to * 2 * np.pi  # [rad/s] Propeller speed

        # Estimation model for mass
        M_pro = M_pro_ref * (D_pro / D_pro_ref) ** 2.0  # [kg] Propeller mass

        # Performance in various operating conditions
        # Take-off
        P_pro_to = C_p * rho_air * n_pro_to**3.0 * D_pro**5.0  # [W] Power per propeller
        T_pro_to = P_pro_to / Omega_pro_to  # [N*m] Propeller torque
        # Hover
        n_pro_hov = np.sqrt(F_pro_hov / (C_t * rho_air * D_pro**4.0))  # [Hz] hover speed
        Omega_pro_hov = n_pro_hov * 2.0 * np.pi  # [rad/s] Propeller speed
        P_pro_hov = C_p * rho_air * n_pro_hov**3.0 * D_pro**5.0  # [W] Power per propeller
        T_pro_hov = P_pro_hov / Omega_pro_hov  # [N*m] Propeller torque

        outputs["C_t"] = C_t
        outputs["C_p"] = C_p
        outputs["D_pro"] = D_pro
        outputs["n_pro_to"] = n_pro_to
        outputs["Omega_pro_to"] = Omega_pro_to
        outputs["M_pro"] = M_pro
        outputs["P_pro_to"] = P_pro_to
        outputs["T_pro_to"] = T_pro_to
        outputs["n_pro_hov"] = n_pro_hov
        outputs["Omega_pro_hov"] = Omega_pro_hov
        outputs["P_pro_hov"] = P_pro_hov
        outputs["T_pro_hov"] = T_pro_hov
