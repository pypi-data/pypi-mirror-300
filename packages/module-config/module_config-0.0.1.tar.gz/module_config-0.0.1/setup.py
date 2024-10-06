from setuptools import setup, find_packages

setup(
    name='module_config',
    version='0.0.1',
    author='Pablo Vergara',
    author_email='vergarapablo2001@gmail.com',
    description='A simple configuration manager for Python applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pablove2001/module-config',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)