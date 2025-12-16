import setuptools
from pathlib import Path

root_dir = Path(__file__).absolute().parent

with (root_dir / "VERSION").open() as f:
    version = f.read().strip()

with (root_dir / "README.md").open() as f:
    long_description = f.read()

with (root_dir / "requirements.in").open() as f:
    requirements = f.read().splitlines()


setuptools.setup(
    name="gn_module_quadrige",
    version=version,
    description="Module d’intégration des données Quadrige pour GeoNature",
    long_description=long_description,
    long_description_content_type="text/x-rst",

    maintainer="Basile André",
    maintainer_email="basile.andre@developpement-durable.gouv.fr",
    url="https://github.com/basileandre056/gn_module_quadrige",

    # Backend packages
    packages=setuptools.find_packages("backend"),
    package_dir={"": "backend"},

    include_package_data=True,
    package_data={
        "gn_module_quadrige": [
            "static/*",
            "templates/*",
            "migrations/data/*.sql",
        ]
    },

    install_requires=requirements,
    zip_safe=False,

    # Points d’entrée GeoNature
    entry_points={
        "gn_module": [
            "code = gn_module_quadrige:MODULE_CODE",
            "picto = gn_module_quadrige:MODULE_PICTO",
            "blueprint = gn_module_quadrige.blueprint:blueprint",
            "config_schema = gn_module_quadrige.config_schema_toml:GnModuleSchemaConf",
            "migrations = gn_module_monitoring:migrations",


        ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: French",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
