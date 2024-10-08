from setuptools import setup, find_packages

setup(
    name='EnergyEfficientAI',  # Name of your library
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'numpy', 
        'psutil', 
        'scikit-learn',
        'seaborn'
    ],
    entry_point = {
        "console_scripts":[
            "EnergyEfficientAI = EnergyEfficientAI:Message",
        ],
    },
    author='Uzair Hassan, Zia Ur Rehman, Saif Ul Islam',
    description='A library to calculate power, energy, and training time of machine learning algorithms',
    long_description=open('README.md').read(),  # Assumes you have a README.md file
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    # url='https://github.com/yourusername/energy_ml_lib',  # Add your repo if any
)
