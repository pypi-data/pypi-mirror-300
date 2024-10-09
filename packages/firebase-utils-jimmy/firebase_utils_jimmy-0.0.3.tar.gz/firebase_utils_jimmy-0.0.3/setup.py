from setuptools import setup, find_packages

setup(
  name='firebase_utils_jimmy',
  version='0.0.3',
  author='Jimmy Q',
  author_email='jaime.quinones.t@gmail.com',
  description='Librería con funciones utiles y seguras para la interacción con Firestore.',
  long_description=open("README.md").read(),
  url='https://github.com/Serialk89/lib-python-base.git',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  python_requires='>=3.11',
  install_requires=[
    'firebase-admin'
  ],
)