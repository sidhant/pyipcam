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

import math, operator
from PIL import Image
from math import fabs

def compare(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    h1 = image1.histogram()
    h2 = image2.histogram()
    rms = math.sqrt(reduce(operator.add,map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    return rms

def detect_motion(old_image, new_image, threshold = 10, blocksize = 8, outline = False, outline_color = 16711680):
    # Blocks of motion found
    motion_level = 0
    
    # Open our images
    image1 = Image.open(old_image)
    image2 = Image.open(new_image)

    # print "Dimensions ", image1.size[0], image1.size[1]

    # Return 0 if images are different size
    if (image1.size[0] != image2.size[0]) or (image1.size[1] != image2.size[1]):
        return 0

    size = image1.size

    imgArr1 = list(image1.getdata())
    imgArr2 = list(image2.getdata())

    t = threshold

    x = 0


    # loop through the image in blocks
    while x < image1.size[0] / blocksize:
        y = 0
        while y < image1.size[1] / blocksize:

            # loop through the blocks in pixels
            x_offset = 0

            block_r_1 = 0
            block_g_1 = 0
            block_b_1 = 0

            block_r_2 = 0
            block_g_2 = 0
            block_b_2 = 0

            while x_offset < blocksize:
                
                y_offset = 0
                while y_offset < blocksize:

                    # calculate the point in the array for this pixel

                    x_pixel = x * blocksize + x_offset
                    y_pixel = y * blocksize + y_offset

                    array_spot = y_pixel * image1.size[0] + x_pixel

#                    print "Solving pixel ", x_pixel , ", ", y_pixel, " @" , array_spot

                    p1 = imgArr1[array_spot]
                    p2 = imgArr2[array_spot]

                    block_r_1 = block_r_1 + p1[0]
                    block_g_1 = block_g_1 + p1[1]
                    block_b_1 = block_b_1 + p1[2]

                    block_r_2 = block_r_2 + p2[0]
                    block_g_2 = block_g_2 + p2[1]
                    block_b_2 = block_b_2 + p2[2]
                    
                    y_offset = y_offset + 1
                    
                x_offset = x_offset + 1

                r_diff = (fabs(block_r_1 - block_r_2)) / (blocksize ** 2)
                g_diff = (fabs(block_g_1 - block_g_2)) / (blocksize ** 2)
                b_diff = (fabs(block_b_1 - block_b_2)) / (blocksize ** 2)

                # see if a block contained motion
                if r_diff > t or g_diff > t or b_diff > t:
                    motion_level = motion_level + 1
                    if outline:
                        outline_offset = 0
                        while outline_offset < blocksize:
                            #horizontal lines
                            image2.putpixel((x * blocksize + outline_offset, y * blocksize), outline_color)
                            image2.putpixel((x * blocksize + outline_offset, y * blocksize + blocksize), outline_color)

                            #vertical lines
                            image2.putpixel((x * blocksize, y * blocksize + outline_offset), outline_color)
                            image2.putpixel((x * blocksize + blocksize, y * blocksize + outline_offset), outline_color)
                            
                            outline_offset = outline_offset + 1
                        

                            
                        
            
            #proceed to next block vertically
            y = y + 1
        #proceed to next column of blocks
        x = x + 1

    if outline and motion_level > 0:
        image2.save(new_image + ".outlined.jpg")
##
##
##
##    while i < len(imgArr1):
##        p1 = imgArr1[i]
##        p2 = imgArr2[i]
##
##        if (fabs(p1[0]-p2[0]) > t) or (fabs(p1[1]-p2[1]) > t) or (fabs(p1[2]-p2[2]) > t):
##
##            motion_level = motion_level + 1
##
##        i = i + 1

    return motion_level
