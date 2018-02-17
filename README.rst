LabelImg README for Markov
========

Saving Image Files Locally
--------------------------
Precursor: Image Training
^^^^^^^^^^^^^^^^^^^^^^^^^
Navigate to /code/gallium/notebooks and run: jupyter notebook
	
	Alternatively, enter and search: https://localhost:9999/tree?

1. From the jupyter home page on your browser, open up the "Capture HDR images for training.ipynb" notebook. 
2. In the 2nd cell, edit the IP address to reflect the box you are using. 
3. In the 4th cell, edit FOOD_NAME value and print() arguments to reflect the food you are gathering images of. 
4. Place your food in the box, and cover the cavity entrance with the black felt curtain. 
	**Ensure that the curtain is not visible within the white space of the cavity. 
5. Click on the first cell, then from the navigation bar go to Kernel > Restart & Run All.
6. Once the cells have run and an image has populated, check the /code/gallium/notebooks folder to ensure a new folder has been created and .jpeg food images are stored within. 
	**Check the photo to ensure good image quality. If there is an obvious light distortion or 'split' within the image, 	     please delete saved image and retake photo. 
7. Continue running the LAST CELL ONLY to take about 200 unique training images. 
	Tips for taking images:
		Take 10 images with food container horizontal (5 with food on left side, flip container around to take 5 		 with food on right side).
		Take 10 images with food container vertical (5 with food on upper side, flip container around to take 5 with	  	    food on lower side).
		Take out food container, place food on a new spot on a new container and repeat above steps for 3-5 			different spots on container.
		Take images with varying servings of food. 
8. When done collecting images, navigate to predator.local:5000
	- Go to Chopper > food_training > food_recognition
		--> Open up the data folder of interest, and create a new folder for the food images to be trained (if not 
		    already made)
		--> Upload .jpeg images. 

Using LabelImg
^^^^^^^^^^^^^^
1. Scroll down to the Installation section below to download and build the labelImg program.
2. Navigate to your local labelImg folder
	a. Go to 'data' folder and open up 'predefine_classes.txt'. Ensure the name of your food (i.e. "ribs) is included--	      if not, add food name, save, and close.
	b. Run python labelImg.py
3. Click on "Open Dir", navigate to /code/gallium/notebooks/ and open the folder with the images you are going to train. 
4. Click on "Change Save Dir" to verify and/or change the directory the trained files will be saved in. 
5. Make the program full window and zoom in (it will make labeling easier!)
6. Click 'Next Image' or type ``d``
7. Click 'Create RectBox' or type ``w``
8. Draw a bounding box by clicking and dragging.
9. A selection box will appear for you to label the food. Select the food that you're tagging ("ribs"). If it's not available, you can edit the file under data > predefined-classes.txt (and commit the change to our repo).
10. Finalize the bounding box. It should be the smallest box that contains the entire food.
	For multiple servings of food:
		a. Foods in close proximity should be grouped within one RectBox -- avoid RectBox overlap
		b. Foods farther apart should be grouped individually -- minimize whitespace within Rectbox
11. Click 'Save' or type ``Ctrl`` + ``s``.
	Check the designated download folder to ensure .xml files are correctly populating.
12. Repeat steps 6-11 until you have gone through all images in the directory.
13. When you're done labeling all images, double check that they have the proper label ("ribs") in the top right of the program. You can click 'Edit Label' to bring up the selection box again.
	Check the designated download folder to ensure the number of .xml files downloaded matches the number of .jpeg files 
	on predator.
14. Exit out of the program.
15. Navigate to 'predator.local:5000' and go to Chopper > food_training > food_recognition > data
	Open up the correct data folder containing the .jpeg food training images. 
	Upload all .xml files.
16. Notify Arvind and Joel that images and labeling for food training are complete and uploaded to predator. 


Saving Image Files using Google Cloud
-------------------------------------
Precursor: Image Training
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Make sure the device has the latest master version of Oxide (at <https://github.com/markovcorp/cawfee/tree/master/oxide>) on it.
2. Open Nickel
3. Go to Settings > Level Settings > Training
4. Turn on Training Mode and enter a name for your training set (usually the food name you're training, such as "ribs").
5. Tap the back button twice to get to the main Nickel flow.
6. Place the food in Level and close the door. After recognition, you should see a toast confirming that an image was saved with your training name.
7. Take about 200 images of the food in various positions, rotations, and containers.
8. Make sure to turn off training mode when you're done.
9. Oxide will automatically sync the images to Google Cloud Storage. If it doesn't...

	-  If Oxide isn't installed or the device isn't associated yet, follow these instructions: <https://github.com/markovcorp/cawfee/tree/master/oxide#associating-your-device>.

	-  If your images aren't downloading in the ImageDownloader script below:
		-  See if the images made it to Google Cloud: https://console.cloud.google.com/storage/browser/blobstoreforimages.appspot.com?project=blobstoreforimages (type in your label name in the prefix search)
		-  Check that the images were actually saving to Android under Settings > Storage & USB > Explore > Pictures > FoodRecognition
		-  Check the latest sync date of your Level Setup account under Settings > Accounts > Level (and toggle the Cooking Session data toggle)


Using LabelImg
^^^^^^^^^^^^^^

1. Get the latest version of master for this repo on a computer that Parth can access remotely (like the Linux laptop between B2 and B3).
2. Run the downloader script: ``python ImageDownloader.py``. This will download the images from Google Cloud Storage to the local device. Please don't commit the new images to the repo.
3. Select the number of the training name that you had set in Nickel ("9: ribs"). This will open up all of your training images in the LabelImg program.
4. Make the program full window and zoom in (it will make labeling easier!)
5. Click 'Next Image' or type ``d``
6. Click 'Create RectBox' or type ``w``
7. Draw a bounding box by clicking and dragging.
8. A selection box will appear for you to label the food. Select the food that you're tagging ("ribs"). If it's not available, you can edit the file under data > predefined-classes.txt (and commit the change to our repo).
9. Finalize the bounding box. It should be the smallest box that contains the entire food.
10. Click 'Save' or type ``Ctrl`` + ``s``.
11. Repeat steps 5-10 until you have gone through all images in the directory.
12. When you're done labeling all images, double check that they have the proper label ("ribs") in the top right of the program. You can click 'Edit Label' to bring up the selection box again.
13. Exit out of the program.
14. Tell Joel and Arvind that you have trained and label every image. He'll retrieve the images from the computer.



----------


Original LabelImg README
========

.. image:: https://img.shields.io/pypi/v/labelimg.svg
        :target: https://pypi.python.org/pypi/labelimg

.. image:: https://img.shields.io/travis/tzutalin/labelImg.svg
        :target: https://travis-ci.org/tzutalin/labelImg

LabelImg is a graphical image annotation tool.

It is written in Python and uses Qt for its graphical interface.

Annotations are saved as XML files in PASCAL VOC format, the format used
by `ImageNet <http://www.image-net.org/>`__.

.. image:: https://raw.githubusercontent.com/tzutalin/labelImg/master/demo/demo3.jpg
     :alt: Demo Image

`Watch a demo video <https://youtu.be/p0nR2YsCY_U>`__

Installation
------------------

Download prebuilt binaries
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Windows & Linux <http://tzutalin.github.io/labelImg/>`__

-  OS X. Binaries for OS X are not yet available. Help would be appreciated. At present, it must be `built from source <#os-x>`__.

Build from source
~~~~~~~~~~~~~~~~~

Linux/Ubuntu/Mac requires at least `Python
2.6 <http://www.python.org/getit/>`__ and has been tested with `PyQt
4.8 <http://www.riverbankcomputing.co.uk/software/pyqt/intro>`__.


Ubuntu Linux
^^^^^^^^^^^^
Python 2 + Qt4

.. code::

    sudo apt-get install pyqt4-dev-tools
    sudo pip install lxml
    make qt4py2
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Python 3 + Qt5

.. code::

    sudo apt-get install pyqt5-dev-tools
    sudo pip3 install lxml
    make qt5py3
    python3 labelImg.py
    python3 labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

OS X
^^^^
Python 2 + Qt4

.. code::

    brew install qt qt4
    brew install libxml2
    make qt4py2
    python labelImg.py
    python  labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]


Windows
^^^^^^^

Download and setup `Python 2.6 or
later <https://www.python.org/downloads/windows/>`__,
`PyQt4 <https://www.riverbankcomputing.com/software/pyqt/download>`__
and `install lxml <http://lxml.de/installation.html>`__.

Open cmd and go to `labelImg <#labelimg>`__ directory

.. code::

    pyrcc4 -o resources.py resources.qrc
    python labelImg.py
    python labelImg.py [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

Get from PyPI
~~~~~~~~~~~~~~~~~
.. code::

    pip install labelImg
    labelImg
    labelImg [IMAGE_PATH] [PRE-DEFINED CLASS FILE]

I tested pip on Ubuntu14.04 and 16.04. However, I didn't test pip on MacOS and Windows

Use Docker
~~~~~~~~~~~~~~~~~
.. code::

    docker run -it \
    --user $(id -u) \
    -e DISPLAY=unix$DISPLAY \
    --workdir=$(pwd) \
    --volume="/home/$USER:/home/$USER" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    tzutalin/py2qt4

    make qt4py2;./labelImg.py

You can pull the image which has all of the installed and required dependencies. `Watch a demo video <https://youtu.be/nw1GexJzbCI>`__


Usage
-----

Steps
~~~~~

1. Build and launch using the instructions above.
2. Click 'Change default saved annotation folder' in Menu/File
3. Click 'Open Dir'
4. Click 'Create RectBox'
5. Click and release left mouse to select a region to annotate the rect
   box
6. You can use right mouse to drag the rect box to copy or move it

The annotation will be saved to the folder you specify.

You can refer to the below hotkeys to speed up your workflow.

Create pre-defined classes
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can edit the
`data/predefined\_classes.txt <https://github.com/tzutalin/labelImg/blob/master/data/predefined_classes.txt>`__
to load pre-defined classes

Hotkeys
~~~~~~~

+------------+--------------------------------------------+
| Ctrl + u   | Load all of the images from a directory    |
+------------+--------------------------------------------+
| Ctrl + r   | Change the default annotation target dir   |
+------------+--------------------------------------------+
| Ctrl + s   | Save                                       |
+------------+--------------------------------------------+
| Ctrl + d   | Copy the current label and rect box        |
+------------+--------------------------------------------+
| Space      | Flag the current image as verified         |
+------------+--------------------------------------------+
| w          | Create a rect box                          |
+------------+--------------------------------------------+
| d          | Next image                                 |
+------------+--------------------------------------------+
| a          | Previous image                             |
+------------+--------------------------------------------+
| del        | Delete the selected rect box               |
+------------+--------------------------------------------+
| Ctrl++     | Zoom in                                    |
+------------+--------------------------------------------+
| Ctrl--     | Zoom out                                   |
+------------+--------------------------------------------+
| ↑→↓←       | Keyboard arrows to move selected rect box  |
+------------+--------------------------------------------+

How to contribute
~~~~~~~~~~~~~~~~~

Send a pull request

License
~~~~~~~
`Free software: MIT license <https://github.com/tzutalin/labelImg/blob/master/LICENSE>`_


Related
~~~~~~~

1. `ImageNet Utils <https://github.com/tzutalin/ImageNet_Utils>`__ to
   download image, create a label text for machine learning, etc
2. `Docker hub to run it <https://hub.docker.com/r/tzutalin/py2qt4>`__
