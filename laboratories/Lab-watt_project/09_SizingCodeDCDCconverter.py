#!/usr/bin/env python
# coding: utf-8

# <img src="./pictures/logo-insa.png" style="float:right; max-width: 60px; display: inline" alt="INSA" /></a>

# # Sizing code of a DC/DC converter
# *Written by Marc Budinger, INSA Toulouse, France*

# Nous allons synthétiser ici l'ensemble des modèles en un code de dimensionnement. 
# Pour rappel :
# 
# 


# In[5]:


# DC/DC converter Specifications
E=150 # [V] DC bus voltage
IL=140 # [A] DC current of the load
UL=62.25 # [V] DC voltage of the load
T_amb=40 # [°C] Ambient temperature
 
# Design Assumptions
DE=E*.01 # [V] Max ripple voltage DC bus
DIL=IL*0.35 # [A] Max current ripple


# In[6]:


## Sizing code


# In[57]:


import numpy as np
import scipy
import scipy.optimize
from math import pi, sqrt
import timeit

# -----------------------
# sizing code
# -----------------------
# inputs: 
# - param: optimisation variables vector 
# - arg: selection of output  
# output: 
# - objective if arg='Obj', problem characteristics if arg='Prt', constraints other else

def SizingDCDC(param, arg):
    # Variables
    # ----------------------------------------
    f=param[0]*1e3 # [Hz] switching frequency
    #-
    T_H=param[1] # [°C] Heatsink temperature (Heatsink)
    W_H=param[2] # [°C] Width W / Height H aspect ratio (Heatsink)
    #-
    e_D=param[3] # [m] air gap / External diameter aspect ratio (Inductor)
    J=param[4]*1e6 # [A/m²] wire current density (Inductor)
    #-
    D_H=param[5] # [m] Diameter / Heigth aspect ratio (Capacitor)
    k_C=param[6] # [m] Oversizing coefficient (Capacitor)
    #-
    k_IGBT=param[7] # [-] Oversizing coefficient (IGBT)
    
    # Main electrical equations
    # ----------------------------------------
    
    # Global
    Alpha=UL/E # [-] Duty cycle
    T=1/f # [s] PWM period
    
    # Filter: Inductor & Capacitor
    L=E*Alpha*(1-Alpha)*T/DIL  # [H] Inductance value
    C=IL*Alpha*(1-Alpha)*T/DE  # [F] Capcitance value
        
    # RMS and mean value
    
    IL_max = IL + DIL/2 # [A] Max current (load side) Inductor
    IL_RMS = IL*sqrt(1+1/12*(DIL/IL)**2) # [A] RMS current (load side) Inductor
    
    IC_RMS = sqrt(Alpha*(1-Alpha))*IL_RMS # [A] RMS current Capacitor
    
    I_IGBT_RMS=sqrt(Alpha)*IL_RMS # [A] RMS current IGBT
    I_IGBT_mean=Alpha*IL # [A] mean current IGBT
    
    I_Diode_RMS=sqrt(1-Alpha)*IL_RMS  # [A] RMS current Diode
    I_Diode_mean=(1-Alpha)*IL  # [A] mean current Diode
    
    
    # Inductor
    # ----------------------------------------
    
    # Assumptions
    B_mag=0.4 # [T] Induction
    k_bob=0.33 # [-] winding coefficient
    T_max_L=150 # [°C] Max temperature

    # Physical constants
    mu_0=4*3.14e-7 # [SI] permeability

    # Reference parameters for scaling laws (Pot core)

    D_ref=66.29e-3 # [m] External diameter
    H_ref=57.3e-3/2 # [m] 1 half core height

    Airon_ref=pi/4*(29.19**2-6.5**2)*1e-6    # [m^2] iron surface
    Awind_ref=43.28*(54.51-28.19)/2*1e-6    # [m^2] winding surface
    Rmoy_ref=(54.51-28.19)/2*1e-3 # [m] Mean radius for winding

    M_ref=225e-3  # [kg] 1 half core mass

    # Magnetic pi_0
    PI0_m=3.86*e_D**(0.344-0.226*np.log10(e_D)-0.0355*(np.log10(e_D))**2)
    
    # Magnetic energy calculation
    E_mag=1/2*L*IL_max**2 # [J] Energy
    
    D=(E_mag*2*PI0_m*D_ref**4/J**2/k_bob**2/Awind_ref**2/mu_0)**(1/5) # External diameter calculation
          
    # Reluctance and inductance
    RL=PI0_m/mu_0/D  # [] reluctance
    N=np.sqrt(L*RL) # [-] turn number
    
    # Wire section & winding surface
    S_w=IL_RMS/J # [m²] 1 wire section area
    S_bob=N*S_w/k_bob # [m^2] winding surface
  
    # Core scaling
    A_iron=Airon_ref*(D/D_ref)**(2) # [m^2] iron surface
    A_wind=Awind_ref*(D/D_ref)**(2) # [m^2] winding surface
    H=H_ref*(D/D_ref)**(1) # [m] 1 half core height    
    Rmoy=Rmoy_ref*(D/D_ref)**(1) # [m] Mean radius for winding
    
    M_core =M_ref*(D/D_ref)**(3) # [kg] one half core mass

    # Magnetic field
    B=N*IL_max/RL/A_iron # [T]
    
    # Mass
    M_copper=2*pi*Rmoy*N*S_w*7800
    M_L=M_copper+M_core*2
    
    # Temperature calculation
    PI0_t = 0.0786 + 0.524*e_D -2.04*e_D**2 # PI0 thermal
    Rth=PI0_t/(0.5*D) # [K/W] thermal resistance
    
    PJ_L=J**2*2*pi*Rmoy*N*S_w*1.7e-8 # [W] Joules losses
    
    T_hot_L=T_H + PJ_L*Rth # [°C] Hot spot temperature
    
    # ----------------------------------------
    # Capacitor

    C_ref= 1000e-6 # [F] Capacitance ref
    D_C_ref= 100e-3 # [m] Diameter reference
    H_C_ref= 155e-3 # [m] Heigth reference
    V_C_ref= 800 # [V] reference voltage
    Rs_C_ref= 3.2e-3 # [Ohm] reference serial resistance
    Rth_C_ref = 3 # [°/W] reference thermal resistance
    M_C_ref=1.5 # [kg] reference mass
    
    T_max_C=80 # [°C] max temeprature
    
    # Scaling laws
    D_C=D_C_ref*(D_H*(C/C_ref))**(1/3) # [m] Capacitor diameter: C*=D*^2H*=D*^3/(D/H) ==> D*=(C*.D/H)^(1/3)
    H_C=D_C/D_H # [m] heigth
    Rs_C=Rs_C_ref*(D_C/D_C_ref)**(-2) # [Ohm] Rs resisatnce: Rs*=D*^-2
    Rth_C=Rth_C_ref*(D_C/D_C_ref)**2*(H_C/H_C_ref) # [K/W] Rth*=(D*2*H)^(-1/3)
    M_C= M_C_ref*(D_C/D_C_ref)**2*(H_C/H_C_ref) # [kg] Capacitor mass: M*=D*^2H*

    # Thermal calculation
    PJ_C=Rs_C*IC_RMS**2 # [W] Capacitor losses
    T_hot_C=T_H + PJ_C*Rth # [°C] Hot spot temperature
    
    # ----------------------------------------
    # IGBT module IXYS: 900V max
    
    I_IGBT_ref=80 # [A] Ref Current of the module
    V0_IGBT_ref=1 #[V] voltage drop 
    R0_IGBT_ref=20e-3 # [Ohm] dynamic resistance
    Ecom_IGBT_ref=8.2e-3 # [J] commutation energy ref
    E_IGBT_ref=600 # [V] ref voltage for commutation loss
    Rth_IGBT_ref=0.3 # [°C/W] thermal resistance
    
    T_max_IGBT=120 # [°C] max temeprature
        
    # current estimation
    I0=k_IGBT*I_IGBT_RMS 
    
    # IGBT scaling
    V0_IGBT=V0_IGBT_ref #[V] voltage drop 
    R0_IGBT=R0_IGBT_ref*(I0/I_IGBT_ref)**(-1) # [Ohm] R0*=I*^-1
    Ecom_IGBT=Ecom_IGBT_ref*(I0*E/(I_IGBT_ref*E_IGBT_ref)) # [J] commutation energy (Eon+Eoff)*=I*E*
    Rth_IGBT=Rth_IGBT_ref*(I0/I_IGBT_ref)**(-1) # [°/W] Rth*=I*^(-1)
    
    # Thermal calculation
    Ploss_IGBT=V0_IGBT*I_IGBT_mean+R0_IGBT*I_IGBT_RMS**2+f*Ecom_IGBT # [W] IGBT losses
    T_hot_IGBT=T_H + Ploss_IGBT*Rth_IGBT # [°C] IGBT junction temperature
    
    # Diode of IGBT module IXYS : 900V max  
      
    I_Diode_ref=41 # [A] Ref Current of the module
    V0_Diode_ref=1 #[V] voltage drop 
    R0_Diode_ref=15e-3 # [Ohm] dynamic resistance
    QrrE_ref=17.2e-3 # [J] commutation energy
    Rth_Diode_ref=0.47 # [°C/W] thermal resistance

    # Diode scaling
    V0_Diode=V0_Diode_ref #[V] voltage drop 
    R0_Diode=R0_Diode_ref*(I0/I_IGBT_ref)**(-1) # [Ohm] R0*=I*^-1
    QrrE=QrrE_ref*(I0*E/(I_IGBT_ref*E_IGBT_ref)) # [J] commutation energy (trrIrm)*=I*E*
    Rth_Diode=Rth_Diode_ref*(I0/I_IGBT_ref)**(-1) # [°/W] Rth*=I*^(-1)

    # Thermal calculation
    Ploss_Diode=V0_Diode*I_Diode_mean+R0_Diode*I_Diode_RMS**2+f*QrrE # [W] Diode losses
    T_hot_Diode=T_H + Ploss_Diode*Rth_Diode  # [°C] Hot spot temperature       
    
    # ----------------------------------------
    # Heatsink : forced convection (2m/s)
    
    Lhs=((D+D_C)*1.2)*1e3 # [mm] Heatsink length
    
    
    # Rth,f = 150*W**(-0.85)*H**(-0.62)*36.7*L**(-0.72) # [°/W] thermal resistance with W,H,L in mm
    # Rth,f = 5505*H**(-1.47)*W_H**(-0.85)*L**(-0.72)
    RthH=(T_H-T_amb)/(Ploss_Diode+Ploss_IGBT+PJ_C+PJ_L) # [°/W] Thermal resistance target
    Hhs=(RthH/5505/Lhs**(-0.72)/W_H**(-0.85))**(-1/1.47) # [mm] Height 
    Whs=Hhs*W_H # [mm] Width
    M_H=0.00263*Whs**0.91*Hhs**0.89*(Lhs/1e3)  # [kg] heatsink mass with W,H,L in mm
    
    # ----------------------------------------
    # Total mass
    
    M_total=M_H+M_L+M_C
    
    # Objective and contraints
    if arg=='Obj':
        return M_total
    elif arg=='Prt':
        print("* Optimisation variables:")
        print("           Frequency f= %.2e Hz"%(f))
        print("           Heatsink temperature (Heatsink) T_H= %.2f [°C]"%(T_H))
        print("           Width W / Height H aspect ratio (Heatsink) W_H= %.2f"%(W_H))
        print("           Air gap / External diameter aspect ratio (Inductor) e_D= %.2f"%(e_D))
        print("           Wire current density (Inductor) J= %.2g [A/m²]"%(J))
        print("           Diameter / Heigth aspect ratio (Capacitor) D_H= %.2f"%(D_H))
        print("           Oversizing coefficient (Capacitor) k_C= %.2f"%(k_C))
        print("           Oversizing coefficient (IGBT) k_IGBT= %.2f"%(k_IGBT))
        print("* Components characteristics:")
        print("           Global mass = %.2f kg"%(M_total))
        print("           Power = %.2f kW"%(IL*UL/1e3))
        print("           Efficiency = %.2f %%"%((IL*UL)/(IL*UL+(Ploss_Diode+Ploss_IGBT+PJ_C+PJ_L))*100))
        print("         ---- Inductor")
        print("           Inductance L = %.2g µH" % (L/1e-6))
        print("           Core (2) mass = %.2f kg" % (2*M_core))
        print("           Coil mass = %.2f kg" % M_copper)
        print("           Core dimensions = %.1f (diameter) x %.1f (heigth) mm"%((D*1e3,2*H*1e3)))
        print("           Airgap e = %.1f mm"%(e_D*D*1e3))
        print("           A_iron = %.0f mm^2"%(A_iron*1e6))
        print("           Number of turns = %i"%(N))
        print("           Power loss = %.1f W"%(PJ_L))  
        print("         ---- Capacitor")
        print("           Capacitance = %.2e F"%(C))
        print("           Mass = %.2f kg"%(M_C))
        print("           dimensions = %.1f (diameter) x %.1f (heigth) mm"%((D_C*1e3,H_C*1e3)))
        print("           H = %.2f mm"%(Hhs))  
        print("           Power loss = %.2e W"%(PJ_C))  
        print("         ---- IGBT + Diode")
        print("           Power loss IGBT= %.2f W"%(Ploss_IGBT))  
        print("           Power loss Diode= %.2f W"%(Ploss_Diode))  
        print("         ---- Heatsink")
        print("           Thermal resistance = %.2f K/W"%(RthH))
        print("           Mass = %.2f kg"%(M_H))
        print("           L = %.2f mm"%(Lhs))
        print("           W = %.2f mm"%(Whs))
        print("           H = %.2f mm"%(Hhs))  
        print("* Constraints (should be >0):")
        print("           Winding  surface margin = %.3f mm²" % ((A_wind-S_bob)*1e6))
        print("           Induction margin = %.3f T" %((B_mag-B)))
        print("           Temperature margin L= %.3f K" %(T_max_L-T_hot_L))
        print("           Temperature margin C= %.3f K" %(T_max_C-T_hot_C))
        print("           Temperature margin IBGT= %.3f K" %(T_max_IGBT-T_hot_IGBT))
        print("           Temperature margin Diode= %.3f K" %(T_max_IGBT-T_hot_Diode))
    else:
#       return [A_wind-S_bob, B_mag-B, T_max_L-T_hot_L]
        return [A_wind-S_bob, B_mag-B, T_max_L-T_hot_L, T_max_C-T_hot_C,T_max_IGBT-T_hot_IGBT,T_max_IGBT-T_hot_Diode]


# ## Optimization problem
# 

# The first step is to give an initial value of optimisation variables:

# In[67]:


#Variables d'optimisation
f=10 # [kHz] switching frequency
T_H=65 # [°C] Heatsink temperature (Heatsink)
W_H=.1 # [°C] Width W / Height H aspect ratio (Heatsink)
e_D=8e-3 # [-] air gap / External diameter aspect ratio (Inductor)
J=1 # [A/mm²] wire current density (Inductor)
D_H=1 # [-] Diameter / Heigth aspect ratio (Capacitor)
k_C=1 # [m] Oversizing coefficient (Capacitor)
k_IGBT=1 # [-] Oversizing coefficient (IGBT)

# Vector of parameters
parameters = scipy.array((f,T_H,W_H,e_D,J,D_H,k_C,k_IGBT))


# We can print of the characterisitcs of the problem before optimization with the intitial vector of optimization variables:

# In[68]:


# Initial characteristics before optimization 
print("-----------------------------------------------")
print("Initial characteristics before optimization :")

SizingDCDC(parameters, 'Prt')
print("-----------------------------------------------")


# Then we can solve the problem and print of the optimized solution:

# In[70]:


# optimization with SLSQP algorithm
contrainte=lambda x: SizingDCDC(x, 'Const')
objectif=lambda x: SizingDCDC(x, 'Obj')
result = scipy.optimize.fmin_slsqp(func=objectif, x0=parameters, 
                                   bounds=[(5,15),(45,75),(2,3),(1e-3,1e-1),(1,50),(.5,2),(1,10),(1,10)],
                                   f_ieqcons=contrainte, iter=100, acc=1e-8)


# Final characteristics after optimization 
print("-----------------------------------------------")
print("Final characteristics after optimization :")

SizingDCDC(result, 'Prt')
print("-----------------------------------------------")



# In[ ]:





# In[ ]:




