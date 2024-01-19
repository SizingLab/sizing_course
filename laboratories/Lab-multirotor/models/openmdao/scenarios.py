import openmdao.api as om
import numpy as np


class Scenarios(om.ExplicitComponent):
    def setup(self):
        self.add_input("k_os", val=np.nan)
        self.add_input("M_pay", val=np.nan, units="kg")
        self.add_input("N_pro_arm", val=np.nan)
        self.add_input("N_arm", val=np.nan)
        self.add_input("a_to", val=np.nan, units="m/s**2")

        self.add_output("M_total", units="kg")
        self.add_output("N_pro")
        self.add_output("F_pro_hov", units="N")
        self.add_output("F_pro_to", units="N")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        k_os = inputs["k_os"]
        M_pay = inputs["M_pay"]
        N_pro_arm = inputs["N_pro_arm"]
        N_arm = inputs["N_arm"]
        a_to = inputs["a_to"]

        M_total = (
            k_os * M_pay
        )  # [kg] Estimation of the total mass (or equivalent weight of dynamic scenario)
        N_pro = N_pro_arm * N_arm  # Propellers number
        F_pro_hov = M_total * (9.81) / N_pro  # [N] Thrust per propeller for hover
        F_pro_to = M_total * (9.81 + a_to) / N_pro  # [N] Thrust per propeller for take-off

        outputs["M_total"] = M_total
        outputs["N_pro"] = N_pro
        outputs["F_pro_hov"] = F_pro_hov
        outputs["F_pro_to"] = F_pro_to
