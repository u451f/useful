#!/usr/bin/env python3

# The file should be executed from the root of jekyll
# The post name will be the image folder name, so
# make sure to name it according to the scheme yyyy-mm-dd-title
# path is the path the image folder, with subfolders.
# path_to_posts is where to publish the post.html.

import glob, os, os.path
from PIL import Image

# <-- CONFIGURATION
size = 300, 200
path = "assets/images/"
path_to_posts = "_posts/"
# --> END CONFIGURATION

abspath = os.path.dirname(os.path.realpath(__file__))
folders = [ f.path for f in os.scandir(path) if f.is_dir() ]

for folder in folders:
    # assign filename for post
    basename = os.path.basename(folder)
    filename = "%s.html" % (basename)

    os.chdir(folder)
    # get all the jpg files from the current folder and create a thumbnail
    # add all files to a dict
    imgs = {}
    for inputfile in glob.glob("*.jpg"):
        outputfile = os.path.splitext(inputfile)[0] + "-thumb.jpg"
        imgs[inputfile] = outputfile
        if inputfile != outputfile:
            try:
                im = Image.open(inputfile)
                im.thumbnail(size)
                im.save(outputfile, "JPEG")
            except IOError:
                print ("Cannot create thumbnail for", inputfile)
    #print (imgs)
    os.chdir(abspath)

    # get first thumb
    if len (imgs) > 0:
        try:
            first_thumb = os.path.join(folder, list(imgs.values())[0])
        except IOError:
            print ("Cannot find first thumb for", filename)
            print ("\r\nimgs:", imgs)

    # write post
    f= open (os.path.join(path_to_posts, filename), "w+")
    f.write ("---\r\n")
    f.write ("layout: post\r\n")
    f.write ("thumbnail: %s" % (first_thumb))
    f.write ("\r\n---\r\n")

    for image, thumb in sorted (imgs.items()):
        # print (image, thumb)
        f.write ('<a href="{{ site.url }}/%s/%s"><img src="{{ site.url }}/%s/%s" alt=""></a>' % (folder, image, folder, thumb))
        # f.write ('<img class="swiper-slide" src="{{ site.url }}/%s/%s" alt="" />' % (folder, image))
        f.write ("\r\n")
    f.close()
    print ("Post %s written" % (os.path.join(path_to_posts, filename)))

    # delete dictionary.
    del imgs
