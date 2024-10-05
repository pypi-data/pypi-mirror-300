from setuptools import setup, find_packages # type: ignore

setup(
    name='cryptonest',
    version='0.1.0',
    description='API de chiffrement avec RSA et ChaCha20 pour la protection des données',
    author='Votre Nom',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'cryptography',
    ],
)
