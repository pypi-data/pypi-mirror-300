from setuptools import setup, find_packages

setup(
    name='udkm1Dsim',
    version='2.0.4',
    packages=find_packages(),
    package_data={
        'udkm1Dsim': ['parameters/atomic_form_factors/chantler/*.cf',
                      'parameters/atomic_form_factors/chantler/*.md',
                      'parameters/atomic_form_factors/henke/*.nff',
                      'parameters/atomic_form_factors/henke/*.md',
                      'parameters/atomic_form_factors/cromermann.txt',
                      'parameters/magnetic_form_factors/*.mf',
                      'parameters/elements.dat',
                      'matlab/*.m',
                      ],
    },
    url='https://github.com/dschick/udkm1Dsim',
    install_requires=['tqdm>=4.43.0',
                      'numpy>=1.18.2,<2.0.0',
                      'pint>=0.23',
                      'scipy>=1.4.1',
                      'sympy>=1.5.1',
                      'tabulate',
                      'matplotlib>=2.0.0'],
    extras_require={
        'parallel':  ['dask[distributed]>=2.6.0'],
        'testing': ['flake8', 'pytest'],
    },
    license='MIT',
    author='Daniel Schick',
    author_email='schick.daniel@gmail.com',
    description='A Python Simulation Toolkit for 1D Ultrafast Dynamics '
                + 'in Condensed Matter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.9',
    keywords='ultrafast dynamics condensed matter 1D '
            + 'NTM 3TM 2TM TTM N-temperature model '
            + 'coherent acoustic phonons sound strain waves '
            + 'resonant magnetic scattering diffraction spectroscopy '
            + 'x-ray magnetic circular dichroism '
            + 'Landau Lifschitz Bloch ',
)
