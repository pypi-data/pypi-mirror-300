from setuptools import setup, find_packages

setup(
    name='aifn',
    version='0.0.1',
    description='AI Function Python package that makes build and deploy AI features faster',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Weco Team',
    author_email='contact@weco.ai',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License:: OSI Approved :: MIT License',
        'Operat ing System :: OS Independent',
    ] ,
    python_requires='>=3.8' ,
)

