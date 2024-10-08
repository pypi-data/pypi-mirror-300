# glam: Galaxy Line Analyzer with MCMC
#Copyright (c) 2024 Livia Vallini

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
import numpy as np

"""
  this module contains the equations to compute the ionization structure
  inputs:
    U is the ionzation parameter
    Z is the metallicity in Zsun
  outputs:
    column densities, measured in cm^-2
"""

def compute_Ni(U,Z):
    """
    Column density of the ionized gas
    Eq. 14 in Ferrara et al. 2019. 
    """
    ND     = compute_Nd(Z)
    tau_sd = (1e+23*U)/ND
    NN     = ND*np.log((1+tau_sd)/(1+(tau_sd/np.exp(1.0))))
    return NN

def compute_Nd(Z):
    """
    Column density corresponding to A_V = 1 
    Eq. 9c in Ferrara et al. 2019
    """
    Ndsolar=1.7e21 #cm^-2
    return Ndsolar/Z

def compute_chi_of_U(Z):
    """
    Eq. 22 in Ferrara et al. 2019
    """
    
    chi = 8.7e+4*Z

    return chi

def compute_chi_prime(U, Z):
    """
    Eq. 22b in Ferrara et al. 2019
    """
    ww       = compute_w_of_D(Z)
    chi      = compute_chi_of_U(U)
    chiprime = ww*chi
    return chiprime

def compute_w_of_D(Z):
    """
    Factor related to the abs. of LW photons
    see Eq. 24 in Ferrara et al. 2019 (see also Sternberg et al. 2014)
    """
    w = 1.0/(1.0+ 0.9*(Z)**0.5)
    return w

def compute_NF(U,Z):
    """
    Column density at which the Lyman-Werner flux vanishes
    Eq. 28 Ferrara et al. 2019
    """
    ND  = compute_Nd(Z)
    out = ND*np.log(1+compute_chi_prime(U,Z))
    return out

def compute_NHIyi(U, Z):
    """
    HI column in the ionized layer
    Eq. 13 and 14 in Ferrara et al. 2019
    """
    Ns     = 1e+23*U
    tau_s  = 2.7e+5 * U
    out    = (Ns/tau_s) * (1.0 - compute_Ni(U,Z)/compute_Nd(Z))
    return out

def compute_NHIy0(U, Z, N0):
    """
    Ionized column density in the case of the density bounded regime
    Eq. 33 in Ferrara et al. 2019
    """
    Ns      = 1e+23*U
    y0      = N0/Ns
    tau_sd  = 59.0 * U * Z
    tau_s   = 2.7e+5 * U
    out     = (Ns/tau_s) * np.log(tau_sd/np.abs((np.exp(tau_sd*y0)-tau_sd-1.0)))
    return out


