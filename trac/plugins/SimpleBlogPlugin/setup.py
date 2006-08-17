from setuptools import find_packages, setup

setup(
    name='SimpleBlogPlugin',
    version='0.1',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = """
        [trac.plugins]
        simpleblog = simpleblog
    """,
)
