from setuptools import setup, find_packages

setup(
    name='sales_forecasting',  # Replace with your custom package name
    version='0.4.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'scikit-learn',
        'numpy',
        'joblib'
    ],
    description="A sales forecasting package based on date features",
    author="Anik",
    author_email="anik.dip@gmail.com",
)