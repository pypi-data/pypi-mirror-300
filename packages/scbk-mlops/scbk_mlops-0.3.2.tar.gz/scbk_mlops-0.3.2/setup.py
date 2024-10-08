from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='scbk_mlops',
    version='0.3.2',
    author='Jong Hwa Lee, Jin Young Kim', 
    author_email='jonghwa.jh.lee@sc.com, jinyoung.jy.kim@sc.com',
    description='Local version of MLOps intended for limited capabilities (no DB connection) under network segregation',
    long_description=open('README.md', encoding='utf-8', errors= 'ignore').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/scbk-datascience/scbk-mlops',
    packages=find_packages(exclude=["tests", "tests.*","compilation.py","model_card","model_card.*"]),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
