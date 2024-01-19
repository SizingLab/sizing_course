import openmdao.api as om
import numpy as np


class Frame(om.ExplicitComponent):
    def setup(self):
        self.add_input("N_arm", val=np.nan)
        self.add_input("D_pro", val=np.nan, units="m")
        self.add_input("F_pro_to", val=np.nan, units="N")
        self.add_input("N_pro_arm", val=np.nan)
        self.add_input("sigma_max", val=np.nan, units="Pa")
        self.add_input("k_D", val=np.nan)
        self.add_input("rho_s", val=np.nan, units="kg/m**3")
        self.add_output("alpha_sep", units="rad")
        self.add_output("L_arm", units="m")
        self.add_output("D_out_arm", units="m")
        self.add_output("D_in_arm", units="m")
        self.add_output("M_arms", units="kg")
        self.add_output("M_body", units="kg")
        self.add_output("M_frame", units="kg")

    def setup_partials(self):
        self.declare_partials("*", "*", method="cs")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        N_arm = inputs["N_arm"]
        D_pro = inputs["D_pro"]
        F_pro_to = inputs["F_pro_to"]
        N_pro_arm = inputs["N_pro_arm"]
        sigma_max = inputs["sigma_max"]
        k_D = inputs["k_D"]
        rho_s = inputs["rho_s"]

        # Arms selection with propellers size
        alpha_sep = 2 * np.pi / N_arm  # [rad] interior angle separation between propellers
        L_arm = D_pro / (2.0 * np.sin(alpha_sep / 2.0))  # [m] length of the arm

        # Tube diameter & thickness selection with take-off scenario
        D_out_arm = (F_pro_to * N_pro_arm * L_arm * 32 / (np.pi * sigma_max * (1 - k_D**4))) ** (
            1 / 3
        )  # [m] outer diameter of the arm (hollow cylinder)
        D_in_arm = k_D * D_out_arm  # [m] inner diameter of the arm (hollow cylinder)

        # Estimation models
        M_arms = (
            np.pi / 4 * (D_out_arm**2 - (k_D * D_out_arm) ** 2) * L_arm * rho_s * N_arm
        )  # [kg] mass of the arms
        M_body = 1.5 * M_arms  # [kg] mass of the body (40% of total mass is the arms)
        M_frame = M_body + M_arms  # [kg] total mass of the frame

        outputs["alpha_sep"] = alpha_sep
        outputs["L_arm"] = L_arm
        outputs["D_out_arm"] = D_out_arm
        outputs["D_in_arm"] = D_in_arm
        outputs["M_arms"] = M_arms
        outputs["M_body"] = M_body
        outputs["M_frame"] = M_frame
