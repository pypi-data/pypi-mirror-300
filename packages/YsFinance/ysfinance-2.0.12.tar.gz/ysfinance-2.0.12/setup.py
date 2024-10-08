from setuptools import setup, find_packages

setup(
    name='YsFinance',
    version='2.0.12',
    author='YunSheng',
    author_email='278211638@qq.com',
    description='About finance',
    # url='https://github.com/YunSheng0129/YsFinance.git',
    packages=find_packages(),
    package_data={
        'YsFinance': ['resources/info.derive.finance','resources/stock.calender','resources/stock.basic'],
    },
    install_requires=['pandas<=1.6',
                      'numpy<=1.26',
                      'scipy',
                      'tushare',
                      'scipy',
                      'statsmodels',
                      'joblib',
                      'ipykernel',
                      'empyrical',
                      'scikit-learn',],  # 依赖列表
)

## python setup.py develop
## python setup.py sdist
## twine upload dist/*