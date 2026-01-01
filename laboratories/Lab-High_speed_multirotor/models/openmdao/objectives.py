import openmdao.api as om
import numpy as np


class Objectives(om.ExplicitComponent):
    def setup(self):
        self.add_input("C_bat", val=np.nan, units="A*s")
        self.add_input("I_bat_hov", val=np.nan, units="A")
        self.add_input("M_esc", val=np.nan, units="kg")
        self.add_input("M_pro", val=np.nan, units="kg")
        self.add_input("M_mot", val=np.nan, units="kg")
        self.add_input("N_pro", val=np.nan)
        self.add_input("M_pay", val=np.nan, units="kg")
        self.add_input("M_bat", val=np.nan, units="kg")
        self.add_input("M_frame", val=np.nan, units="kg")
        self.add_output("t_hov", units="min")
        self.add_output("M_total_real", units="kg")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        C_bat = inputs["C_bat"]
        I_bat_hov = inputs["I_bat_hov"]
        M_esc = inputs["M_esc"]
        M_pro = inputs["M_pro"]
        M_mot = inputs["M_mot"]
        N_pro = inputs["N_pro"]
        M_pay = inputs["M_pay"]
        M_bat = inputs["M_bat"]
        M_frame = inputs["M_frame"]

        # ---
        t_hov = C_bat / I_bat_hov / 60.0  # [min] Hover time
        M_total_real = (M_esc + M_pro + M_mot) * N_pro + M_pay + M_bat + M_frame  # [kg] Total mass

        outputs["t_hov"] = t_hov
        outputs["M_total_real"] = M_total_real
