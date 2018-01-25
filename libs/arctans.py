import numpy as np

def arctans(x, y):
    y[y == 0] = 0.000001
    z = x / y
    z = np.arctan(z)
    
    pi = np.pi
    
    test = (y < 0.0) * (x <  0.0)
    z[test] = -pi/2.0 - z[test]
    
    test = (y < 0.0) * (x >  0.0)
    z[test] = pi + z[test] 
    
    test = (y < 0.0) * (x == 0.0)
    z[test] = -pi
    
    return z
