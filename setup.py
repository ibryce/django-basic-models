from setuptools import setup, find_packages
import csky
from basic_models import VERSION

setup(
    name='django-basic-models',
    version=".".join(map(str, VERSION)),
    packages = find_packages(),

    author = 'Concentric Sky',
    author_email = 'django@concentricsky.com',
    description = 'Useful basic models that any django app should need'
)
