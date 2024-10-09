from setuptools import setup, find_packages

setup(
    name='nitroflare_uploader',
    version='1.1.0',
    description='A Python package to upload files to Nitroflare',
    author='Zack3D',
    author_email='zack3d@goocat.gay',
    url='https://git.goocat.gay',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0',
        'tqdm>=4.0.0',
        'requests-toolbelt>=0.9.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
