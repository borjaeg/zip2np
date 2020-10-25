from setuptools import find_packages, setup

setup(
    name='pyeden',
    packages=find_packages(include=['pyeden']),
    version='0.1.0',
    description='Library for downloading EDEN datasets',
    author='SFT Group',
    license='MIT',
    install_requires=[
          'requests',
          'numpy',
          'glob3',
          'tqdm',
          'opencv-python'
      ]
)