Examples
========

You can start from these examples to explore the library. The next topic
:doc:`Api <modules>` lists all available methods with their parameters and
some other examples.

Python
------

Start python and import the library you have :doc:`previously installed <install>`

>>> import bblab

You can download and use the
`set of sample data <https://github.com/lorenzo-cavazzi/bblab/tree/master/data>`_ 
provided. In the following examples we assume you saved them in a `data` folder

Assignment
```````````

The original assignment has 3 steps. Here are the instructions to execute them.
We assume Tiff files from our sample set to be available in `data/1i_channels` and
`data/2i_mask` folders. We will save the output of each step in these folders:
`data/output1`, `data/output2` and `data/output3`.

#. Overlay channels
    >>> from bblab.image import processing # or use bblab.image.processing
    >>> processing.overlay_channels(r"data/1i_channels", r"data/output1")
    
#. Highlight cells
    >>> processing.highlight_cells(r"data/output1", r"data/2i_mask", r"data/output2")

#. Compute means
    >>> processing.compute_mean(r"data/output2", r"data/output3")

You may verify each step results in the `data/output[x]` folders

Improvements
`````````````

The final Csv file containing channels means may be significative because it preserves
all the information from the Tiff channels without modifying it. Nevertheless, the output
images are not very interesting at a first glance because they are too dark to allow
humans to identity any features.

There are a number of parameters to modify channels intensity. We can try to maximize
all of them, and further applying a multiplier on every single channel

>>> processing.overlay_channels(r"data/1i_channels", r"data/output1",
        maximize_intensity = True, r_channel_multiplier = 50,
        g_channel_multiplier = 2, b_channel_multiplier = 5)

Now the cells appear more identifiable, but we lose some information in the process:
some full-green pixels are in fact from intensities that were originally different
by a factor 10 or more.

We can also improve the cell highlighting by applying an algorithm that tries to
preserve the information about single pixel cells identification. This time we will
lose the correspondence between original cell id and final transparency channel value.

>>> processing.highlight_cells(r"data/output1", r"data/2i_mask", r"data/output2",
        cells_highlight = 2)

We can easily identify the cells. Given a transparency channel of 16 bits, the
difference of up to 680 (the number of different cells) is negligible for a human
eye.

The final step yields to different numbers, but this is inevitable if we always
take only the Png images from the previous step because we lost information in
the first step.

Command line
-------------

The library gets installed along with a command line tool to be invoked from the shell.
Try to type

>>> bblab -h
usage: command [-h] {overlay_channels,highlight_cells,compute_mean} ...
bblab command line tool allows you to start bblab main functions from [...]

Every function has its own help description. As an example try typing

>>> bblab overlay_channels -h
usage: command overlay_channels [-h] [-i INPUT_FOLDER] [-o OUTPUT_FOLDER]
[...]

Please note that only some function parameters are available while invoking functions
from the command line.

Here is an exmaple of how to use the command line `bblab` tool

>>> bblab overlay_channels -i "data/1i_channels" -o "data/output1" -max True
bblab.image.processing.overlay_channels
>>> bblab highlight_cells -irgb "data/output1" -imask "data/2i_mask" -o "data/output2" -ch 2
bblab.image.processing.highlight_cells
>>> bblab compute_mean -i "data/output2" -o "data/output3"
bblab.image.processing.compute_mean


Explore
--------

You can play with the values in the examples to obtain different results. The next topic
lists all available methods with their parameters and some other examples. Enjoy :)