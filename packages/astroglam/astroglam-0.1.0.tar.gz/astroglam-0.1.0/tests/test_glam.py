import numpy as np
import astroglam as gl
import corner
import os

if __name__ == '__main__':
       # Instantiate your class and run the method
   

	mcr = gl.MC_model()
	mcr.set_priors(lognMIN = 0.0, lognMAX= 4.5,logZMIN = -2, logZMAX= 0.1, logkMIN = -0.5, logkMAX= 3.5)

	mcr.set_walkers(logn0=1.0,logZ0=-0.66,logk0 = 0.92)
	mcr.set_mc_parameters(n_walkers = 10, steps = 10000, burn_in   = 100)

	galaxy_exampleOIII = gl.galaxy_template()

	# load the cii, ciii, oiii, sfr in the cell

	Sigma_CIIcell=10**7
	Sigma_ioncell=10**7
	Sigma_SFRcell=10.0
	print('THIS IS A TEST RUN: ....')
            
	# run mcmc for oiii
	filename_backendoiii='oiii.h5'
	galaxy_exampleOIII.set_data(Sigma_SFR=Sigma_SFRcell, Sigma_CII=Sigma_CIIcell, Sigma_ion=Sigma_ioncell, ion_tracer='OIII5007')
	galaxy_exampleOIII.set_relative_errors(rel_err_Sigma_CII=0.2, rel_err_Sigma_ion=0.2, rel_err_Delta=0.2)
	mcr.set_backend(bkh_fname=filename_backendoiii)
	mcr.set_galaxy_data(galaxy_data = galaxy_exampleOIII)
	flat_samplesOIII = mcr.run_model()
            
	fig = corner.corner(flat_samplesOIII, labels=["log(n)", r"log(Z/Z$_{\odot}$)", r"log($\kappa_s$)"])

	fig.savefig("test.png")

	print('EXITED OK! GLAM SHOULD WORK FINE')
