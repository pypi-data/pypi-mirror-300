from os import path
import sys


sys.path.append(path.join(path.dirname(__file__), 'assemblies'))

print(sys.path)
from pythonnet import load

load("coreclr")

import clr

clr.AddReference("MrKWatkins.OakEmu.Machines.ZXSpectrum")  # noqa
clr.AddReference("MrKWatkins.OakEmu.Machines.ZXSpectrum.Games")  # noqa
