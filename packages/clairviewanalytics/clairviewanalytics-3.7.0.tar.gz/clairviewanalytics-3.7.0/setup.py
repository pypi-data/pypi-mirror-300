import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import analytics-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "clairview"))
from version import VERSION

long_description = """
ClairView is developer-friendly, self-hosted product analytics. clairview-python is the python package.
"""

install_requires = ["requests>=2.7,<3.0", "six>=1.5", "monotonic>=1.5", "backoff>=1.10.0", "python-dateutil>2.1"]

extras_require = {
    "dev": [
        "black",
        "isort",
        "flake8",
        "flake8-print",
        "pre-commit",
    ],
    "test": ["mock>=2.0.0", "freezegun==0.3.15", "pylint", "flake8", "coverage", "pytest", "pytest-timeout", "django"],
    "sentry": ["sentry-sdk", "django"],
}

setup(
    name="clairview",
    version=VERSION,
    url="https://github.com/clairview/clairview-python",
    author="Clairview",
    author_email="hey@clairview.com",
    maintainer="ClairView",
    maintainer_email="hey@clairview.com",
    test_suite="clairview.test.all",
    packages=["clairview", "clairview.test", "clairview.sentry", "clairview.exception_integrations"],
    license="MIT License",
    install_requires=install_requires,
    extras_require=extras_require,
    description="Integrate ClairView into any python application.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
