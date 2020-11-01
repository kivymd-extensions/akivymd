import os
import sys

pkg_path = os.path.abspath(__file__).rsplit("akivymd")[0]
sys.path.append(pkg_path)

from akivymd import factory_registers  # noqa

__version__ = "1.2.2"
