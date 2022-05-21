from setuptools import setup

setup(
    name='onceler',
    version='0.1.0',
    description='A CLI tool that allows a user to execute livemedia-creator from a config file.',
    author='Cappy Ishihara',
    author_email='cappy@cappuchino.xyz',
    install_requires=[
        "pykickstart",
        "toml",
        "lorax",
    ],
    include_dirs=["onceler"],
    include_package_data=True,
    packages=["onceler"],
    package_dir={"onceler": "onceler"},
    entry_points={"console_scripts": [
            "onceler=onceler.__main__:main",
            ]},
)