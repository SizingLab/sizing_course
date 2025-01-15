import openmdao.api as om
import numpy as np


class ESC(om.ExplicitComponent):
    def setup(self):
        self.add_input("P_el_mot_to", val=np.nan, units="W")
        self.add_input("U_bat", val=np.nan, units="V")
        self.add_input("U_mot_to", val=np.nan, units="V")
        self.add_input("M_esc_ref", val=np.nan, units="kg")
        self.add_input("P_esc_ref", val=np.nan, units="W")

        self.add_output("P_esc", units="W")
        self.add_output("U_esc", units="V")
        self.add_output("M_esc", units="kg")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        P_el_mot_to = inputs["P_el_mot_to"]
        U_bat = inputs["U_bat"]
        U_mot_to = inputs["U_mot_to"]
        M_esc_ref = inputs["M_esc_ref"]
        P_esc_ref = inputs["P_esc_ref"]

        # Power selection with takeoff scenario
        P_esc = (
            P_el_mot_to * U_bat / U_mot_to
        )  # [W] power electronic power (corner power or apparent power)

        # Estimation models
        U_esc = 1.84 * P_esc**0.36  # [V] ESC voltage
        M_esc = M_esc_ref * (P_esc / P_esc_ref)  # [kg] Mass ESC

        outputs["P_esc"] = P_esc
        outputs["U_esc"] = U_esc
        outputs["M_esc"] = M_esc
