#/*-----------------------------------------------------------------*/
#/*! 
#  \file setup.py 
#  \brief Python installer for calceph library
#
#  \author  M. Gastineau 
#           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
#
#   Copyright, 2016-2024, CNRS
#   email of the author : Mickael.Gastineau@obspm.fr
#*/
#/*-----------------------------------------------------------------*/
# 
#/*-----------------------------------------------------------------*/
#/* License  of this file :
# This file is "triple-licensed", you have to choose one  of the three licenses 
# below to apply on this file.
# 
#    CeCILL-C
#    	The CeCILL-C license is close to the GNU LGPL.
#    	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
#   
# or CeCILL-B
#        The CeCILL-B license is close to the BSD.
#        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
#  
# or CeCILL v2.1
#      The CeCILL license is compatible with the GNU GPL.
#      ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
# 
#
# This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under 
# French law and abiding by the rules of distribution of free software.  
# You can  use, modify and/ or redistribute the software under the terms 
# of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA  
# at the following URL "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
# */
# /*-----------------------------------------------------------------*/

# see http://docs.cython.org/en/latest/src/tutorial/clibraries.html
# require to install Cython.Distutils
#  pip install Cython
# execute  : python setup.py sdist

import logging
import sysconfig
from setuptools import setup, Extension
from setuptools.command.install import install
from setuptools.command.build_clib import build_clib
from setuptools.command.build_ext import build_ext
from subprocess import  check_call
import os
import shutil
import sys
import platform
import tempfile
from os import path
import Cython
from Cython.Build import cythonize

class custom_build_ext(build_ext):
    def run(self):
        self.run_command('build_clib')
        build_ext.run(self)

class custom_build_clib(build_clib):
    def run(self):
        cc, cflags = sysconfig.get_config_vars('CC','CFLAGS')
        build_temp = self.build_temp
        try:
            os.makedirs(build_temp)
        except FileExistsError:
            pass
        # Destination for headers and libraries is build_clib.
        extdir = cwd
        build_clib = os.path.realpath(self.build_clib)
        env = dict(os.environ)
        sourcedir = os.path.abspath('')
        print('extdir:', extdir)
        print('sourcedir:', sourcedir)
        print('cc:', cc)
        print('cflags:', cflags)
        cmd = ["cmake", '-DENABLE_PYTHON=ON',
                '-DENABLE_PYTHON_TESTS=OFF',
                '-DENABLE_FORTRAN=OFF',
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=' + extdir,
                sourcedir
               ] 
        logging.info('%s', ' '.join(cmd))
        check_call(cmd, env=dict(env, PYTHON=sys.executable), cwd=build_temp)           
        check_call(['cmake', '--build', '.'], env=env, cwd=build_temp)   
#        print('listing:')
#        files = [f for f in os.listdir() if os.path.isfile(f)]
#        print(files)       

DOC_URL = 'https://calceph.imcce.fr/docs/4.0.1/html/python/index.html'

cwd = os.path.dirname(os.path.abspath(__file__))
print('current directory :', cwd)

# add noexcept decoration if required
calcephpypyx = 'calcephpy_prev_3_0.pyx'
if (Cython.__version__ >= "3.0.0"):
    calcephpypyx = 'calcephpy_after_3_0.pyx'

setup(
    name='calcephpy',
    version='4.0.1',
    description='Python interface for the CALCEPH Library',
    long_description="""CALCEPH library
===============           

This library is designed to access the binary planetary ephemeris files, such INPOPxx, JPL DExxx and SPICE ephemeris files.
This library provides a C Application Programming Interface (API) and, optionally, Fortran 77/2003, Python 2/3 and Octave/Matlab interfaces to be called by the application

This library  is developed by the "Astronomy and Dynamical System" team
at  IMCCE, Observatoire de Paris, CNRS, PSL Research University, Sorbonne Universite,  (PARIS).  


Installation
------------

.. image:: https://badge.fury.io/py/calcephpy.svg
    :target: https://badge.fury.io/py/calcephpy
    
NumPy should be already installed.

.. code:: python

    pip install calcephpy


Sources
-------

The library is available at :  https://www.imcce.fr/inpop/calceph


""",
    author='Mickael Gastineau',
    author_email='inpop.imcce@obspm.fr',
    url='https://www.imcce.fr/inpop/calceph/',
    license='CeCILL-C or CeCILL-B or CeCILL v2.1',
    classifiers=[ 'Topic :: Scientific/Engineering :: Astronomy', 'Topic :: Software Development :: Libraries' ],
    cmdclass = {'build_ext':  custom_build_ext, 'build_clib':  custom_build_clib},
    ext_modules = cythonize([
        Extension("calcephpy", [os.path.join("pythonapi/src/",calcephpypyx)],
              include_dirs = ["src"], 
              library_dirs = [ cwd ],
              libraries=["calceph"],
        )
    ]),
    install_requires=['setuptools>=20.4', 'cython>=0.27', 'numpy']
)
