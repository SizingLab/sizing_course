import openmdao.api as om
import numpy as np


class Constraints(om.ExplicitComponent):
    def setup(self):
        self.add_input("M_total", val=np.nan, units="kg")
        self.add_input("M_total_real", val=np.nan, units="kg")
        self.add_input("T_max_mot", val=np.nan, units="N*m")
        self.add_input("T_pro_to", val=np.nan, units="N*m")
        self.add_input("U_bat", val=np.nan, units="V")
        self.add_input("U_mot_to", val=np.nan, units="V")
        self.add_input("P_bat_max", val=np.nan, units="W")
        self.add_input("P_el_mot_to", val=np.nan, units="W")
        self.add_input("N_pro", val=np.nan)
        self.add_input("U_esc", val=np.nan, units="V")
        self.add_input("t_hov", val=np.nan, units="min")
        self.add_input("t_hov_spec", val=np.nan, units="min")
        self.add_input("MTOW", val=np.nan, units="kg")

        self.add_output("cons_1")
        self.add_output("cons_2")
        self.add_output("cons_3")
        self.add_output("cons_4")
        self.add_output("cons_5")
        self.add_output("cons_6")
        self.add_output("cons_7")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        M_total = inputs["M_total"]
        M_total_real = inputs["M_total_real"]
        T_max_mot = inputs["T_max_mot"]
        T_pro_to = inputs["T_pro_to"]
        U_bat = inputs["U_bat"]
        U_mot_to = inputs["U_mot_to"]
        P_bat_max = inputs["P_bat_max"]
        P_el_mot_to = inputs["P_el_mot_to"]
        N_pro = inputs["N_pro"]
        U_esc = inputs["U_esc"]
        t_hov = inputs["t_hov"]
        t_hov_spec = inputs["t_hov_spec"]
        MTOW = inputs["MTOW"]

        cons_1 = M_total - M_total_real
        cons_2 = T_max_mot - T_pro_to
        cons_3 = U_bat - U_mot_to
        cons_4 = P_bat_max - (P_el_mot_to * N_pro) / 0.95
        cons_5 = U_esc - U_bat
        cons_6 = t_hov - t_hov_spec
        cons_7 = MTOW - M_total_real

        outputs["cons_1"] = cons_1
        outputs["cons_2"] = cons_2
        outputs["cons_3"] = cons_3
        outputs["cons_4"] = cons_4
        outputs["cons_5"] = cons_5
        outputs["cons_6"] = cons_6
        outputs["cons_7"] = cons_7
