# setup.py

from setuptools import setup, find_packages

setup(
    name='volkanoban',  # Name of your package
    version='0.1.20',  # Version of your package
    description='A powerful stacking classifier framework that integrates advanced machine learning techniques and some deep learning techniques, overfitting prevention, and explainability features such as LIME, SHAP, and model interpretation dashboards.',
    long_description=open('README.md').read(),  # Use README for long description
    long_description_content_type='text/markdown',  # Markdown format for long description
    author='Dr. Volkan OBAN',  # Your name
    author_email='volkanobn@gmail.com',  # Your email
    packages=find_packages(),  # Automatically find package directories
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'xgboost',
        'lightgbm',
        'catboost',
        'lime',
        'shap',
        'explainerdashboard',
        'plotly',
        'tabulate',
        'torch',  # PyTorch is required for TabNetClassifier
        'pytorch-tabnet',  # PyTorch TabNet library
    ],
    classifiers=[  # Metadata about the package
        'Programming Language :: Python :: 3',  # Supported programming language
        'Operating System :: OS Independent',  # Compatibility with different operating systems
        'Development Status :: 4 - Beta',  # Indicates that the package is in a beta stage of development
        'Intended Audience :: Developers',  # Target audience: developers
        'Intended Audience :: Science/Research',  # Target audience: researchers in AI and data science
        'Topic :: Scientific/Engineering :: Artificial Intelligence',  # Focus on AI and scientific applications
    ],
    python_requires='>=3.8',  # Specify the minimum version of Python required
)

