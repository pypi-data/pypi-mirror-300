from setuptools import setup, find_packages

setup(
    name='slyvek-deployer',
    version='0.1.0',
    description='Un package pour déployer et configurer un VPS avec slyvek-setup',
    author='guiguito',
    packages=find_packages(),
    install_requires=[
        'fabric>=2.6.0',
        'requests>=2.32.3'
    ],
    entry_points={
        'console_scripts': [
            'slyvek-deploy = slyvek_deployer.deployer:main',
        ],
    },
)
