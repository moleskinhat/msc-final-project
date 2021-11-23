from setuptools import setup, find_packages
from setuptools.command.install import install


class InstallNltkDependencies(install):
    """ Custom command to install nltk dependencies
    """

    def run(self):
        install.run(self)
        import nltk
        for dependency in ['stopwords', 'punkt']:
            nltk.download(dependency)


setup(
    name="poetry-analyser",
    version="0.0.1",
    description="Poetry analyzer tool for close reading.",
    author="Sam Baderman",
    author_email="sbader01@dcs.bbk.ac.uk",
    packages=find_packages(
        where="src",
        include=["*"],
        exclude=["test"]
    ),
    package_dir={"": "src"},
    cmdclass={'install': InstallNltkDependencies},
    setup_requires=[
        'nltk==3.5'
    ],
    install_requires=[
        "cmudict==0.4.5",
        "pronouncing==0.2.0",
        "nltk==3.5",
    ],
    test_requires=[
        "pytest==6.2.1"
    ],
    entry_points={
        'console_scripts': [
            'poetry_analyser = poetry_analyser:main'
        ]
    }
)
