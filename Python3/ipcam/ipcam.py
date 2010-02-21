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
import http.client
import time
import settings

#create a connection to the webcam
print ("Connectiong to", settings.host)
conn = http.client.HTTPConnection(settings.host)

#request the mjpeg stream
print ("Requesting stream @", settings.path)
conn.request("GET", settings.path)

#get the response
r1 = conn.getresponse()

#display the response status
print ("Device returned:", r1.status, r1.reason)

#control variables initial states
in_file=False
file_write=False
first_image=True

#read data from the response and write it to a file
print ("Downloading",settings.chunk_size * 100,"bytes from device")


while True:
    new_data=r1.read(settings.chunk_size)  #chunk size is in bytes

    #default values for every chunk
    start_write=0
    end_write=settings.chunk_size

    for i in range(0, settings.chunk_size - 1):
        if in_file:
            file_write=True
            #look for jpeg end of image (aka EOI) mark (0xFFD9)
            if(new_data[i]==255 and new_data[i+1]==217):
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
                    print("Looking for motion in ", filename, " vs ", prior_filename, " : ")

                #record the filename of the image we just created as the prior image
                prior_filename=filename

                #Record we are no longer after the first iamge
                first_image=False
               
        else:
            #look for jpeg start of image (aka SOI) mark (0xFFD8)
            if(new_data[i]==255 and new_data[i+1]==216):
                #We want to write data to the file this pass
                file_write=True
                #We are now inside a file
                in_file=True
                #Record the offset to start writing at
                start_write=i
                #lets assume this frame ends at the end of this for safety sake
                end_write=settings.chunk_size
                #open a file to write to
                filename="images/" + str(time.time()) + ".jpg"
                print("Creating image ", filename)
                f=open(filename, 'wb')
            else:
                file_write=False
    #Check if we need to perform a write 
    if(file_write==True):
        f.write(new_data[start_write:end_write])

##    for i in range(0, settings.chunk_size - 1):
##        if in_file:
##            f.write(jpgfile)
##        else:
##            #look for jpeg start of image (aka SOI) mark (0xFFD8)
##            if(data[i]==255 and data[i+1]==216):
##                print ("File start!")
##                in_file=True
##                jpgfile[0]=bytes(data[i])
##f.close()


#Close our file if it's still open
if(in_file==True):
    f.close()

#Close connection to the webcam
conn.close()
print ("Downlaod complete")
