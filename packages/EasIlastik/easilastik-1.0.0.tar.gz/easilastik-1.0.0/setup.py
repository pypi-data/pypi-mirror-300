from setuptools import setup, find_packages

setup(
    name='EasIlastik',
    version='1.0.0',
    author='Titouan Le Gourrierec',
    author_email='titouanlegourrierec@icloud.com',
    url='https://github.com/titouanlegourrierec/EasIlastik',
    README='README.md',
    CHANGELOG='CHANGELOG.md',
    description='This package provides seamless integration of pre-trained image segmentation models from Ilastik into Python workflows, empowering users with efficient and intuitive image segmentation capabilities for diverse applications.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'h5py',
        'opencv-python'
    ],
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
)