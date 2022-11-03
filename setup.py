from setuptools import setup, find_packages


setup(
    name="utils",
    version="0.0.3",
    license="GPLv2+",
    url="https://git.ars-virtualis.org/yul/utils",
    description="Misc utils",
    author_email="aymeric.guth@protonmail.com",
    author="Aymeric Guth",
    packages=find_packages(),
    package_data={"utils": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v2 or later(GPLv2+)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "is_kebab_case=utils.cli:_is_kebab_case",
            "is_snake_case=utils.cli:_is_snake_case",
            "is_lower_case=utils.cli:_is_lower_case",
            "parse_version=utils.cli:_parse_version",
            "generate_eggname=utils.cli:_generate_eggname",
        ]
    },
)
