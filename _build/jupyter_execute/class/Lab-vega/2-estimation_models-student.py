#!/usr/bin/env python
# coding: utf-8

# <img src="../../images/logo.png" style="float:right; max-width: 120px; display: inline" alt="SizingLab" />

# 
# 
# # Estimation models with scaling laws and linear regression (student version)
# 
# *Written by Marc Budinger (INSA Toulouse) and Scott Delbecq (ISAE-SUPAERO), Toulouse, France*
# 
# The estimation models calculate the component characteristics requested for their selection without requiring a detailed design. Scaling laws are particularly suitable for this purpose. This notebook illustrates the approach with  roller bearings used as thrust bearing in the linear Electro-mechanical Actuator. 
# 
# *Roller bearing in face to face configuration (SKF) :*
# 
# <img src="./assets/images/RollerBearingFaceToFace.png" width="20%">
# 
# Validation of the obtained scaling laws is realized thanks linear regression on catalog data.  
# 
# The [following article](https://hal.archives-ouvertes.fr/hal-00712986/document) give more details and other models for electromechanical actuators:  
# >*Budinger, M., Liscouët, J., Hospital, F., & Maré, J. C. (2012). Estimation models for the preliminary design of electromechanical actuators. Proceedings of the Institution of Mechanical Engineers, Part G: Journal of Aerospace Engineering, 226(3), 243-259.*  
# 

# ## Scaling laws
# 
# #### Assumptions and notation
# The scaling laws use two key modelling assumptions:
# 1. All material properties are assumed to be identical to those of the component used for reference: $E^* = \rho^* = ... = 1$
# 2. The ratio of all the lengths of the considered component to all the lengths of the reference component is constant (geometric similarity): $D^* = T^*= ... = d^*$
# 
# For mechanical components, the mechanical stresses in the materials must be kept below elastic, fatigue, or contact pressure (Hertz) limits. Taking the same stress limit for a full product range yields: $ F^* = d^{*2}$
# 
# *Notation*: The x* scaling ratio of a given parameter is calculated as $x^*=\frac{x}{x_{ref}}$ where $x_{ref}$ is the parameter taken as the reference and $x$ the parameter under study.
# 

# #### Exercice: Axial maximal force estimation
# Propose a scaling law which links the maximal axial force and diameter. Estimate and print the maximal force for a bearing of 90 mm external diameter knowing the following reference component:   
# $D_{ref} = 140 mm$  
# $F_{axial,ref} = 475 kN$  
# 
# Example of `print()` function use: `print("%s=%.2f" % ("pi", 3.14159))` gives `pi=3.14`

# In[1]:


D_ref = 140  # [mm] Reference diameter
F_axial_ref = 475  # [kN] Reference max axial force

print("The estimated axial force is: %.2f kN" % (F_axial_ref * ))
print("The estimation model is: F_axial_max = %.2e.D^2" % (F_axial_ref * ))


# ## Validation with linear regression
# 
# We will validate the scaling laws obtained with regressions on catalog data. 
# 
# #### Cleaning data
# 
# The first step is to import catalog data stored in a .csv file. We use for that functions from [Panda](https://pandas.pydata.org/index.html) package (with here an [introduction to panda](https://jakevdp.github.io/PythonDataScienceHandbook/03.00-introduction-to-pandas.html)). 

# In[ ]:


# Panda package Importation
import os.path as pth
import pandas as pd

# Read the .csv file with bearing data
file_path = "https://raw.githubusercontent.com/SizingLab/sizing_course/main/class/Lab-vega/assets/data/bearings.csv"
df = pd.read_csv(file_path, sep=";")
# Print the head (first lines of the file)
df.head()


# If we display these data in a scatter plot, we see that some components are not optimized in terms of axial effort.

# In[ ]:


# import plot functions from the mtplotlib package
import matplotlib.pyplot as plt

# plot
g, ax = plt.subplots(1, 1, sharex=True)
ax.plot(df["D"], df["Fa axial static"], ".b")
ax.set_ylabel("Axial maximal static force (kN)")
ax.set_xlabel("External diameter (mm)")
ax.grid()


# It is interesting to clean this data in order to keep only the components representative of the problem considered. For this purpose, Pareto filtering is used where only dominant components are kept. A componant dominate another if the first is not inferior to the second in all selected objectives. Here the objective is small diameter and high maximum static force.
# 

# In[ ]:


# This function tests if a component is dominated
# return 0 if non dominated, the number of domination other else
# inputs :
# x_,y_ : the  component's characteristics to test
# X_,Y_ : the  data set characteristics
def dominated(x_, y_, X_, Y_):
    compteur = 0
    for x, y in zip(X_, Y_):
        # x>x_ for small diameter and  y>y_ for high force
        if (x < x_) and (y > y_):
            compteur += 1
    return compteur


# We create here a new row which will give the information of component dominated or not
df["Dominated"] = False
for i in range(len(df["D"])):
    if (
        dominated(
            df.loc[i, "D"],
            df.loc[i, "Fa axial static"],
            df["D"].values,
            df["Fa axial static"].values,
        )
        > 0
    ):
        df.loc[i, "Dominated"] = True
# Print the new table
df


# The Pareto front component are now ploted in red. 

# In[ ]:


# We keep only the non dominated component (Pareto front)
df_filter =
# Diameter of filtered bearings
df_filter_D =
# Axial force of filtered bearings
df_filter_F =

# plot of the data set with the Pareto front
g, ax = plt.subplots(1, 1, sharex=True)
ax.plot(df["D"], df["Fa axial static"], ".b", df_filter_D, df_filter_F, ".r")
ax.set_ylabel("Axial maximal static force (kN)")
ax.set_xlabel("External diameter (mm)")
ax.grid()


# #### Linear regression
# 
# The filtered data will be approximeted here by a linear regression of the form: $Y=aX+b$  
# 
# We use here :
# - the functions of the [scikit-learn](http://scikit-learn.org) package ([linear_model.LinearRegression](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html))
# - a log transformation in order to linearize the power law expression $Y=k.X^a$  into $log(Y) = log(k) + a.log(X)$
# 
# A usefull introduction to machine learning can be found here [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/):
# > VanderPlas, J. (2016). Python data science handbook: Essential tools for working with data. " O'Reilly Media, Inc."
# 
# with examples of [linear regressions](https://jakevdp.github.io/PythonDataScienceHandbook/05.06-linear-regression.html).

# In[ ]:


# Import packages
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt

# Create a new object for the linear regression
reg = linear_model.LinearRegression()

# Get the data :
# - X inputs and Y outputs
# - apply a log transformation in order

X = np.log10(df_filter["D"].values)

Y = np.log10(df_filter["Fa axial static"].values)

# Gives a new shape to an array without changing its data : transform data into array
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)

# Realize the data fitting
reg.fit(X, Y)


# We can now compare the coefficients of linear regression with scaling laws:

# ##### Exercice
# Print the expression of $F_{axial}$ get with the regression.
# 
# Example of `print()` function use: `print("%s=%.2f" % ("pi", 3.14159))` gives `pi=3.14`

# In[ ]:


print("The coefficient are:", )
print("The intercept is:", )
print("The estimation model is: F_axial_max = %.2e.D^%.1f" % )


# Remark : unit of $D$ is $mm$ and F$_{axial,max}$ is $kN$
# 
# We can also directly compare on a graphic the both expressions:

# In[ ]:


# Add 1 mm diameter point
Xa = np.insert(X, 0, np.log10([1, 10, 20])).reshape(-1, 1)
# The predict function calculate the output with the regression
Yest = reg.predict(Xa)

# Scaling law
Yscal =

# plot
h, ax = plt.subplots(1, 1, sharex=True)
ax.plot(10**Xa, 10**Yest, "--b", 10**X, 10**Y, ".r", 10**Xa, Yscal, "g")
ax.set_ylabel("Axial maximal static force (kN)")
ax.set_xlabel("External diameter (mm)")
ax.grid()


# In[ ]:


10 ** reg.predict([[np.log10(90)]])


# In[ ]:





# In[ ]:




