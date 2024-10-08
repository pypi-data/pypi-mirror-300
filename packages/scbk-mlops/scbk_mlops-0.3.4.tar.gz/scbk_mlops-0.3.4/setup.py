from setuptools import setup, find_packages

setup(
    name='scbk_mlops',
    version='0.3.4',
    author='Jong Hwa Lee, Jin Young Kim', 
    author_email='jonghwa.jh.lee@sc.com, jinyoung.jy.kim@sc.com',
    description='Local version of MLOps intended for limited capabilities (no DB connection) under network segregation',
    long_description=open('README.md', encoding='utf-8', errors= 'ignore').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/scbk-datascience/scbk-mlops',
    packages=find_packages(exclude=["tests", "tests.*","compilation.py","model_card","model_card.*"]),
    install_requires=['arfs>=2.3.2','evidently>=0.4.38','fairlearn>=0.10.0','imbalanced-learn>=0.12.4'
                      ,'Jinja2>=3.1.4','jupyterlab>=4.2.5','lightgbm>=4.5.0','lime>=0.2.0.1','matplotlib>=3.7.5'
                      ,'mlflow>=2.16.2','numpy==1.26.4','pandas==2.1.4','pyarrow==17.0.0','pycaret==3.3.2','scikit-learn==1.4.2'
                      ,'scipy==1.11.4','seaborn==0.13.2','shap==0.46.0','statsmodels==0.14.4','sweetviz==2.3.1','wordcloud==1.9.3','xlwings==0.33.1'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    include_package_data=True,
)
