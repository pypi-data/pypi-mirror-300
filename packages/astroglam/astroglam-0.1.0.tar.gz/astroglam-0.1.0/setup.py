from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")
# Setup
setup(
 name="astroglam",
 version="0.1.0",
 description="A code to leverage ALMA and JWST data to infer the gas density, metallicity, and burstiness of galaxies.",
 long_description=long_description,
 long_description_content_type="text/markdown",
 url="https://github.com/lvallini/",
 author="Livia Vallini",
 author_email="livia.vallini@inaf.it",
 classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License", 
"Operating System :: OS Independent",
"Topic :: Scientific/Engineering :: Astronomy",
"Intended Audience :: Science/Research"
 ],
 package_dir={"": "src"},
 packages=find_packages(where="src"),
 include_package_data=True,
 package_data={
 "": ["resources/*.csv"],
 "": ["docs/*.ipynb"],
 },
 python_requires=">=3.9, <4",
 install_requires=[
  'contourpy>=1.2.0',
  'corner>=2.2.2',
  'cycler>=0.11.0',
  'emcee>=3.1.6',
  'fonttools>=4.51.0',
  'h5py>=3.11.0',
  'kiwisolver>=1.4.4',
  'matplotlib>=3.9.2',
  'numpy<2.0',
  'packaging==24.1',
  'pillow>=10.4.0',
  'pip>=24.2',
  'PyNeb>=1.1.16',
  'pyparsing>=3.1.2',
  'python-dateutil>=2.9.0.post0',
  'scipy>=1.13.1',
  'setuptools>=59',
  'six>=1.16.0',
  'tornado>=6.4.1',
  'unicodedata2>=15.1.0',
  'wheel>=0.44.0',
  "tqdm>=4.66.5",
],
 project_urls={ # Optional

 "Bug Reports": "https://github.com/lvallini/MCMC_galaxyline_analyzer",
 "Source": "https://github.com/lvallini/MCMC_galaxyline_analyzer",
 },
)
