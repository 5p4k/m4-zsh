#!/usr/bin/env python
# Find the xterm-256color that is nearest to a given RGB color.
#
# ------------------------------------ USAGE ------------------------------------
#
# nearest-col.py <color> [options]
#
#   <color>     Hexadecimal RGB color, e.g. 'deadbe' (24 bit) or 'eef' (12 bit)
#               with optional leading '#'.
#   Options:
#       -d1     Uses 1-distance between the color values.
#       -d2     Uses 2-distance (euclidean) between the color values (default).
#       -dinf   Uses inf-distance (max) between the color values.
#       -rgb    Compares the RGB values (default).
#       -hsb    Converts the colors to HSB before comparing the values.
#
# ----------------------------------- LICENSE -----------------------------------
#
# Copyright (c) 2014, Pietro Saccardi
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies, 
# either expressed or implied, of the FreeBSD Project
#
# -------------------------------------------------------------------------------


import sys, re, math

# Load terminal colors in order
TERM_COLORS = [
    0x000000,
    0x800000,
    0x008000,
    0x808000,
    0x000080,
    0x800080,
    0x008080,
    0xc0c0c0,
    0x808080,
    0xff0000,
    0x00ff00,
    0xffff00,
    0x0000ff,
    0xff00ff,
    0x00ffff,
    0xffffff,
    0x000000,
    0x00005f,
    0x000087,
    0x0000af,
    0x0000d7,
    0x0000ff,
    0x005f00,
    0x005f5f,
    0x005f87,
    0x005faf,
    0x005fd7,
    0x005fff,
    0x008700,
    0x00875f,
    0x008787,
    0x0087af,
    0x0087d7,
    0x0087ff,
    0x00af00,
    0x00af5f,
    0x00af87,
    0x00afaf,
    0x00afd7,
    0x00afff,
    0x00d700,
    0x00d75f,
    0x00d787,
    0x00d7af,
    0x00d7d7,
    0x00d7ff,
    0x00ff00,
    0x00ff5f,
    0x00ff87,
    0x00ffaf,
    0x00ffd7,
    0x00ffff,
    0x5f0000,
    0x5f005f,
    0x5f0087,
    0x5f00af,
    0x5f00d7,
    0x5f00ff,
    0x5f5f00,
    0x5f5f5f,
    0x5f5f87,
    0x5f5faf,
    0x5f5fd7,
    0x5f5fff,
    0x5f8700,
    0x5f875f,
    0x5f8787,
    0x5f87af,
    0x5f87d7,
    0x5f87ff,
    0x5faf00,
    0x5faf5f,
    0x5faf87,
    0x5fafaf,
    0x5fafd7,
    0x5fafff,
    0x5fd700,
    0x5fd75f,
    0x5fd787,
    0x5fd7af,
    0x5fd7d7,
    0x5fd7ff,
    0x5fff00,
    0x5fff5f,
    0x5fff87,
    0x5fffaf,
    0x5fffd7,
    0x5fffff,
    0x870000,
    0x87005f,
    0x870087,
    0x8700af,
    0x8700d7,
    0x8700ff,
    0x875f00,
    0x875f5f,
    0x875f87,
    0x875faf,
    0x875fd7,
    0x875fff,
    0x878700,
    0x87875f,
    0x878787,
    0x8787af,
    0x8787d7,
    0x8787ff,
    0x87af00,
    0x87af5f,
    0x87af87,
    0x87afaf,
    0x87afd7,
    0x87afff,
    0x87d700,
    0x87d75f,
    0x87d787,
    0x87d7af,
    0x87d7d7,
    0x87d7ff,
    0x87ff00,
    0x87ff5f,
    0x87ff87,
    0x87ffaf,
    0x87ffd7,
    0x87ffff,
    0xaf0000,
    0xaf005f,
    0xaf0087,
    0xaf00af,
    0xaf00d7,
    0xaf00ff,
    0xaf5f00,
    0xaf5f5f,
    0xaf5f87,
    0xaf5faf,
    0xaf5fd7,
    0xaf5fff,
    0xaf8700,
    0xaf875f,
    0xaf8787,
    0xaf87af,
    0xaf87d7,
    0xaf87ff,
    0xafaf00,
    0xafaf5f,
    0xafaf87,
    0xafafaf,
    0xafafd7,
    0xafafff,
    0xafd700,
    0xafd75f,
    0xafd787,
    0xafd7af,
    0xafd7d7,
    0xafd7ff,
    0xafff00,
    0xafff5f,
    0xafff87,
    0xafffaf,
    0xafffd7,
    0xafffff,
    0xd70000,
    0xd7005f,
    0xd70087,
    0xd700af,
    0xd700d7,
    0xd700ff,
    0xd75f00,
    0xd75f5f,
    0xd75f87,
    0xd75faf,
    0xd75fd7,
    0xd75fff,
    0xd78700,
    0xd7875f,
    0xd78787,
    0xd787af,
    0xd787d7,
    0xd787ff,
    0xd7af00,
    0xd7af5f,
    0xd7af87,
    0xd7afaf,
    0xd7afd7,
    0xd7afff,
    0xd7d700,
    0xd7d75f,
    0xd7d787,
    0xd7d7af,
    0xd7d7d7,
    0xd7d7ff,
    0xd7ff00,
    0xd7ff5f,
    0xd7ff87,
    0xd7ffaf,
    0xd7ffd7,
    0xd7ffff,
    0xff0000,
    0xff005f,
    0xff0087,
    0xff00af,
    0xff00d7,
    0xff00ff,
    0xff5f00,
    0xff5f5f,
    0xff5f87,
    0xff5faf,
    0xff5fd7,
    0xff5fff,
    0xff8700,
    0xff875f,
    0xff8787,
    0xff87af,
    0xff87d7,
    0xff87ff,
    0xffaf00,
    0xffaf5f,
    0xffaf87,
    0xffafaf,
    0xffafd7,
    0xffafff,
    0xffd700,
    0xffd75f,
    0xffd787,
    0xffd7af,
    0xffd7d7,
    0xffd7ff,
    0xffff00,
    0xffff5f,
    0xffff87,
    0xffffaf,
    0xffffd7,
    0xffffff,
    0x080808,
    0x121212,
    0x1c1c1c,
    0x262626,
    0x303030,
    0x3a3a3a,
    0x444444,
    0x4e4e4e,
    0x585858,
    0x606060,
    0x666666,
    0x767676,
    0x808080,
    0x8a8a8a,
    0x949494,
    0x9e9e9e,
    0xa8a8a8,
    0xb2b2b2,
    0xbcbcbc,
    0xc6c6c6,
    0xd0d0d0,
    0xdadada,
    0xe4e4e4,
    0xeeeeee,
]

TERM_COLORS.__doc__ = "List of xterm-256color colors in RGB."

# Trivial helper functions
COL24_TO_RGB = lambda color: (color >> 16, (color & 0xFFFF) >> 8, color & 0xFF)
COL12_TO_RGB = lambda color: (color >>  8, (color & 0x00FF) >> 4, color & 0x0F)

COL24_TO_RGB.__doc__ = "Converts a 24-bit number into a 3-tuple with RGB values (#RRGGBB)."
COL12_TO_RGB.__doc__ = "Converts a 12-bit number into a 3-tuple with RGB values (#RGB)."

def COL_DIST2(col1, col2):
    """
    Computes 2-distance between two RGB vectors, i.e.
        = sqrt(r^2 + g^2 + b^2)
    """
    r, g, b = (col1[i] - col2[i] for i in range(0, 3))
    return math.sqrt(r * r + g * g + b * b)

def COL_DIST1(col1, col2):
    """
    Computes 1-distance between two RGB vectors, i.e.
        = abs(r) + abs(g) + abs(b)
    """
    r, g, b = (col1[i] - col2[i] for i in range(0, 3))
    return abs(r) + abs(g) + abs(b)

def COL_DISTINF(col1, col2):
    """
    Computes inf-distance between two RGB vectors, i.e.
        = max(abs(r), abs(g), abs(b))
    """
    r, g, b = (col1[i] - col2[i] for i in range(0, 3))
    return max(abs(r), abs(g), abs(b))



# Nice function for going into HSB domain
def RGB_TO_HSB(col):
    """
    Converts a 3-tuple with RGB values (in range 0..255) into a 3-tuple
    with HSB color values in range [0..1].
    """
    r, g, b = col

    cmax = float(max(r, g, b))
    cmin = float(min(r, g, b))

    delta = cmax - cmin

    brightness = cmax / 255.0
    saturation = (delta / cmax) if cmax > 0 else 0
    hue = 0

    if saturation > 0:
        redc = (cmax - r) / delta
        greenc = (cmax - g) / delta
        bluec = (cmax - b) / delta

        if r == cmax:
            hue = bluec - greenc
        elif g == cmax:
            hue = 2.0 + redc - bluec
        else:
            hue = 4.0 + greenc - redc

        hue /= 6.0
        if hue < 0: hue += 1.0

    return (hue, saturation, brightness)



if __name__ == '__main__':

    # Default distance
    distance = COL_DIST2
    hsb = False

    # Check the other parameters
    if len(sys.argv) > 2:
        for opt in sys.argv[2:]:
            if opt == '-d2':
                distance = COL_DIST2
            elif opt == '-d1':
                distance = COL_DIST1
            elif opt == '-dinf':
                distance = COL_DISTINF
            elif opt == '-rgb':
                hsb = False
            elif opt == '-hsb':
                hsb = True
            else:
                print('Unrecognized option: ' + sys.argv[2])


    # String to color
    def parse_color(color):
        if color[0] == '#': color = color[1:]
        short = (len(color) == 3)
        color = int(color, 16)
        return COL24_TO_RGB(color) if not short else COL12_TO_RGB(color)


    # Setup a regex for testing input
    pattern = re.compile('^#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')



    color = sys.argv[1] if len(sys.argv) > 1 else None
    
    while color is None or pattern.match(color) is None:
        color = raw_input('Hex color: ')

        # Check for exit
        if len(color) == 0: sys.exit()

    color = parse_color(color)



    # Preprocess TERM_COLORS
    if hsb:
        colors = [RGB_TO_HSB(COL24_TO_RGB(c)) for c in TERM_COLORS]
        color = RGB_TO_HSB(color)
    else:
        colors = [COL24_TO_RGB(c) for c in TERM_COLORS]

    # Now we have a color vector, compute differences
    differences = [(i, TERM_COLORS[i], distance(colors[i], color)) for i in range(0, len(colors))]
    differences = sorted(differences, key=lambda item: item[2])

    # Print out the best 3 candidates
    for i in range(0, 3):
        item  = differences[i]
        print(
            'Code: %03d (#%06X)\tDistance: %0.2f\t\t' % item +
            '\x1b[48;5;15m\x1b[38;5;%dmFORECOLOR\x1b[00m' % item[0] +
            '\x1b[48;5;0m\x1b[38;5;%dmFORECOLOR\x1b[00m\t' % item[0] +
            '\x1b[38;5;15m\x1b[48;5;%dmBACKGROUND\x1b[00m' % item[0] +
            '\x1b[38;5;0m\x1b[48;5;%dmBACKGROUND\x1b[00m' % item[0]
            )
        