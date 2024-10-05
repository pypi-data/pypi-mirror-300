from setuptools import setup, find_packages

setup(
    name="bizflow-db-helper",
    version="0.1.2",
    packages=['bizflow_db_helper'],
    install_requires=[
        "oracledb",
        "pandas",
        "bcpy",
        "sqlalchemy",
        "numpy",
        "pyodbc",
        "psycopg2",
    ],
    extras_require={
        'dev': ['wheel']
    },
    author="littlekeixi",
    author_email="littlekeixi@gmail.com",
    description="A helper module for database operations",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)