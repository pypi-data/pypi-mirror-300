from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="prusek_spheroid",
    version="6.6",
    description="Spheroid segmentation package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Michal Prusek",
    author_email="prusemic@cvut.cz",
    url="https://github.com/michalprusek/prusek-spheroid",
    packages=["prusek_spheroid"],
    install_requires=[
        'numpy==1.26.0',
        'opencv-python==4.8.1',
        'scikit-image==0.22.0',
        'scikit-learn==1.3.2',
        'shapely==2.0.2',
        'threadpoolctl==3.2.0',
        'matplotlib==3.8.1',
        'rasterio==1.3.9',
        'pandas==2.1.3',
        'openpyxl==3.1.2',
        'torch==2.1.1',
        'imagehash==4.3.1',
        'joblib==1.3.2'
    ],
)

