#!/usr/bin/env python
# coding: utf-8

# # Quizz

# This last part of CM1 is a quizz

# In[1]:


from jupyterquiz import display_quiz


# # Design drivers and sizing scenarios
# 
# ### Keywords on design drivers and sizing scenarios
# 
# Design drivers:
# - Operational limits  
# Transient: rapid degradations   
# Continuous: gradual degration  
# - Imperfections (Energy storage, Losses)
# 
# Sizing scenarios:
# - Functions of the system
# - Design drivers of components
# 
# 
# ### Quiz
# ### Ballscrew
# Rapid and gradual degradations of Ball and roller screws are defined by specific parameters.  
# 
# ![BallScrew](./assets/images/DesignDriver_Ballscrew.png)
# 
# The first one is defined by: "Load acting on the axis of the screw resulting in a nominal life of one million revolutions"

# In[2]:


display_quiz("./assets/quiz/quiz_ballscrew.json")


# ### Electric motor
# The operational limits of a brushless motors is defined by the following diagram.
# 
# ![SOA Brushless motors](./assets/images/DesignDriver_BrushlessMotor.png)
# 
# Match the ABC boundaries of the torque/speed characteristic with the physical limitations of a brushless motor-drive combination. Also indicate whether the operational limit is transient or continuous.

# In[3]:


display_quiz("./assets/quiz/quiz_motor.json")


# ### Imperfections Power transmission
# Power transmission components have imperfections such as inertia. A ball screw SDS 14x4 of 0.5 m is associated with a reducer of reduction ratio 3 and a NX205 brushless motor. Using informations given in the following datasheet, calculate the  inertia of the components.
# 
# ![Inertia](./assets/images/DesignDriver_Inertia.png)
# 

# In[4]:


display_quiz("./assets/quiz/quiz_inertia.json")


# In[ ]:




