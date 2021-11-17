from setuptools import setup

TEST_DEPS = ["pytest==5.0.1", "pytest-runner==5.1", "pytest-cov==2.7.1", "nox"]

setup(
    name="wst_nachine",
    author="Abdellah EL YOUNSI",
    author_email="abdel.ely.ds@gmail.com",
    url="https://github.com/abdel-ely-ds/trading-pytrader",
    keywords="core",
    license="MIT",
    description="ws backtest strategies",
    long_description="file: README.md",
    classifiers=["Programming Language :: Python :: 3.7"],
    zip_safe=True,
    include_package_data=True,
    entry_points={"console_scripts": ["ws-just-tradeit=wst_nachine.main:main"]},
    package_dir={"": "src"},
    install_requires=["uvicorn", "fastapi"],
    tests_require=TEST_DEPS,
    extras_require={"test": TEST_DEPS},
)