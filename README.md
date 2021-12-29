# photo-grammetry
Simple measure&amp;scale from photo

This script displays a photo file and then responds to key presses and (left)
button clicks to report scaled distances.
The report is (currently) on the launching terminal stdout :-(

Prerequisites: python3 tkinter and Pillow (as PIL replacement)

Usage: Run from command terminal (where output will appear) with scale factor
and photo file, eg:
`python3 photogram_1.py 200 ../examples/mastfoot/20211229_090356.jpg`
Then point to the 10cms point on the rule and type 'r'; move to the 30cms point
and type 's'; Then select any starting point and ctrl-left click. from then on
left click will display the distance (in the terminal window) from the last
ctrl-left reference point.


<!-- kate: indent-width 4; tab-width 4; replace-tabs on; -->
<!-- kate: word-wrap on; word-wrap-column 70 -->