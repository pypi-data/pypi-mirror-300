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
    this module contains the analytical eq.s for the cooling rate of various ions
    outpus:
      cooling rates in erg/s/cm-3
    inputs:
      T, the temperature in K
"""

def compute_lambda_CII_h(T):
    
    """
    Maxwellian-averaged collision rates with neutrals
    using expression from Goldsmith et al. 2012
    see Appendix A, Ferrara et al. 2019
    """

    factor = (1.84e-4*(T)**0.64)/2.0
    out    = (8.6293e-6/np.sqrt(T))*factor*(1.602e-12*0.0079)*np.exp((-1.602e-12*0.0079)/(1.38065e-16*T))

    return out

def compute_lambda_CII_e(T):
    """
    Maxwellian-averaged collision rates with e-
    using expression from Goldsmith et al. 2012.
    see Appendix A, Ferrara et al. 2019
    """
    factor= (0.67*(T)**0.13)/2.0
    out   = (8.6293e-6/np.sqrt(T))*factor*(1.602e-12*0.0079)*np.exp((-1.602e-12*0.0079)/(1.38065e-16*T))

    return out


def compute_lambda_CIII_e(T):
    """
    Maxwellian-averaged collision rates with e-
    using expression from Appendix A, Ferrara et al. 2019
    """
    factor=1.265-0.0174e-4*T
    out = (8.6293e-6/np.sqrt(T))*factor*(1.602e-12*6.54)*np.exp((-1.602e-12*6.54)/(1.38065e-16*T))
    
    return out




