"""
RenertPy Python Package
Copyright (C) 2022 Assaf Gordon (assafgordon@gmail.com)
License: BSD (See LICENSE file)
"""
import warnings
import colorsys

def rgb_to_hsv(r,g,b):
    if not (r>=0 and r<=255):
        raise ValueError("Invalid r (red) value '%s': must be between 0 and 255" % str(r))
    if not (g>=0 and g<=255):
        raise ValueError("Invalid g (green) value '%s': must be between 0 and 255" % str(g))
    if not (b>=0 and b<=255):
        raise ValueError("Invalid b (blue) value '%s': must be between 0 and 255" % str(b))

    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)

    h = int(h * 360) # convert to degrees

    return [h,s,v]

def hsv_to_rgb(h,s,v):
    if not (h>=0 and h<=360):
        raise ValueError("Invalid h (hue) value '%s': must be between 0 and 360" % str(h))
    if not (s>=0.0 and s<=1.0):
        raise ValueError("Invalid s (saturation) value '%s': must be between 0.0 and 1.0" % str(s))
    if not (v>=0 and v<=255):
        raise ValueError("Invalid v (value) value '%s': must be between 0 and 255" % str(v))

    r,g,b = colorsys.hsv_to_rgb(h/360,s,v)

    return [int(r*255), int(g*255), int(b*255)]
