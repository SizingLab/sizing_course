import openmdao.api as om
import numpy as np


class Motor(om.ExplicitComponent):
    def setup(self):
        self.add_input("k_mot", val=np.nan)
        self.add_input("T_pro_hov", val=np.nan, units="N*m")
        self.add_input("k_vb", val=np.nan)
        self.add_input("P_pro_to", val=np.nan, units="W")
        self.add_input("k_speed_mot", val=np.nan)
        self.add_input("Omega_pro_to", val=np.nan, units="rad/s")
        self.add_input("M_mot_ref", val=np.nan, units="kg")
        self.add_input("T_nom_mot_ref", val=np.nan, units="N*m")
        self.add_input("R_mot_ref", val=np.nan, units="ohm")
        self.add_input("K_T_ref", val=np.nan, units="N*m/A")
        self.add_input("T_mot_fr_ref", val=np.nan, units="N*m")
        self.add_input("T_max_mot_ref", val=np.nan, units="N*m")
        self.add_input("Omega_pro_hov", val=np.nan, units="rad/s")
        self.add_input("T_pro_to", val=np.nan, units="N*m")

        self.add_output("T_nom_mot", units="N*m")
        self.add_output("U_bat", units="V")
        self.add_output("K_T", units="N*m/A")
        self.add_output("M_mot", units="kg")
        self.add_output("R_mot", units="ohm")
        self.add_output("T_mot_fr", units="N*m")
        self.add_output("T_max_mot", units="N*m")
        self.add_output("I_mot_hov", units="A")
        self.add_output("U_mot_hov", units="V")
        self.add_output("P_el_mot_hov", units="W")
        self.add_output("I_mot_to", units="A")
        self.add_output("U_mot_to", units="V")
        self.add_output("P_el_mot_to", units="W")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        k_mot = inputs["k_mot"]
        T_pro_hov = inputs["T_pro_hov"]
        k_vb = inputs["k_vb"]
        P_pro_to = inputs["P_pro_to"]
        k_speed_mot = inputs["k_speed_mot"]
        Omega_pro_to = inputs["Omega_pro_to"]
        M_mot_ref = inputs["M_mot_ref"]
        T_nom_mot_ref = inputs["T_nom_mot_ref"]
        R_mot_ref = inputs["R_mot_ref"]
        K_T_ref = inputs["K_T_ref"]
        T_mot_fr_ref = inputs["T_mot_fr_ref"]
        T_max_mot_ref = inputs["T_max_mot_ref"]
        Omega_pro_hov = inputs["Omega_pro_hov"]
        T_pro_to = inputs["T_pro_to"]

        # Nominal torque selection with hover scenario
        T_nom_mot = k_mot * T_pro_hov  # [N*m] Motor nominal torque per propeller

        # Torque constant selection with take-off scenario
        U_bat = k_vb * 1.84 * P_pro_to ** (0.36)  # [V] battery voltage estimation
        K_T = U_bat / (k_speed_mot * Omega_pro_to)  # [N*m/A] or [V/(rad/s)] Kt motor

        # Estimation models
        M_mot = M_mot_ref * (T_nom_mot / T_nom_mot_ref) ** (3.0 / 3.5)  # [kg] Motor mass
        R_mot = (
            R_mot_ref * (T_nom_mot / T_nom_mot_ref) ** (-5.0 / 3.5) * (K_T / K_T_ref) ** 2.0
        )  # [ohm] motor resistance
        T_mot_fr = T_mot_fr_ref * (T_nom_mot / T_nom_mot_ref) ** (
            3.0 / 3.5
        )  # [N*m] Friction torque
        T_max_mot = T_max_mot_ref * (T_nom_mot / T_nom_mot_ref)  # [N*m] Max. torque

        # Performance in various operating conditions
        # Hover current and voltage
        I_mot_hov = (T_pro_hov + T_mot_fr) / K_T  # [A] Current of the motor per propeller
        U_mot_hov = (
            R_mot * I_mot_hov + Omega_pro_hov * K_T
        )  # [V] Voltage of the motor per propeller
        P_el_mot_hov = U_mot_hov * I_mot_hov  # [W] Hover : electrical power
        # Takeoff current and voltage
        I_mot_to = (T_pro_to + T_mot_fr) / K_T  # [A] Current of the motor per propeller
        U_mot_to = R_mot * I_mot_to + Omega_pro_to * K_T  # [V] Voltage of the motor per propeller
        P_el_mot_to = U_mot_to * I_mot_to  # [W] Takeoff : electrical power

        outputs["T_nom_mot"] = T_nom_mot
        outputs["U_bat"] = U_bat
        outputs["K_T"] = K_T
        outputs["M_mot"] = M_mot
        outputs["R_mot"] = R_mot
        outputs["T_mot_fr"] = T_mot_fr
        outputs["T_max_mot"] = T_max_mot
        outputs["I_mot_hov"] = I_mot_hov
        outputs["U_mot_hov"] = U_mot_hov
        outputs["P_el_mot_hov"] = P_el_mot_hov
        outputs["I_mot_to"] = I_mot_to
        outputs["U_mot_to"] = U_mot_to
        outputs["P_el_mot_to"] = P_el_mot_to
