#!/usr/bin/env python
# coding: utf-8

# # Scenarios and Design Drivers

# ## Sizing and optimization process

# ![drawing75](../../images/design_drivers_process.png)

# ## Sizing scenarios and design drivers concept

# ![drawing75](../../images/sizing_scenarios_design_drivers.png)

# ## Case study

# ### Aircraft Spoiler
# #### Functions
# - Move : Positions 0, 20, 50° (Hinge torque: 1000-2500 N.m)
# - No damage (structure and actuator) if spoiler blocking or on gust action

# ![drawing75](../../images/aircraft_spoiler.png)

# ## Actuator architecture and components

# ### Based on Electro-Mechanical Actuator (Moog)
# #### Components

# ![drawing50](../../images/ema_moog.png)

# ## Design drivers and sizing scenarios

# ### Components of the actuator have to satisfy:
# 1. Transient power demand - Performance &rarr; Prevents rapid damages (e.g. permanent deformation, rupture)
# 2. Continuous power demand - Endurance &rarr; Addresses gradual degradation (e.g., fatigue) and ensures reliable operation during service lifetime

# ### Components of the actuator have imperfections:
# 1. Increase stresses on themselves (e.g , inertia) or on other components (e.g, efficiency)
# 2. Can create new critical cases (e.g, inertia and jamming) &rarr; Induced new design drivers

# ---
# **Sizing scenarios or sizing mission profiles should be determined in order to be representative of all these design drivers**
# 
# ---

# ## Design drivers of mechanical components (1)

# ![drawing75](../../images/dd_mechanical-1.png)

# ## Design drivers of mechanical components (2)

# ![drawing75](../../images/dd_mechanical-2.png)

# ## Induced design drivers of mechanical components

# ### Mechanical losses & friction:
# During sizing it is important to take into account the main parasitic aspect of components in terms of power transmission. For mechanical components efficiency and friction are important.
# 1. First level of modeling : constant efficiency (direct and inverse) with speed and torque
# 2. Second level : friction increases at low speed
# ![drawing50](../../images/losses_frictions.png)

# ![drawing50](../../images/frictions_ema.png)

# ## Design drivers of electrical components (1)

# ![drawing75](../../images/dd_electrical-1.png)

# ---
# **For the EMA study case:**
# - Brushless motor: max torque due to saturation (teeth)
# 
# ---

# ## Design drivers of electrical components (2)

# ![drawing75](../../images/dd_electrical-2.png)

# ---
# **For the EMA study case:**
# - Brushless motor: continuous torque and max temperature due to thermal aspect (need of a thermal model)
# 
# ---

# ## Induced design drivers of the electrical components

# ### Motor rotor inertia:
# - Increases electromagnetic torque : critical issue for high dynamic application (e.g., TVC )
# - High stress when jamming or stop : reflected mass can be very high
# 
# ### Copper and iron losses:
# - Effect on sizing of power electronics
# - Effect on housing for frameless motor
# 
# ![drawing50](../../images/motor_torque_losses.png)

# ---
# **For the EMA study case:**
# - Brushless motor: rotor inertia
# - Brushless motor: losses
# ---

# ## Sizing scenarios and mission profiles

# ![drawing75](../../images/mission_profile.png)

# ## Verification matrix

# ![drawing75](../../images/verification_matrix.png)

# ## Example of representation

# ![drawing75](../../images/dd_representation_example.png)
