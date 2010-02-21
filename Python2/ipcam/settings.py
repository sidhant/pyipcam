## Copyright (c) 2010 Jared De Blander
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.

#IP/Hostname
host = "10.10.1.20"

#Path to MJPEG file
path = "/img/video.mjpeg" 

#Bytes to grab per read. Default 1024 (1KB)
chunk_size = 1024

#Motion Threshold (Hue based no longer used)
threshold = 40

#motion rgb threshold
rgb_threshold = 20

#pixel block size
rgb_blocksize = 10

#Outline blocks with motion?
rgb_outline = True

#color of outline - 0 = black, 255 = red
rgb_outline_color = 255
