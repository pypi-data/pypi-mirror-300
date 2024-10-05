from setuptools import setup, find_packages

setup(
    name='rlpp',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'pygame',                      # Required for game development
        'pyqt5>=5.15.9',               # GUI framework
        'pyqt5-tools>=5.15.9.3.3',     # Tools for Qt Designer and other utilities
        'opencv-python',        # For image processing
        'opencv-contrib-python',  # Additional OpenCV functionality
        'numpy',                       # For numerical operations
    ],
    entry_points={
        'console_scripts': [
            'rlpp_designer = rlpp.rlpp_designer:main',  # Assuming main() is your entry function
        ],
    },
    # Additional metadata
    author='Uriel Garcilazo Cruz',                 # Replace with your name
    author_email='garcilazo.uriel@gmail.com',  # Replace with your email
    description='A GUI tool for building Pygame applications and Reinforcement Learning',
    long_description=open('README.md').read(),  # Ensure you have a README.md file for a long description
    long_description_content_type='text/markdown',
    url='https://github.com/UGarCil/The_RL_Playground_with_python',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Specify the Python version requirement
)