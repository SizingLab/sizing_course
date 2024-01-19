import openmdao.api as om
import numpy as np


class Battery(om.ExplicitComponent):
    def setup(self):
        self.add_input("k_mb", val=np.nan)
        self.add_input("M_pay", val=np.nan, units="kg")
        self.add_input("E_bat_ref", val=np.nan, units="J")
        self.add_input("M_bat_ref", val=np.nan, units="kg")
        self.add_input("U_bat", val=np.nan, units="V")
        self.add_input("I_bat_max_ref", val=np.nan, units="A")
        self.add_input("C_bat_ref", val=np.nan, units="A*s")
        self.add_input("P_el_mot_hov", val=np.nan, units="W")
        self.add_input("N_pro", val=np.nan)
        self.add_output("M_bat", units="kg")
        self.add_output("E_bat", units="J")
        self.add_output("C_bat", units="A*s")
        self.add_output("I_bat_max", units="A")
        self.add_output("P_bat_max", units="W")
        self.add_output("I_bat_hov", units="A")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        k_mb = inputs["k_mb"]
        M_pay = inputs["M_pay"]
        E_bat_ref = inputs["E_bat_ref"]
        M_bat_ref = inputs["M_bat_ref"]
        U_bat = inputs["U_bat"]
        I_bat_max_ref = inputs["I_bat_max_ref"]
        C_bat_ref = inputs["C_bat_ref"]
        P_el_mot_hov = inputs["P_el_mot_hov"]
        N_pro = inputs["N_pro"]

        # Energy selection with payload mass
        M_bat = k_mb * M_pay  # [kg] Battery mass
        E_bat = (
            E_bat_ref * M_bat / M_bat_ref * 0.8
        )  # [J] Energy  of the battery (.8 coefficient because 80% use only of the total capacity)

        # Estimation models
        C_bat = E_bat / U_bat  # [A*s] Capacity  of the battery
        I_bat_max = I_bat_max_ref * (C_bat / C_bat_ref)  # [A] Max discharge current
        P_bat_max = U_bat * I_bat_max  # [W] Max power

        # Performance in hover
        I_bat_hov = (P_el_mot_hov * N_pro) / 0.95 / U_bat  # [A] Current of the battery

        outputs["M_bat"] = M_bat
        outputs["E_bat"] = E_bat
        outputs["C_bat"] = C_bat
        outputs["I_bat_max"] = I_bat_max
        outputs["P_bat_max"] = P_bat_max
        outputs["I_bat_hov"] = I_bat_hov
