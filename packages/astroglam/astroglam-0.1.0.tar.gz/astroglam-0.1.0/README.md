# General purpose and references

GLAM is a Python software that will allow you to derive the gas density, metallicity, and deviations from the Kennicutt-Schmidt relation of a galaxy with known star formation rate surface density (Sigma_SFR), known [CII] surface brightness, and known surface brightness of an ionized gas tracer (e.g. Halpha, [OIII]5007, [OIII]88um, ...).
Details on the rationale, the model implementation, and on the equations are discussed in the following papers:
 
  - <a href="https://ui.adsabs.harvard.edu/abs/2021arXiv210605279V/abstract">Vallini et al. 2021</a>
  - <a href="https://ui.adsabs.harvard.edu/abs/2020MNRAS.495L..22V/abstract">Vallini et al. 2020</a> 
  - <a href="https://ui.adsabs.harvard.edu/abs/2019MNRAS.489....1F/abstract">Ferrara et al. 2019</a> 

# Requirements
The code is tested for Python >3.9.  It **requires** <a href="https://github.com/Morisset/PyNeb_devel">Pyneb</a>, 
<a href='https://emcee.readthedocs.io/en/stable'>emcee</a>,  <a href="https://corner.readthedocs.io/en/latest/index.html">corner</a>.

## Acknowledging this code in Scientific Publications

<div class="row codice">
<pre><code><span>@ARTICLE{Ferrara:2019,
       author = <span>{</span> {Ferrara}, A. and {Vallini}, L. and {Pallottini}, A. and {Gallerani}, S. and {Carniani}, S.
                 and {Kohandel}, M. and {Decataldo}, D. and {Behrens}, C.},
        title = "{A physical model for [C II] line emission from galaxies}",
      journal = {\mnras},
         year = 2019,
        month = oct,
       volume = {489},
       number = {1},
        pages = {1-12},
          doi = {10.1093/mnras/stz2031},
archivePrefix = {arXiv},
       eprint = {1908.07536},
 primaryClass = {astro-ph.GA},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2019MNRAS.489....1F},
   }</span></code>
</pre>
</div>


<div class="row codice">
<pre><code><span>@ARTICLE{Vallini2021,
       author = <span>{</span>{Vallini}, L. and {Ferrara}, A. and {Pallottini}, A. and {Carniani}, S. and {Gallerani}, S.},
        title = "{High [OIII]/[CII] surface brightness ratios trace early starburst galaxies}",
      journal = {arXiv e-prints},
     keywords = {Astrophysics - Astrophysics of Galaxies},
         year = 2021,
        month = jun,
          eid = {arXiv:2106.05279},
        pages = {arXiv:2106.05279},
archivePrefix = {arXiv},
       eprint = {2106.05279},
 primaryClass = {astro-ph.GA},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2021arXiv210605279V},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System},
}</span></code>
</pre>
</div>

## Funding
This work is supported by the ERC Advanced Grant INTERSTELLAR H2020/740120 (PI: Ferrara). 

Part of the work of LV has been supported by funding from the EU Horizon 2020 research and innovation program under the Marie Sklodowska-Curie Grant agreement No. 746119. 

