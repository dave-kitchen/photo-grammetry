#!/usr/bin/env python3

print ('Note: currently no rectification!')

import tkinter
from PIL import ImageDraw, Image, ImageTk
import sys
import math

reference = None
scale = None # 5.7 # pixels per unit-length

import numbers
ref_point_1 = None
ref_point_2 = None

def relative(x,y,fix=False):
    global reference
    if fix or reference == None:
        reference = (x, y)
    dx = x-reference[0]
    dy = y-reference[1]
    return math.sqrt(dx*dx+dy*dy)

def at_scale(p):
    global scale
    if isinstance(p, numbers.Real):
        return p/scale
    # assume iterable
    return map(lambda x: x/scale, p)

def calc_scale():
    global ref_point_1, ref_point_2, ref_length, scale
    dx = ref_point_2[0]-ref_point_1[0]
    dy = ref_point_2[1]-ref_point_1[1]
    dr = math.sqrt(dx*dx+dy*dy)
    scale = dr/ref_length
    print ('scale is',scale,'pixels per unit-length')


def process(args):
    global ref_point_1, ref_point_2, ref_length
    ref_length = args.length
    fn = args.file
    window = tkinter.Tk(className=fn)
    # print ('filename is',fn)
    image = Image.open(fn)
    size = image.size
    new_w = 1000
    w = float(size[0])
    h = float(size[1])
    new_h = int(new_w*(h/w))
    print ('w,h,new_w,new_h:',w,h,new_w,new_h)
    image = image.resize((new_w, new_h), Image.ANTIALIAS)
    #image = image.resize((1000, 800), Image.ANTIALIAS)
    global canvas
    canvas = tkinter.Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack()
    image_tk = ImageTk.PhotoImage(image)

    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

    def callback(event):
        global ref_point_1, ref_point_2
        if ref_point_1 == None or ref_point_2 == None:
            return
        ctl = (event.state & 4) != 0
        print ("clicked at: ", (event.x, event.y),
                at_scale(relative(event.x, event.y, ctl)))
    def callback_1(event):
        global ref_point_1, ref_point_2
        # ctl = (event.state & 4) != 0
        if event.char in {'r','s'}:
            print (event.char, "pressed at: ", (event.x, event.y))
        # print ('callback_1')
            if event.char == 'r':
                ref_point_1 = (event.x, event.y)
            if event.char == 's':
                ref_point_2 = (event.x, event.y)
            if ref_point_1 == None or ref_point_2 == None:
                return
            calc_scale()

    canvas.bind("<Button-1>", callback)
    window.bind_all("<Key>", callback_1)
    tkinter.mainloop()

if __name__ == '__main__':
    from argparse import ArgumentParser
    desc = """Display and measure Image.
Identify two points in the image known to be at the Reference length apart.
Mark the first by keying 'r' while the cursor is over it.
Mark the second point by keying 's', again while cursor is over it.
Using this scale (assumed to be isotropic) lengths between a base point
and others are reported. Set the base point by ctrl-left-click, and report
length from there by left-click. Reports are to the console/stdout.
"""
    parser = ArgumentParser(description=desc)
    parser.add_argument('--parallel', action='store_true',
                    help='display, and enforce, calibration-parallel lengths')
    parser.add_argument('length', type=float, help='Reference length')
    parser.add_argument('file', type=str,  help='File to measure')
    args=parser.parse_args()

    process(args)
    #process(sys.argv[1:])
    pass

# kate: indent-width 4; tab-width 4; replace-tabs on
