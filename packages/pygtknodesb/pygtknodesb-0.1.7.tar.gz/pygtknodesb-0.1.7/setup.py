import setuptools
import subprocess
import os

def build():
    if not os.path.isdir("./pygtknodesb/lib"):
        print("Building gtknodes using podman ...")
        # podman build
        subprocess.run(["podman", "build", "-f", "./Dockerfile", "-t", "gtknodes"])

        # podman run -it -d --name gtknodes-container gtknodes
        subprocess.run(["podman", "run", "-it", "-d", "--name", "gtknodes-container", "gtknodes"])

        # podman cp 
        out = subprocess.run(["podman", "cp", "gtknodes-container:/gtknodes/build/.", "./pygtknodesb/"])

        if out.returncode != 0:
            print("error on subprocess run podman cp.")
            exit(1)

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True

            build()

except ImportError:
    bdist_wheel = None

try:
    from setuptools.command.bdist_egg import bdist_egg as _bdist_egg

    class bdist_egg(_bdist_egg):
        def run(self):
            build()
            _bdist_egg.run(self)
except ImportError:
    bdist_egg = None

# to build binary distributions
# $ python setup.py sdist bdist_egg bdist_wheel

# to upload to pypi
# $ pip install twine
# $ twine upload --repository-url https://upload.pypi.org/legacy/ dist/* --verbose

setuptools.setup(
    name='pygtknodesb',
    version="0.1.7",
    author="aluntzer",
    description="",
    packages=['pygtknodesb'],
    package_data={'pygtknodesb':['lib/**', 'include/**', 'share/**'] },
    cmdclass={'bdist_wheel': bdist_wheel, 'bdist_egg': bdist_egg},
)
