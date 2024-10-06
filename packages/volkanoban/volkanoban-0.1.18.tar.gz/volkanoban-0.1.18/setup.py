# setup.py

from setuptools import setup, find_packages

setup(
    name='volkanoban',  # Package name
    version='0.1.18',  # Version number
    description='A stacking classifier with advanced explainability and visualization features',
    long_description=open('README.md').read(),  # Use the README file for long description
    long_description_content_type='text/markdown',  # Markdown format for long description
    author='Dr. Volkan OBAN',  # Your name
    author_email='volkanobn@gmail.com',  # Your email
    packages=find_packages(),  # Automatically find the package directories
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'xgboost',
        'lightgbm',
        'catboost',
        'lime',
        'explainerdashboard',
        'plotly',
        'tabulate',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',  # Support Python 3
        'License :: OSI Approved :: MIT License',  # Choose the license
        'Operating System :: OS Independent',  # OS compatibility
        'Development Status :: 4 - Beta',  # Package status
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.8',  # Minimum Python version
)
