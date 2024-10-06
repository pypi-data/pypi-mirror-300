from setuptools import setup, find_packages

setup(
    name='petpet',
    version='2.0.1',
    packages=find_packages(),
    include_package_data=True,  # Stellt sicher, dass alle Dateien in MANIFEST.in berücksichtigt werden
    package_data={
        'petpet': ['img/*.gif'],  # Alle GIF-Dateien im img-Ordner einbeziehen
    },
)
