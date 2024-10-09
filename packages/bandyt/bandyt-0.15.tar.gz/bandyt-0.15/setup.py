from setuptools import setup, find_packages

setup(
    name='bandyt',                   # Your module's name
    version='0.15',                      # Initial release version
    packages=['bandyt'],           # Automatically find packages in your project
    install_requires=[                  # Dependencies
        'numpy',
        'pandas',
        'seaborn',
        'matplotlib',
        'pydot',
        'igraph'
    ],
    description='A brief description of your module',
    long_description=open('README.md').read(),  # Optional: Content of your README file
    long_description_content_type='text/markdown',  # Optional: README file type
    url='https://github.com/bandyt-group/bandyt',  # URL to your GitHub repository
    author='Elizaveta Mukhaleva, Babgen Manookian, Grigoriy Gogoshin, Nagarajan Vaidehi, Andrei Rodin, Sergio Branciamore',
    author_email='bandyt-group@gmail.com',
    license='MIT',                      # License type
    classifiers=[                       # Optional metadata
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',            # Minimum Python version requirement
)
