#!/usr/bin/env python
# coding: utf-8

# <img src="../../images/logo.png" style="float:right; max-width: 120px; display: inline" alt="SizingLab" />

# # Sizing procedure and optimization with OpenMDAO
# 
# *Written by Marc Budinger (INSA Toulouse) and Scott Delbecq (ISAE-SUPAERO), Toulouse, France*
# 
# The objective of this notebook is to learn how to implement a sizing code and use a simple numerical optimization to find the optimal design of the system. The system studied is the TVC EMA of the VEGA launcher.

# In[1]:


import numpy as np
import scipy.optimize
from scipy import log10
from math import pi


# ## Objectives and specifications
# 
# The objective is to select the reduction ratio of a gear reducer in order to minimize the mass of the motor.
# 
# The application have to ensure at nozzle level :
# - a max torque $T_{load}$ of $48 kNm$ and a max acceleration of $\dot{\omega}_{max}=811 °/s²$  
# - a max speed $\omega_{max}$ of 9.24 °/s
# - a max magnitude $\alpha_{max}$ of 5.7 °
# 
# We will give here an example based on a linear actuator with a preselected roller screw (pitch of 10 mm/rev).
# We assume here, for simplification, the efficiency equal to 70%.
# 
# *EMA components:*
# 
# ![EMA](./assets/images/EMA_VEGA.png)
# 

# We first define the specifications and assumptions for the sizing:

# In[2]:


# Specifications
angular_magnitude_max = 5.7 * pi / 180  # [rad]
max_dyn_torque = 48e3  # [N.m]
max_speed_rot = 9.24 * pi / 180  # [rad/s]
max_acc_rot = 811 * pi / 180  # [rad/s²]

# Assumptions
pitch = 10e-3 / 2 / pi  # [m/rad]
nu_screw = 0.7  # [-]

# Security coefficient for mechanical components
k_sec = 2


# We then define the main characteristics for the components for the scaling laws:

# In[3]:


# Motor
T_mot_guess_max_ref = 13.4  # [N.m]
W_mot_max_ref = 754  # [rad/s]
J_mot_ref = 2.9e-4 / 2  # [kg.m²]
M_mot_ref = 3.8  # [kg]

# Rod end
F_rod_max_ref = 183e3  # [N]
M_rod_ref = 1.55  # [kg]
L_rod_ref = 0.061  # [m]

# Screw
M_nut_ref = 2.1  # [kg]
Ml_screw_ref = 9.4  # [kg/m]
D_nut_ref = 0.08  # [m]
L_nut_ref = 0.12 * 0.08 / 0.09  # [m]
F_screw_max_ref = 135e3  # [N]

# Bearing
M_bearing_ref = 5.05  # [kg]
L_bearing_ref = 0.072  # [m]
F_bearing_max_ref = 475e3  # [N]


# ## Sizing code

# The sizing code is defined here in a function which can give an evaluation of the objective and of the constraints function of design variables.
# 
# The **design variables** of this sizing code are :
# - the reduction ratio of the reducer
# - an oversizing coefficient for the selection of the motor used to tacke an algebraic loop
# - the positions ($d_1$ and $d_2$) of the actuator anchorages
#     
# *New design variables*
# ![Mechanical Loads](./assets/images/design_variables_vega.png)
#     
# The **objective** is the global mass of the actuator.
# 
# The **constraints** which should be positives are here: 
# - the speed margin, ie. the motor doesn't exceed its maximum speed
# - the torque margin, ie. the motor doesn't exceed its maximum torque
# - the length margin, ie. the global length of the actuator doesn't exceed the distance between anchorage points
# 

# In[4]:


import openmdao.api as om


# In[5]:


class LeverArm(om.Group):
    """
    Actuator model.
    """

    def setup(self):

        self.add_subsystem(
            "lever_arm",
            om.ExecComp(
                "lever_arm = ((-(-0.9744 * d1 - 1.372) * (0.2248 * d1 - 0.3757) * ((0.2248 * d1 - 0.3757) ** 2 + (-0.9744 * d1 + d2 - 1.172) ** 2) ** (-0.5) + (0.2248 * d1 + 0.9823) * ((0.2248 * d1 - 0.3757) ** 2 + (-0.9744 * d1 + d2 - 1.172) ** 2) ** (-0.5)* (-0.9744 * d1 + d2 - 1.172))** 2) ** 0.5",
                d1=0.0,
                d2=0.0,
            ),
            promotes=["*"],
        )


# In[6]:


class Actuator(om.Group):
    """
    Actuator model.
    """

    def setup(self):

        self.add_subsystem(
            "actuator_length",
            om.ExecComp(
                "actuator_length = ((0.2248 * d1 - 0.3757) ** 2 + (-0.9744 * d1 + d2 - 1.172) ** 2) ** 0.5",
                d1=0.0,
                d2=0.0,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "stroke",
            om.ExecComp(
                "stroke = angular_magnitude_max * 2 * lever_arm",
                angular_magnitude_max=angular_magnitude_max,
            ),
            promotes=["*"],
        )


# In[7]:


class LoadSpeed(om.Group):
    """
    Load and speed model.
    """

    def setup(self):

        self.add_subsystem(
            "max_speed",
            om.ExecComp("max_speed = max_speed_rot * lever_arm", max_speed_rot=max_speed_rot),
            promotes=["*"],
        )

        self.add_subsystem(
            "max_load",
            om.ExecComp("max_load = max_dyn_torque / lever_arm", max_dyn_torque=max_dyn_torque),
            promotes=["*"],
        )


# In[8]:


class Forces(om.Group):
    """
    Stall and mechanical forces model.
    """

    def setup(self):

        self.add_subsystem(
            "max_stall_force",
            om.ExecComp("max_stall_force = T_mot_guess / pitch * reduction_ratio", pitch=pitch),
            promotes=["*"],
        )

        self.add_subsystem(
            "max_mech_force",
            om.ExecComp("max_mech_force = k_sec * max_stall_force", k_sec=k_sec),
            promotes=["*"],
        )


# In[9]:


class Motor(om.Group):
    """
    Motor model.
    """

    def setup(self):

        self.add_subsystem(
            "M_mot",
            om.ExecComp(
                "M_mot = M_mot_ref * (T_mot_guess / T_mot_guess_max_ref) ** (3 / 3.5)",
                M_mot_ref=M_mot_ref,
                T_mot_guess_max_ref=T_mot_guess_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "J_mot",
            om.ExecComp(
                "J_mot = J_mot_ref * (T_mot_guess / T_mot_guess_max_ref) ** (5 / 3.5)",
                J_mot_ref=J_mot_ref,
                T_mot_guess_max_ref=T_mot_guess_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "W_mot",
            om.ExecComp(
                "W_mot = W_mot_max_ref * (T_mot_guess / T_mot_guess_max_ref) ** (-1 / 3.5)",
                W_mot_max_ref=W_mot_max_ref,
                T_mot_guess_max_ref=T_mot_guess_max_ref,
            ),
            promotes=["*"],
        )


# In[10]:


class RodEnd(om.Group):
    """
    Rod end model.
    """

    def setup(self):

        self.add_subsystem(
            "M_rod",
            om.ExecComp(
                "M_rod = M_rod_ref * (max_mech_force / F_rod_max_ref) ** (3 / 2)",
                M_rod_ref=M_rod_ref,
                F_rod_max_ref=F_rod_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "L_rod",
            om.ExecComp(
                "L_rod = L_rod_ref * (max_mech_force / F_rod_max_ref) ** (1 / 2)",
                L_rod_ref=L_rod_ref,
                F_rod_max_ref=F_rod_max_ref,
            ),
            promotes=["*"],
        )


# In[11]:


class Nut(om.Group):
    """
    Nut model.
    """

    def setup(self):

        self.add_subsystem(
            "M_bearing",
            om.ExecComp(
                "M_bearing = M_bearing_ref * (max_mech_force / F_bearing_max_ref) ** (3 / 2)",
                M_bearing_ref=M_bearing_ref,
                F_bearing_max_ref=F_bearing_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "M_screw",
            om.ExecComp(
                "M_screw = Ml_screw_ref * (max_mech_force / F_screw_max_ref) ** (2 / 2) * actuator_length / 2",
                Ml_screw_ref=Ml_screw_ref,
                F_screw_max_ref=F_screw_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "D_nut",
            om.ExecComp(
                "D_nut = D_nut_ref * (max_mech_force / F_screw_max_ref) ** (1 / 2)",
                D_nut_ref=D_nut_ref,
                F_screw_max_ref=F_screw_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "L_nut",
            om.ExecComp(
                "L_nut = L_nut_ref * (max_mech_force / F_screw_max_ref) ** (1 / 2)",
                L_nut_ref=L_nut_ref,
                F_screw_max_ref=F_screw_max_ref,
            ),
            promotes=["*"],
        )


# In[12]:


class Bearing(om.Group):
    """
    Bearing model.
    """

    def setup(self):

        self.add_subsystem(
            "M_nut",
            om.ExecComp(
                "M_nut = M_nut_ref * (max_mech_force / F_screw_max_ref) ** (3 / 2)",
                M_nut_ref=M_nut_ref,
                F_screw_max_ref=F_screw_max_ref,
            ),
            promotes=["*"],
        )

        self.add_subsystem(
            "L_bearing",
            om.ExecComp(
                "L_bearing = L_bearing_ref * (max_mech_force / F_bearing_max_ref) ** (1 / 2)",
                L_bearing_ref=L_bearing_ref,
                F_bearing_max_ref=F_bearing_max_ref,
            ),
            promotes=["*"],
        )


# In[13]:


class MotorTorqueReal(om.Group):
    """
    Real motor torque model.
    """

    def setup(self):

        self.add_subsystem(
            "T_mot_real",
            om.ExecComp(
                "T_mot_real = max_load * pitch / reduction_ratio / nu_screw + J_mot * max_acc_rot * lever_arm * reduction_ratio / pitch",
                pitch=pitch,
                nu_screw=nu_screw,
            ),
            promotes=["*"],
        )


# ## Optimization with SLSQP algorithm
# 

# We will now use the [opmization algorithms](https://docs.scipy.org/doc/scipy/reference/optimize.html) of the Scipy package to solve and optimize the configuration. We will first use the [SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html) algorithm without explicit expression of the gradient (Jacobian). 

# The first step is to give an initial value of optimisation variables:

# In[14]:


# Optimization variables
# Reduction ratio
reduction_ratio_init = 1  # [-]
reduction_ratio_min = 0.1  # [-]
reduction_ratio_max = 10  # [-]

# Oversizing coefficient for multidisciplinary coupling
k_oversizing_init = 1  # [-]
k_oversizing_min = 0.2  # [-]
k_oversizing_max = 5  # [-]

# Anchorage positions
d1_init = 0  # [m]
d1_min = -80 / 100  # [m]
d1_max = 80 / 100  # [m]

d2_init = 0  # [m]
d2_min = -20 / 100  # [m]
d2_max = 20 / 100  # [m]

# Initial values vector for design variables
parameters = np.array((reduction_ratio_init, k_oversizing_init, d1_init, d2_init))


# ### MDF formulation

# ![MDF](./assets/images/mdf.png)

# In[15]:


class MotorTorque(om.Group):
    """
    Real motor torque model.
    """

    def setup(self):

        self.add_subsystem(
            "T_mot_guess",
            om.ExecComp(
                "T_mot_guess = max_load * pitch / reduction_ratio / nu_screw + J_mot * max_acc_rot * lever_arm * reduction_ratio / pitch",
                pitch=pitch,
                nu_screw=nu_screw,
            ),
            promotes=["*"],
        )


# In[16]:


class ObjectiveConstraints(om.Group):
    """
    Objective and constraints model.
    """

    def setup(self):

        self.add_subsystem(
            "objective",
            om.ExecComp("objective = M_mot + M_bearing + 2 * M_rod + M_screw + M_nut"),
            promotes=["*"],
        )

        self.add_subsystem(
            "C1",
            om.ExecComp("C1 = W_mot - reduction_ratio * max_speed / pitch", pitch=pitch),
            promotes=["*"],
        )

        self.add_subsystem(
            "C3",
            om.ExecComp("C3 = actuator_length - stroke - L_nut - L_bearing - 2 * L_rod"),
            promotes=["*"],
        )


# In[17]:


class SystemMDF(om.Group):
    """
    Overall system model with MDF formulation
    """

    def setup(self):

        self.add_subsystem("lever_arm", LeverArm(), promotes=["*"])
        self.add_subsystem("actuator", Actuator(), promotes=["*"])
        self.add_subsystem("load_speed", LoadSpeed(), promotes=["*"])

        # We have to do something here regarding the cycle
        cycle = self.add_subsystem("cycle", om.Group(), promotes=["*"])
        cycle.add_subsystem("motor_torque", MotorTorque(), promotes=["*"])
        cycle.add_subsystem("forces", Forces(), promotes=["*"])
        cycle.add_subsystem("motor", Motor(), promotes=["*"])
        # We had a solver
        cycle.nonlinear_solver = om.NonlinearBlockGS(maxiter=100)

        self.add_subsystem("rod_end", RodEnd(), promotes=["*"])
        self.add_subsystem("nut", Nut(), promotes=["*"])
        self.add_subsystem("bearing", Bearing(), promotes=["*"])
        self.add_subsystem("motor_torque_real", MotorTorqueReal(), promotes=["*"])
        self.add_subsystem("objective_constraints", ObjectiveConstraints(), promotes=["*"])


# In[18]:


import openmdao.api as om
import time

prob = om.Problem()
prob.model = SystemMDF()

prob.driver = om.ScipyOptimizeDriver()
prob.driver.options["optimizer"] = "SLSQP"
# prob.driver.options['maxiter'] = 100
prob.driver.options["tol"] = 1e-8

prob.model.add_design_var("reduction_ratio", lower=reduction_ratio_min, upper=reduction_ratio_max)
prob.model.add_design_var("d1", lower=d1_min, upper=d1_max)
prob.model.add_design_var("d2", lower=d2_min, upper=d2_max)

prob.model.add_objective("objective")
prob.model.add_constraint("C1", lower=0)
prob.model.add_constraint("C3", lower=0)

# Ask OpenMDAO to finite-difference across the model to compute the gradients for the optimizer
prob.model.approx_totals()

prob.setup()
prob.set_solver_print(level=1)

# Initialization of design variables
prob.set_val("reduction_ratio", reduction_ratio_init)
prob.set_val("d1", d1_init)
prob.set_val("d2", d2_init)

start = time.time()
prob.run_driver()
end = time.time()


# In[19]:


print("Objective:")
print("     Total mass = %.2f kg" % (prob.get_val("objective")))
print("Design variables:")
print("     reduction_ratio =  %.2f" % prob.get_val("reduction_ratio"))
print("     d_1 =  %.2f m" % prob.get_val("d1"))
print("     d_2 =  %.2f m" % prob.get_val("d2"))
print("Performances:")
print("     Stroke = %.2f m" % prob.get_val("stroke"))
print("     Max load = %.0f N" % prob.get_val("max_load"))
print("     Stall load = %.0f N" % prob.get_val("max_stall_force"))
print("Components characteristics:")
print("     Lever arm = %.2f m" % prob.get_val("lever_arm"))
print("     Actuator length = %.2f m" % prob.get_val("actuator_length"))
print("     Motor mass = %.2f kg" % prob.get_val("M_mot"))
print("     Max Tem = %.2f N.m" % prob.get_val("T_mot_real"))
print("     Rod-end mass = %.2f kg" % (2 * prob.get_val("M_rod")))
print("     Rod-end length = %.2f m" % prob.get_val("L_rod"))
print("     Screw mass = %.2f kg" % prob.get_val("M_screw"))
print("     Nut mass = %.2f kg" % (2 * prob.get_val("M_nut")))
print("     Nut length = %.2f m" % prob.get_val("L_nut"))
print("     Bearing length = %.2f m" % prob.get_val("L_bearing"))
print("Constraints (should be >= 0):")
print("     Speed margin: W_mot-reduction_ratio*max_speed/pitch= %.3f" % prob.get_val("C1"))
print(
    "     Length margin: actuator_length-stroke-L_nut-L_bearing-2*L_rod =  %.3f"
    % prob.get_val("C3")
)
print("Calculation time:\n", end - start, "s")


# In[20]:


om.n2(prob)


# ### NVH formulation

# ![MDF](./assets/images/mdf.png)

# In[21]:


class MotorTorqueGuess(om.Group):
    """
    Guess of motor torque model.
    """

    def setup(self):

        self.add_subsystem(
            "T_mot_guess",
            om.ExecComp(
                "T_mot_guess = k_oversizing * max_load * pitch / reduction_ratio / nu_screw",
                pitch=pitch,
                nu_screw=nu_screw,
            ),
            promotes=["*"],
        )


# In[22]:


class ObjectiveConstraints(om.Group):
    """
    Objective and constraints model.
    """

    def setup(self):

        self.add_subsystem(
            "objective",
            om.ExecComp("objective = M_mot + M_bearing + 2 * M_rod + M_screw + M_nut"),
            promotes=["*"],
        )

        self.add_subsystem(
            "C1",
            om.ExecComp("C1 = W_mot - reduction_ratio * max_speed / pitch", pitch=pitch),
            promotes=["*"],
        )

        self.add_subsystem("C2", om.ExecComp("C2 = T_mot_guess - T_mot_real"), promotes=["*"])

        self.add_subsystem(
            "C3",
            om.ExecComp("C3 = actuator_length - stroke - L_nut - L_bearing - 2 * L_rod"),
            promotes=["*"],
        )


# In[23]:


class SystemNVH(om.Group):
    """
    Overall system model with NVH formulation
    """

    def setup(self):
        self.add_subsystem("lever_arm", LeverArm(), promotes=["*"])
        self.add_subsystem("actuator", Actuator(), promotes=["*"])
        self.add_subsystem("load_speed", LoadSpeed(), promotes=["*"])
        self.add_subsystem("motor_torque", MotorTorqueGuess(), promotes=["*"])
        # self.add_subsystem('motor_torque', MotorTorque(), promotes=["*"])
        self.add_subsystem("forces", Forces(), promotes=["*"])
        self.add_subsystem("motor", Motor(), promotes=["*"])
        self.add_subsystem("rod_end", RodEnd(), promotes=["*"])
        self.add_subsystem("nut", Nut(), promotes=["*"])
        self.add_subsystem("bearing", Bearing(), promotes=["*"])
        self.add_subsystem("motor_torque_real", MotorTorqueReal(), promotes=["*"])
        self.add_subsystem("objective_constraints", ObjectiveConstraints(), promotes=["*"])


# In[24]:


import openmdao.api as om
import time

prob = om.Problem()
prob.model = SystemNVH()

prob.driver = om.ScipyOptimizeDriver()
prob.driver.options["optimizer"] = "SLSQP"
# prob.driver.options['maxiter'] = 100
prob.driver.options["tol"] = 1e-8

prob.model.add_design_var("reduction_ratio", lower=reduction_ratio_min, upper=reduction_ratio_max)
prob.model.add_design_var("k_oversizing", lower=k_oversizing_min, upper=k_oversizing_max)
prob.model.add_design_var("d1", lower=d1_min, upper=d1_max)
prob.model.add_design_var("d2", lower=d2_min, upper=d2_max)

prob.model.add_objective("objective")
prob.model.add_constraint("C1", lower=0)
prob.model.add_constraint("C2", lower=0)
prob.model.add_constraint("C3", lower=0)

# Ask OpenMDAO to finite-difference across the model to compute the gradients for the optimizer
prob.model.approx_totals()

prob.setup()
prob.set_solver_print(level=0)

# Initialization of design variables
prob.set_val("reduction_ratio", reduction_ratio_init)
prob.set_val("k_oversizing", k_oversizing_init)
prob.set_val("d1", d1_init)
prob.set_val("d2", d2_init)

start = time.time()
prob.run_driver()
end = time.time()


# We can print of the characterisitcs of the problem before optimization with the intitial vector of optimization variables:

# In[25]:


print("Objective:")
print("     Total mass = %.2f kg" % (prob.get_val("objective")))
print("Design variables:")
print("     reduction_ratio =  %.2f" % prob.get_val("reduction_ratio"))
print("     k_oversizing =  %.2f" % prob.get_val("k_oversizing"))
print("     d_1 =  %.2f m" % prob.get_val("d1"))
print("     d_2 =  %.2f m" % prob.get_val("d2"))
print("Performances:")
print("     Stroke = %.2f m" % prob.get_val("stroke"))
print("     Max load = %.0f N" % prob.get_val("max_load"))
print("     Stall load = %.0f N" % prob.get_val("max_stall_force"))
print("Components characteristics:")
print("     Lever arm = %.2f m" % prob.get_val("lever_arm"))
print("     Actuator length = %.2f m" % prob.get_val("actuator_length"))
print("     Motor mass = %.2f kg" % prob.get_val("M_mot"))
print("     Max Tem = %.2f N.m" % prob.get_val("T_mot_real"))
print("     Rod-end mass = %.2f kg" % (2 * prob.get_val("M_rod")))
print("     Rod-end length = %.2f m" % prob.get_val("L_rod"))
print("     Screw mass = %.2f kg" % prob.get_val("M_screw"))
print("     Nut mass = %.2f kg" % (2 * prob.get_val("M_nut")))
print("     Nut length = %.2f m" % prob.get_val("L_nut"))
print("     Bearing length = %.2f m" % prob.get_val("L_bearing"))
print("Constraints (should be >= 0):")
print("     Speed margin: W_mot-reduction_ratio*max_speed/pitch= %.3f" % prob.get_val("C1"))
print("     Torque margin: T_mot_guess-T_mot_real= %.3f " % prob.get_val("C2"))
print(
    "     Length margin: actuator_length-stroke-L_nut-L_bearing-2*L_rod =  %.3f"
    % prob.get_val("C3")
)
print("Calculation time:\n", end - start, "s")


# In[26]:


om.n2(prob)

