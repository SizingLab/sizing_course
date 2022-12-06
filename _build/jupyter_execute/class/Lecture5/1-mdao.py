#!/usr/bin/env python
# coding: utf-8

# # MDAO (Multidisciplinary Design Analysis and Optimization)

# ```{warning}
# This course is under construction...
# ```

# # What is MDAO?

# MDAO stands for Multidisciplinary Design Analysis and Optimization. It is a scientific domain developed to adress the design optimization of multidisciplinary engineering systems that:

# - involve several disciplines/components

# - involve the presence of multidisciplinary couplings (algebraic loops)

# - involve a large number of design variables and constraints (10 to 100 000)

# Therefore, it is particularly interesting for the sizing and optimization of mechatronic systems.

# **_NOTE:_**  MDA vs MDAO: Performing an MDA means to perform a system analysis that solves the multidisciplinary couplings without varying the design variables.

# ## MDAO of engineering systems: # of disciplines vs fidelity of models

# ![drawing50](./assets/images/fidelity_vs_nb_disciplines.png)

# ## MDAO of engineering systems: multidisciplinary couplings

# The design of engineering systems can imply the presence and solving of multidiscipliary couplings. A bad ordering of disciplines or computation steps can lead to the creation or addition or creation of couplings:

# ![drawing50](./assets/images/mdao_ordering.png)

# ## MDAO frameworks

# All commercial modelling and optimization software (Matlab, Wolfram Mathematica...) can be used to implement MDAO techniques. However, recently Python scientific framework have been developed in order to provide a **framework** to implement such problem more easily and solve them more efficiently:

# - OpenMDAO (NASA)
# 
# ![drawing50](./assets/images/openmdao_main_logo.png)
# 
# 
# - GEMSEO (IRT Saint Exupery)
# 
# ![drawing50](./assets/images/gemseo_logo.png)

# ## Gradient-based MDAO: derivate computation techniques

# ![drawing50](./assets/images/coupled_direct_adjoint.png)

# There are different possibilities to compute gradients (derivatives) using typical MDAO frameworks:

# - **full analytic derivative** method uses the analytic derivatives of the model analysis functions (obtained by hand) and the analytic derivatives of the total model

# - **semi-analytic derivative** method is similar to the full analytic except that the model analysis functions derivatives are computed numerically (e.g. Finite Difference (FD))

# - **monolithic derivative** method estimates directly the total system derivatives numerically (e.g. FD) and does not require any knowledge of analysis function derivatives

# ## MDAO formulations

# For solving an MDAO problem multiple formulations (or architectures) can be implemented. In 2012, *Martins and Lambe* proposed a survey of these formulations.

# ![drawing50](./assets/images/mdo_architectures.png)

# ## MDAO formulations: distributed vs monolithic (1/2)

# Distributed formulations use more than one optimizer:

# ![drawing40left](./assets/images/mdao_co.png)

# Monolithic formulations use only one optimizer:

# ![drawing40right](./assets/images/mdao_mdf.png)

# ## MDAO formulations: distributed vs monolithic (2/2)

# The Sellar problem is a simple and well known test case for MDO formulations:
# \begin{equation}
#     \begin{aligned}
#     & \text{minimize}
#     & & x_{1}^{2} + z_{2} + y_{1} + e^{-y_{2}} \\
#     & \text{with respect to}
#     & & z_{1}, z_{2}, x_{1}\\
#     & \text{subject to}
#     & & \frac{y_{1}}{3.16} - 1 \geq 0
#     & & 1 - \frac{y_{2}}{24} \geq 0
#     & & -10 \geq z_{1} \leq 10
#     & & 0 \geq z_{2} \leq 10
#     & & 0 \geq x_{1} \leq 10
#     \end{aligned}
# \end{equation}
# 
# Where $y_{1} = z_{1}^2 + x_{1} + z_{2} - 0.2 y_{2}$ and $y_{2}=\sqrt{y_{1}} +
# z_{1} + z_{2}$.
# 
# The number of function evaluation is a key metric to assess the computational cost as it enables to avoid considering the performance of the computer used.

# | # Function evaluations      | Discipline 1 | Discipline 2     |
# | :---        |    :----:   |          ---: |
# | IDF      | 60       | 50   |
# | MDF      | 222       | 216   |
# | CO      | 5647       | 8252   |
# | BLISS      | 3344       | 3130   |
# | BLISS-2000      | 818       | 108   |

# In the context of sizing we are particularly interested in computation time as we are in a decision making process. Hence, we generally use monolithic formulations.

# ## Monolithic formulations: High dynamic EMA case study

# ![drawing50](./assets/images/coupled_system.png)

# \begin{equation}
# T_{em} = J_{mot} \cdot A_{max}\frac{N_{red}}{p} + F_{ema} \frac{p}{N_{red}}
# \label{eq_1}
# \end{equation}
# 
# \begin{equation}
# J_{mot} = J_{mot_{ref}} \cdot \left(\frac{T_{em}}{T_{em_{ref}}}\right)^{\frac{5}{3.5}}
# \label{eq_2}
# \end{equation}
# 
# \begin{equation}
# \Omega_{mot} = \Omega_{mot_{ref}} \cdot  \left(\frac{T_{em}}{T_{em_{ref}}}\right)^{-\frac{1}{3.5}}
# \label{eq_3}
# \end{equation}
# 
# \begin{equation}
# \Omega_{mot} \geq V_{max}\cdot \frac{N_{red}}{p}
# \label{eq_4}
# \end{equation}
# 
# \begin{equation}
# M_{mot} = M_{mot_{ref}} \cdot \left(\frac{T_{em}}{T_{em_{ref}}}\right)^{\frac{3}{3.5}}
# \label{eq_5}
# \end{equation}

# \begin{equation}
#     \begin{aligned}
#     & \text{minimize}
#     & & M_{mot} \\
#     & \text{with respect to}
#     & &  N_{red}\\
#     & \text{subject to}
#     & & V_{max} \cdot \frac{N_{red}}{p} - \Omega_{mot} \leq 0
#     \end{aligned}
# \end{equation}

# ## Monolithic formulations: MultiDisciplinary Feasible (MDF)

# ![drawing50](./assets/images/mdf.png)

# \begin{equation}
#     \begin{aligned}
#     & \text{minimize}
#     & & M_{mot} \\
#     & \text{with respect to}
#     & &  N_{red}\\
#     & \text{subject to}
#     & & V_{max} \cdot \frac{N_{red}}{p} - \Omega_{mot} \leq 0
#     \end{aligned}
# \end{equation}

# ## Monolithic formulations: Individual Discipline Feasible (IDF)

# ![drawing50](./assets/images/idf.png)

# ## Monolithic formulations: Hybrid

# ![drawing50](./assets/images/hybrid.png)

# ## Monolithic formulations: Normalized Variable Hybrid (NVH)

# ![drawing50](./assets/images/nvh.png)

# \begin{equation}
#     \begin{aligned}
#     & \text{min.}
#     & & M_{mot} \\
#     & \text{w.r.t}
#     & &  N_{red}, k_{os}\\
#     & \text{s.t.}
#     & & V_{max} \cdot \frac{N_{red}}{p} - \Omega_{mot} \leq 0 \\
#     & & & J_{mot} \cdot A_{max}\frac{N_{red}}{p} + F_{ema} \frac{p}{N_{red}} - T_{em} \leq 0
#     \end{aligned}
# \end{equation}

# ## Monolithic formulations: Performance comparison

# ![drawing50](./assets/images/formulations_comparison.png)

# The NVH formulation is an intrusive formulation as it requires to redefine the optimization problem and models. However, it provides significant reduction of computational cost.
