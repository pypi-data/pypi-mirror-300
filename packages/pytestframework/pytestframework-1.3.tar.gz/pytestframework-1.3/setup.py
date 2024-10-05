from setuptools import setup, find_packages

setup(
    name='pytestframework',
    version='1.3',
    author="Yogesh C",
    author_email="Ykotha@munichre.digital",    
    packages=find_packages(),
    description='Pytest framework project',
    install_requires=[        
        "pytest>=7.4.4",        
        'playwright>=1.40.0'
    ]
)
