from setuptools import setup, find_packages

setup(
    name='beth-smallo-interpreter',
    version='0.1.0',
    author='Viktor A. Rozenko Voitenko',
    author_email='sharp.vik@gmail.com',
    description='Beth is an assembler + VM bundle for SmallO written in Python. She runs your SmallO assembly without any extra steps and dependencies.',
    url='https://github.com/smallo-lang/Beth',
    license='MPL-2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'colorama',
        'termcolor',
    ],
    entry_points="""
        [console_scripts]
        beth=beth.cli:run
    """,
)
