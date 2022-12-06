#!/usr/bin/env python
# coding: utf-8

# # Quizz

# In[1]:


from jupyterquiz import display_quiz


# ### Linear Regression
# 
# 
# ##### Correlation
# 
# ![Linear regression](./assets/images/LinearRegression_ScatterPlot.png)

# In[2]:


display_quiz("./assets/quiz/quiz_linear_regression-1.json")


# We have a database on SKF bearings. We want to estimate the mass of these bearings. A correlation analysis is carried out from these data. 
# 
# ![Bearing correlation matrix](./assets/images/LinearRegression_CorrelationBearing.png)

# In[3]:


display_quiz("./assets/quiz/quiz_linear_regression-2.json")


# #### Linear regression
# 
# The line y = 4 + 2x has been proposed as a line of best for the following five sets of bivariate data.
# 
# ![Best fit](./assets/images/LinearRegression_bestFit.png)
# 
# 

# In[4]:


display_quiz("./assets/quiz/quiz_linear_regression-3.json")


# ![Regression analysis](./assets/images/LinearRegression_ValidationRegression.png)

# In[5]:


display_quiz("./assets/quiz/quiz_linear_regression-4.json")


# Here is the scatter plot of mass according to the static load. 
# 
# ![Regression analysis](./assets/images/LinearRegression_BearingRegression.png)

# In[6]:


display_quiz("./assets/quiz/quiz_linear_regression-5.json")


# Datas have been transformed with log10 function. 
# 
# ![Regression analysis](./assets/images/LinearRegression_BearingTransformation.png)

# In[7]:


display_quiz("./assets/quiz/quiz_linear_regression-6.json")


# ### Scaling laws

# #### Quizzes on Geometric similarity
# 
# We assume to have similarity on all geometrical parameters : $r^* = d^* = …= l^*$

# In[8]:


display_quiz("./assets/quiz/quiz_scaling_laws-1.json")


# ### Buckingham theorem and scaling laws
# 
# Thanks Buckingham theorem, find evolution of stress $\sigma$ with geometrical dimension for a rectangular sample under a load in a three-point bending setup:  
# - $F$ is the load (force) at the fracture point (N) 
# - $L$ is the length of the support span 
# - $b$ is width 
# - $d$ is thickness 
# 
# ![beam](./assets/images/scaling_beam.png)

# In[9]:


display_quiz("./assets/quiz/quiz_scaling_laws-2.json")


# ### Mechanics: stress & components examples
# 
# ![rod-end](./assets/images/scaling_rodend.png)

# In[10]:


display_quiz("./assets/quiz/quiz_scaling_laws-3.json")

