from setuptools import setup, find_packages


setup(
    name='dayana-endostat',
    version='0.1.0',
    author='Ashik Sanyo',
    author_email='ashiksanyo01@gmail.com',
    description='A library for clinical & statistical calculations in Endodontics',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
    packages=find_packages(),
    install_requires=[
        'numpy', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
