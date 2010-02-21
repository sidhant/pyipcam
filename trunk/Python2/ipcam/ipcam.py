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

#include our libraries & settings
import httplib
import time
import settings
import motion
import shutil
import os
import sys

while True:
    try:
        #create a connection to the webcam
        print "Connectiong to", settings.host
        conn = httplib.HTTPConnection(settings.host)

        #request the mjpeg stream
        print "Requesting stream @", settings.path
        conn.request("GET", settings.path)

        #get the response
        r1 = conn.getresponse()

        #display the response status
        print "Device returned:", r1.status, r1.reason

        #control variables initial states
        in_file=False
        file_write=False
        first_image=True

        #read data from the response and write it to a file
        print "Streaming", settings.chunk_size, " byte chunks from device"


        while True:
            new_data=r1.read(settings.chunk_size)  #chunk size is in bytes

            #default values for every chunk
            start_write=0
            end_write=settings.chunk_size

            for i in range(0, settings.chunk_size - 1):

                if in_file:
                    file_write=True
                    #look for jpeg end of image (aka EOI) mark (0xFFD9)
                    if(new_data[i]==chr(255) and new_data[i+1]==chr(217)):
                        #Record the last byte address of this chunk
                        end_write=i+2
                        #Record that we are no longer in a file
                        in_file=False
                        #Perform our final write
                        f.write(new_data[start_write:end_write])
                        #Record that we are done writing to this file
                        file_write==False
                        #Close the file
                        f.close()
                        #if not the first image then look for motion
                        if (first_image==False):
                            # difference = motion.compare(filename, prior_filename)
                            # print "Hue Variation : " , int(difference)
                            motion_level = motion.detect_motion(prior_filename, filename, settings.rgb_threshold, settings.rgb_blocksize, settings.rgb_outline, settings.rgb_outline_color)
                            os.remove(prior_filename)
                            print "Motion Level :", int(motion_level)
                            if motion_level > settings.threshold:
                                shutil.copy(filename, "motion/")
                                if settings.rgb_outline:
                                    shutil.copy(filename + ".outlined.jpg", "motion.outlined/")
                                    os.remove(filename + ".outlined.jpg")

                        #record the filename of the image we just created as the prior image
                        prior_filename=filename

                        #Record we are no longer after the first iamge
                        first_image=False
                       
                else:
                    #look for jpeg start of image (aka SOI) mark (0xFFD8)
                    if(new_data[i]==chr(255) and new_data[i+1]==chr(216)):
                        #We want to write data to the file this pass
                        file_write=True
                        #We are now inside a file
                        in_file=True
                        #Record the offset to start writing at
                        start_write=i
                        #lets assume this frame ends at the end of this for safety sake
                        end_write=settings.chunk_size
                        #open a file to write to
                        filename="tmp/" + str(time.time()) + ".jpg"
                        f=open(filename, 'wb')
                    else:
                        file_write=False
            #Check if we need to perform a write 
            if(file_write==True):
                f.write(new_data[start_write:end_write])
    except:
        print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
        print "Attempting to recover."
