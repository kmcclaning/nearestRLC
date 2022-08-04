# Purpose
This package allows the user to specify an exact value of resistor, inductor or capacitor and find the closest 
standard value to that exact value. Tolerances included are: values: 20% (E6), 10% (E12), 5% (E24), 
2% (E48), 1% (E96), and 0.5% (E192).

The method handles 0.0, math.inf and math.nan inputs. 

# Examples
```
import math
from nearestRLC import nearestRLC
print(nearestRLC(5.123E3, '2p0'))   # prints 5110.0
print(nearestRLC(5.123E3, '5p0'))   # prints 5100.0
print(nearestRLC(5.123E3, '10p0'))  # prints 4700.0
print(nearestRLC(5.123E3, '20p0'))  # prionts 4700.0
print(nearestRLC(4.4E5, '20p0'))    # prints 470000.0
```

See the test methods in test_nearestRLC.py for other calling examples. 