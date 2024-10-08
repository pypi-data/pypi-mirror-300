from __future__ import print_function
import numpy as np
import os
from multiprocessing import Pool
import emcee
from astroglam.emission_models import Delta, Sigma_CII158, Sigma_OIII88, Sigma_OIII52, Sigma_OIII5007, Sigma_CIII
from astroglam.empirical import delooze_fit_resolved

class galaxy_template:

    def __init__(
        self,
        Sigma_SFR=2.0,  # Msun/yr/kpc
        Sigma_CII=3.0e7,  # Lsun/kpc^2
        Sigma_ion=7.0e7  # Lsun/kpc^2
        #
        ,
        rel_err_Sigma_CII=0.2,  # relative error on the SigmaCII
        rel_err_Sigma_ion=0.2,  # relative error on the SigmaOIII
        rel_err_Delta=0.2,  # relative error on the Delta
        ion_tracer='88um',
    ):

        # setup the template for the data
        #
        self.Sigma_SFR = None  # Msun/yr/kpc^2
        self.Sigma_CII = None  # Lsun/kpc^2
        self.Sigma_ion = None  # Lsun/kpc^2
        #
        self.rel_err_Sigma_CII = None
        self.rel_err_Sigma_ion = None
        self.rel_err_Delta = None
        
        self.ion_tracer= None

        # set the input errors
        self.set_relative_errors(
            rel_err_Sigma_CII=rel_err_Sigma_CII,
            rel_err_Sigma_ion=rel_err_Sigma_ion,
            rel_err_Delta=rel_err_Delta,
        )

        # set the input data
        self.set_data(Sigma_SFR=Sigma_SFR, Sigma_CII=Sigma_CII, Sigma_ion=Sigma_ion, ion_tracer=ion_tracer)

    def set_relative_errors(
        self, rel_err_Sigma_CII=None, rel_err_Sigma_ion=None, rel_err_Delta=None
    ):

        if rel_err_Sigma_CII is not None:
            self.rel_err_Sigma_CII = rel_err_Sigma_CII
        if rel_err_Sigma_ion is not None:
            self.rel_err_Sigma_ion = rel_err_Sigma_ion
        if rel_err_Delta is not None:
            self.rel_err_Delta = rel_err_Delta

    def set_data(self, Sigma_SFR=None, Sigma_CII=None, Sigma_ion=None, ion_tracer=None):

        if Sigma_SFR is not None:
            self.Sigma_SFR = Sigma_SFR
        if Sigma_CII is not None:
            self.Sigma_CII = Sigma_CII
        if Sigma_ion is not None:
            self.Sigma_ion = Sigma_ion
        if ion_tracer is not None:
            self.ion_tracer = ion_tracer

    def data_for_MCMC(self):
        y = np.array([self.Deltagalaxy(), self.Sigma_CII, self.Sigma_ion])
        yerr = np.array(
            [
                self.Deltagalaxy() * self.rel_err_Delta,
                self.Sigma_CII * self.rel_err_Sigma_CII,
                self.Sigma_ion * self.rel_err_Sigma_ion,
            ]
        )

        par = self.Sigma_SFR
        label=self.ion_tracer

        return y, yerr, par, label

    def Deltagalaxy(self):

        out = np.log10(self.Sigma_CII) - np.log10(delooze_fit_resolved(self.Sigma_SFR))

        return out

    def print_info(self):

        print("Galaxy input data")
        print("  ion tracer   = ", self.ion_tracer)
        #
        print("  Sigma_SFR         = ", self.Sigma_SFR, "Msun/yr/kpc^2")
        print("  Sigma_CII         = ", self.Sigma_CII, "Lsun/kpc^2")
        print("  Sigma_ion        = ", self.Sigma_ion, "Lsun/kpc^2")
        #
        print("  relative error on Delta       = ", 100.0 * self.rel_err_Delta, "%")
        print("  relative error on Sigma_CII  = ", 100.0 * self.rel_err_Sigma_CII, "%")
        print(
            "  relative error on Sigma_ion  = ", 100.0 * self.rel_err_Sigma_ion, "%"
        )


class MC_model:

    def __init__(
        self
        # priors
        ,
        lognMIN=0.5,
        lognMAX=3.5,  # minimum and maximum log density [cm-3]
        logkMIN=-1.0,
        logkMAX=2.5,  # minimum and maximum log k_s
        logZMIN=-1.5,
        logZMAX=0.0  # minimum and maximum log metallicity [Zsun]
        #
        # MCMC parameters
        ,
        n_walkers=10,
        steps=200,
        burn_in=50
        #
        # starting point for the walkers
        ,
        logn0=2.0,
        logZ0=-0.5,
        logk0=0.3
        # backend fname
        ,
        bkh_fname=None,
    ):

        # backend init
        self.bkh_fname = None

        # priors for the MCMC
        self.lognMIN = None
        self.lognMAX = None
        self.logkMIN = None
        self.logkMAX = None
        self.logZMIN = None
        self.logZMAX = None

        # walker init
        self.logn0 = None
        self.logZ0 = None
        self.logk0 = None

        # eemc parameters
        self.n_dim = 3
        self.n_walkers = None
        self.steps = None
        self.burn_in = None

        self.galaxy_data = None

        self.pool = None

        self.set_priors(
            lognMIN=lognMIN,
            lognMAX=lognMAX,
            logkMIN=logkMIN,
            logkMAX=logkMAX,
            logZMIN=logZMIN,
            logZMAX=logZMAX,
        )

        self.set_walkers(logn0=logn0, logZ0=logZ0, logk0=logk0)
        self.set_backend(bkh_fname=bkh_fname)
        self.set_mc_parameters(n_walkers=n_walkers, steps=steps, burn_in=burn_in)
       
        self.Y = None
        self.YERR = None
        self.SSFR = None
        self.LINELABEL = None

    def check_consistency(self):

        # check the priors
        ok_priors = self.lognMIN < self.lognMAX
        ok_priors = ok_priors and self.logkMIN < self.logkMAX
        ok_priors = ok_priors and self.logZMIN < self.logZMAX
        if not ok_priors:
            print("Priors look funky, i.e. min >= max for some of them")

        ok_init = self.check_bounds(theta=tuple([self.logn0, self.logZ0, self.logk0]))
        if not ok_init:
            print("Initial position of the walkers is out of the priors")

        ok_data = isinstance(self.galaxy_data, galaxy_template)
        if not ok_data:
            print("galaxy data is not a galaxy_template() class")

        NoneType = type(None)
        no_backend = isinstance(self.bkh_fname, NoneType)
        ok_backend = not (no_backend)
        if not ok_backend:
            print("You need to provide the fname for the backend, use set_backend()")

        return ok_priors and ok_init and ok_data and ok_backend

    def run_model_parallel(self, proc=None):

        ok = self.check_consistency()
        if not ok:
            print("Problem in the initialization, aborting")
        assert ok

        if(1):
            print("about to run (with parallelization) ...")
            self.print_info()
            print("galaxy data")
            self.galaxy_data.print_info()

        # get galaxy data in the format for the MCMC
        y, yerr, par,ll = self.galaxy_data.data_for_MCMC()

        # set them as global variables
        self.set_global(y, yerr, par)
        
        # set the line label as global param as well
        self.set_linelabel_global(ll)
        
        # init walkers
        starting_point = [self.logn0, self.logZ0, self.logk0]
        pos = [
            starting_point + 1e-5 * np.random.randn(self.n_dim)
            for i in range(self.n_walkers)
        ]

        # Set up the backend
        backend = emcee.backends.HDFBackend(self.bkh_fname)
        backend.reset(self.n_walkers, self.n_dim)

        if proc is None:
            with Pool() as pool:
                # set the emcee
                sampler = emcee.EnsembleSampler(
                    self.n_walkers, self.n_dim, self.lnprob_global, pool=pool
                )
                # run the thing
                sampler.run_mcmc(pos, self.steps, progress=True)
                # tau            = sampler.get_autocorr_time(quiet=True)
            flat_samples = sampler.get_chain(discard=self.burn_in, flat=True)
            return flat_samples

        else:
            with Pool(processes=proc) as pool:
                # set the emcee
                sampler = emcee.EnsembleSampler(
                    self.n_walkers, self.n_dim, self.lnprob_global, pool=pool
                )
                # run the thing
                sampler.run_mcmc(pos, self.steps, progress=True)
                # tau            = sampler.get_autocorr_time()
            flat_samples = sampler.get_chain(discard=self.burn_in, flat=True)
            return flat_samples

    def run_model(self, verbose=True):

        ok = self.check_consistency()
        if not ok:
            print("Problem in the initialization, aborting")
        assert ok

        if verbose:
            print("about to run (w/o parallelization)....")
            self.print_info()
            print("galaxy data")
            self.galaxy_data.print_info()

        # get galaxy data in the format for the MCMC
        y, yerr, par, ll = self.galaxy_data.data_for_MCMC()
        

        # init walkers
        starting_point = [self.logn0, self.logZ0, self.logk0]
        pos = [
            starting_point + 1e-5 * np.random.randn(self.n_dim)
            for i in range(self.n_walkers)
        ]

        # Set up the backend
        backend = emcee.backends.HDFBackend(self.bkh_fname)
        backend.reset(self.n_walkers, self.n_dim)

        # set the emcee
        sampler = emcee.EnsembleSampler(
            self.n_walkers,
            self.n_dim,
            self.lnprob,
            args=(y, yerr, par, ll),
            backend=backend,
        )
        # run the thing
        sampler.run_mcmc(pos, self.steps, progress=True)
        tau = sampler.get_autocorr_time(quiet=True)
        flat_samples = sampler.get_chain(discard=self.burn_in, flat=True)

        return flat_samples

    def set_mc_parameters(self, n_walkers=None, steps=None, burn_in=None):

        # set priors for the model
        # if input is None, no change is done
        if n_walkers is not None:
            self.n_walkers = n_walkers
        if steps is not None:
            self.steps = steps
        if burn_in is not None:
            self.burn_in = burn_in

    def set_backend(self, bkh_fname=None):
        # set the name for the bkh file
        # if input is None, no change is done
        if bkh_fname is not None:
            self.bkh_fname = bkh_fname  #

    def set_priors(
        self,
        lognMIN=None,
        lognMAX=None,
        logkMIN=None,
        logkMAX=None,
        logZMIN=None,
        logZMAX=None,
    ):

        # set priors for the model
        # if input is None, no change is done
        if lognMIN is not None:
            self.lognMIN = lognMIN  #
        if lognMIN is not None:
            self.lognMAX = lognMAX  # maximum log density [cm-3]
        if logkMIN is not None:
            self.logkMIN = logkMIN  # minimum log k_s
        if logkMAX is not None:
            self.logkMAX = logkMAX  # maximum log k_s
        if logZMIN is not None:
            self.logZMIN = logZMIN  #
        if logZMAX is not None:
            self.logZMAX = logZMAX  # maximum log metallicity [Zsun]

    def set_galaxy_data(self, galaxy_data=None):
        self.galaxy_data = galaxy_data

    def set_walkers(self, logn0=None, logZ0=None, logk0=None):

        if logn0 is not None:
            self.logn0 = logn0
        if logZ0 is not None:
            self.logZ0 = logZ0
        if logk0 is not None:
            self.logk0 = logk0

    def check_bounds(self, theta):
        logn, logZ, logk = theta

        ok = self.lognMIN < logn < self.lognMAX
        ok = ok and self.logkMIN < logk < self.logkMAX
        ok = ok and self.logZMIN < logZ < self.logZMAX

        return ok

    def model(self, theta, ssfr, ll):

        logn, logZ, logk = theta

        Z, k = 10**logZ, 10**logk

        delta_galaxy = Delta(logn=logn, Z=Z, k=k, Sigma_sfr=ssfr)
        sigma_cii_galaxy = Sigma_CII158(logn=logn, Z=Z, k=k, Sigma_sfr=ssfr)
        
        if(ll=='88um'):
            sigma_ion_galaxy = Sigma_OIII88(logn=logn, Z=Z, k=k, Sigma_sfr=ssfr)
        if(ll=='52um'):
            sigma_ion_galaxy = Sigma_OIII52(logn=logn, Z=Z, k=k, Sigma_sfr=ssfr)
        if(ll=='OIII5007'):
            sigma_ion_galaxy = Sigma_OIII5007(logn=logn, Z=Z, k=k, Sigma_sfr=ssfr)
        if(ll=='CIII'):
            sigma_ion_galaxy = Sigma_CIII(logn=logn, Z=Z, k=k, Sigma_sfr=ssfr)
            
        return delta_galaxy, sigma_cii_galaxy, sigma_ion_galaxy

    def lnlike(self, theta, y, yerr, ssfr, ll):
        mod = np.asarray(self.model(theta=theta, ssfr=ssfr, ll=ll))
        inv_sigma2 = 1.0 / (yerr**2)
        out = -0.5 * (np.sum((y - mod) ** 2 * inv_sigma2))
        return out

    def lnprob(self, theta, y, yerr, ssfr, ll):
        lp = self.lnprior(theta)

        if not np.isfinite(lp):
            out = -np.inf
        else:
            out = lp + self.lnlike(theta, y, yerr, ssfr, ll)

        return out
    
    def lnprior(self,theta):
       #flat priors on logn, logk, and log Z

        ok = self.check_bounds(theta=theta)

        if  ok:
            out = 0.0
        else:
            out = -np.inf
       
        return out
    
    def set_global(self, a, b, c):
        
        self.Y=a
        self.YERR=b
        self.SSFR=c
        
    def set_linelabel_global(self, ll):
        
        self.LINELABEL=ll
        
    
    def model_global(self,theta):

        logn, logZ, logk = theta

        Z, k = 10**logZ, 10**logk

        delta_galaxy = Delta(logn=logn, Z=Z, k=k, Sigma_sfr=self.SSFR)
        sigma_cii_galaxy = Sigma_CII158(logn=logn, Z=Z, k=k, Sigma_sfr=self.SSFR)
        
        if(self.LINELABEL=='88um'):
            sigma_ion_galaxy = Sigma_OIII88(logn=logn, Z=Z, k=k, Sigma_sfr=self.SSFR)
        if(self.LINELABEL=='52um'):
            sigma_ion_galaxy = Sigma_OIII52(logn=logn, Z=Z, k=k, Sigma_sfr=self.SSFR)
        if(self.LINELABEL=='OIII5007'):
            sigma_ion_galaxy = Sigma_OIII5007(logn=logn, Z=Z, k=k, Sigma_sfr=self.SSFR)
        if(self.LINELABEL=='CIII'):
            sigma_ion_galaxy = Sigma_CIII(logn=logn, Z=Z, k=k, Sigma_sfr=self.SSFR)
            
        return delta_galaxy, sigma_cii_galaxy, sigma_ion_galaxy


    def lnlike_global(self,theta):
        mod              = np.asarray(self.model_global(theta=theta))
        inv_sigma2       = 1.0/(self.YERR**2)
        out              = -0.5*(np.sum((self.Y-mod)**2*inv_sigma2))
        return out
   
    
    def lnprob_global(self,theta):
        lp = self.lnprior(theta)

        if not np.isfinite(lp):
            out = -np.inf
        else:
            out = lp + self.lnlike_global(theta)

        return out
    

    def print_info(self):
        print("MC parameters")
        print("  n_walkers", self.n_walkers)
        print("  steps    ", self.steps)
        print("  burn_in  ", self.burn_in)

        print("Priors")
        print(
            "{:10} {:10} {:10}".format(self.lognMIN, "< log(n/cm^-3) <", self.lognMAX)
        )
        print(
            "{:10} {:10} {:10}".format(self.logkMIN, "< log(k_s)     <", self.logkMAX)
        )
        print(
            "{:10} {:10} {:10}".format(self.logZMIN, "< log(Z/Z_sun) <", self.logZMAX)
        )

        print("walkers starting point")
        print("  log n ", self.logn0)
        print("  log Z ", self.logZ0)
        print("  log k ", self.logk0)

        print("Backend fname")
        print("  fname ", self.bkh_fname)
        
        




