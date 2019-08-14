
from libs.pascal_voc_io import PascalVocReader
from libs.pascal_voc_io import XML_EXT
from libs.attributes import AbstractAttributesWidgets
import os
import time
from threading import Thread
from threading import Event
import shutil

from ast import literal_eval as make_tuple

from PyQt5 import Qt


class_filters = {}
image_index = -1
image_classes_cache = {}

def toggle( class_name ):
    new_value = not class_filters[ class_name ] if class_name in class_filters else True
    class_filters[ class_name ] = new_value
    print( "toggle [{}]: {}".format( class_name, class_filters[ class_name ] ) )


def get_meta( image_path=None, xml_dir=None ):
    basename = os.path.basename( os.path.splitext( image_path )[0] )
    meta_path = os.path.join( xml_dir, basename + XML_EXT )
    if os.path.isfile( meta_path ):
        reader = PascalVocReader( meta_path )
        reader.parseXML()
        return reader
    else:
        return None

def get_meta_shapes( image_path, xml_dir=None ):
    meta = get_meta( image_path, xml_dir )
    if meta is None:
        return []
    else:
        return meta.getShapes()


class AttributesManager( AbstractAttributesWidgets ):

    # used to implement the "natural order" of the various attributes definitions
    global_index = 0
    filter_by_class = True
    filter_func = None

    def get_next_path( self, reverse=False ):

        image_paths = self.mainWindow.mImgList
        current_path = self.mainWindow.filePath
        xml_dir = self.mainWindow.defaultSaveDir

        if len(image_paths) <= 0:
            return None

        image_path = None

        if not reverse and current_path is None:
            image_index = 0
        elif reverse and current_path is None:
            image_index = len( image_paths ) - 1
        else:
            image_index = image_paths.index( current_path )

        image_path = image_paths[ image_index ]

        if self.filter_func is None:
            print( "next_filtered_path: reverse={}, filters={}".format( reverse, class_filters ) )
        else:
            print( "next_filtered_path: reverse={}, func={}".format( reverse, self.filter_func ) )


        while True:

            if not reverse and ( image_index < ( len( image_paths ) - 1 ) ):
                image_index = image_index + 1

            elif reverse and ( image_index > 0 ):
                image_index = image_index - 1
            else:
                self.mainWindow.errorMessage( "get_next_path", "No more filtered shapes!" )
                return current_path

            image_path = image_paths[ image_index ]

            self.mainWindow.status( "Searching: index=[{}], file=[{}] ".format( image_index, image_path ), delay=5000 )

            if image_path not in image_classes_cache:
                shapes = get_meta_shapes( image_path, xml_dir )
                # cache the shapes
                image_classes_cache[ image_path ] = shapes
            else:
                shapes = image_classes_cache[ image_path ]


            for shape in shapes:
                key = shape[ 0 ]
                if self.filter_func is None:
                    if key in class_filters and class_filters[ key ]:
                        print( "Matched filter [{}] at index [{}:{}]".format( key, image_index, image_path ) )
                        return image_path
                    else:
                        print( "No filter for: [{}]".format( key ) )
                else:
                    if self.filter_func( shape ):
                        print( "Matched filter_func at index [{}:{}]".format( image_index, image_path ) )
                        return image_path

            image_index = image_index + ( -1 if reverse else 1 )



    def next_index( self ):
        self.global_index = self.global_index + 1
        return self.global_index

    #
    def toggle_defaults_dirty( self, toggle ):
        self.defaults_dirty = toggle
        print( "defaults_dirty={}".format( self.defaults_dirty ) )
        return True

    def toggle_filter_by_class( self, toggle ):
        self.filter_by_class = toggle
        print( "filter_by_class={}".format( self.filter_by_class ) )
        return True

    # just capture the destination
    def update_destination( self, destination ):
        self.destination = destination
        return True

    def update_destination_class( self, destination_class_id ):
        print( "destination_class={}".format( self.mainWindow.labelHist[ destination_class_id ] ) )
        self.destination_class = self.mainWindow.labelHist[ destination_class_id ]

        class_filters.clear()
        class_filters[ self.destination_class ] = True
        print( "class_filters={}".format( class_filters ) )

        return True

    # just capture the destination
    def update_slideshow_fps( self, slideshow_fps ):
        self.slideshow_fps = int( slideshow_fps )
        return True

    def slideshow( self ):

        if hasattr( self, 'slideshow_timer') and self.slideshow_timer is not None:
            self.slideshow_timer = None
            print("Stopped slideshow")
        else:

            self.slideshow_timer = 1

            fps = self.slideshow_fps if hasattr( self, 'slideshow_fps') else 2
            spf = 1 / fps
            interval = int( 1000 * spf )

            def has_more_images():
                if len(self.mainWindow.mImgList) <= 0:
                    return False

                filename = None
                if self.mainWindow.filePath is None:
                    filename = self.mainWindow.mImgList[0]
                else:
                    currIndex = self.mainWindow.mImgList.index(self.mainWindow.filePath)
                    if currIndex + 1 < len(self.mainWindow.mImgList):
                        return True
                    else:
                        return False

            def local():
                if not has_more_images():
                    print("Stopping slideshow: no more images.")
                    self.slideshow_timer = None
            
                if self.slideshow_timer is not None:
                    self.mainWindow.openNextImg()
                    Qt.QTimer.singleShot( interval, local )

            print("Starting slideshow: fps={}, spf={}, interval={}".format( fps, spf, interval ))

            local()




    # try to copy the current image file and create a new label file at the destination
    def copy_to_destination_class( self ):
        if not hasattr(self, "destination") or self.destination is None:
            self.mainWindow.errorMessage( "Copy to Destination", "Destination not defined!" )
            raise ValueError( "Destination not defined!" )
        if not hasattr(self, "destination_class") or self.destination_class is None:
            self.mainWindow.errorMessage( "Copy to Destination", "Destination Class not defined!" )
            raise ValueError( "Destination Class not defined!" )

        try:
            destination_path = os.path.join( self.destination, self.destination_class )
        except Exception as e:
            print( "destination={}, class={}".format( self.destination, self.destination_class ) )
            raise e


        if not os.path.isdir( destination_path ):
            self.mainWindow.errorMessage( "Copy to Destination", "Destination path does not exist: {}".format( destination_path )  )
            raise ValueError( "Destination path does not exist: {}".format( destination_path ) )

        image_filename = os.path.basename( self.mainWindow.filePath )
        # only need the root
        classification_filename = image_filename.split(".")[0]

        targetImagePath = os.path.join( destination_path, image_filename )
        targetClassificationPath = os.path.join( destination_path, classification_filename )

        print( "copy_to_destination: {}".format( targetImagePath )  )

        shutil.copyfile( self.mainWindow.filePath, targetImagePath )
        self.mainWindow.saveLabels( targetClassificationPath )

        # and save the original in place
        self.mainWindow.saveFile()

        return True

    # just capture
    def update_move_destination( self, move_destination ):
        self.move_destination = move_destination
        return True

    def update_min_max_score( self, min_max_score ):
        try:
            try:
                min_score, max_score = make_tuple( "({})".format( min_max_score ) )

                # create function: no score means 0
                def filter_func( shape ):
                    score = shape[ 5 ]
                    return 0 if score is None else ( min_score <= score ) and ( score <= max_score )

            except:
                min_score = float( min_max_score )

                # create function: no score means 0
                def filter_func( shape ):
                    score = shape[ 5 ]
                    return 0 if score is None else min_score <= score


            self.filter_func = filter_func

            print( "Created filter_func: score range: {}".format( min_max_score ) )

        except Exception as e:
            self.filter_func = None
            print( "Removed filter function: {}".format( e ) )
        return True


    # move the current image file and label file
    def move( self ):
        if not hasattr(self, "move_destination") or self.move_destination is None:
            self.mainWindow.errorMessage( "Move", "Move destination not defined!" )
            raise ValueError( "Move destination not defined!" )
        if not hasattr(self, "destination_class") or self.destination_class is None:
            self.mainWindow.errorMessage( "Move", "Destination Class not defined!" )
            raise ValueError( "destination Class not defined!" )

        try:
            move_path = os.path.join( self.move_destination, self.destination_class )
        except Exception as e:
            print( "rejects={}, class={}".format( self.move_destination, self.destination_class ) )
            raise e


        if not os.path.isdir( move_path ):
            self.mainWindow.errorMessage( "Move", "Move path does not exist: {}".format( move_path )  )
            raise ValueError( "Move path does not exist: {}".format( move_path ) )

        image_filename = os.path.basename( self.mainWindow.filePath )
        targetImagePath = os.path.join( move_path, image_filename )

        classification_root = self.mainWindow.filePath.split(".")[0] + ".xml"
        classification_filename = image_filename.split(".")[0] + ".xml"
        targetClassificationPath = os.path.join( move_path, classification_filename )

        shutil.move( self.mainWindow.filePath, targetImagePath )
        print( "moved: [{}] to [{}]".format( self.mainWindow.filePath, targetImagePath )  )

        shutil.move( classification_root, targetClassificationPath )
        print( "moved: [{}] to [{}]".format( classification_root, targetClassificationPath )  )


        # now refresh lists
        index = self.mainWindow.mImgList.index( self.mainWindow.filePath )
        self.mainWindow.mImgList.pop( index )

        if index > 0:
            self.mainWindow.filePath = self.mainWindow.mImgList[ index - 1 ]
        else:
            if len( self.mainWindow.mImgList ) > 0:
                self.mainWindow.filePath = self.mainWindow.mImgList[ 0 ]
            else:
                self.mainWindow.filePath = None

        self.mainWindow.openNextImg()

        return True

    # specific actions specified above
    def get_global_attribute_definitions( self ):
        g_defs = [
            (
                "Operations",
                "operations",
                {
                    "previous": {
                        "order": self.next_index(),
                        "tooltip": "Previous image matching filter.",
                        "type": "button",
                        "action": lambda : self.mainWindow.loadFile( self.get_next_path( reverse=True ) )
                    },

                    "next": {
                        "order": self.next_index(),
                        "tooltip": "Next image matching filter.",
                        "type": "button",
                        "action": lambda : self.mainWindow.loadFile( self.get_next_path( ) )
                    },

                    "empty cache": {
                        "order": self.next_index(),
                        "tooltip": "Clears the image class cache (e.g. if changed directories).",
                        "type": "button",
                        "action": lambda : image_classes_cache.clear()
                    },

                    "min/max score": {
                        "order": self.next_index(),
                        "tooltip": "Filter by min/max score.",
                        "default": "0.5",
                        "type": "text",
                        "action": self.update_min_max_score
                    },

                    "class": {
                        "order": self.next_index(),
                        "tooltip": "A class directory (under a root directory). See copy & move.",
                        "default": "unclassified",
                        "type": "combo",
                        "choices": [ c for c in self.mainWindow.labelHist ],
                        "action": self.update_destination_class
                    },

                    "copy destination": {
                        "order": self.next_index(),
                        "tooltip": "The root directory for class directories (to which the current image and it's PASCAL VOC file will be copied)",
                        "default": "D:/animals-count/data/estuarybank_12_v06/(pending)",
                        "type": "text",
                        "action": self.update_destination
                    },

                    "copy": {
                        "order": self.next_index(),
                        "tooltip": "Copy the current image and it's PASCAL VOC file the to the class folder in copy destination",
                        "type": "button",
                        "action": self.copy_to_destination_class
                    },

                    "move destination": {
                        "order": self.next_index(),
                        "tooltip": "The root directory for class directories (to which the current image and it's PASCAL VOC file will be moved)",
                        "default": "D:/animals-count/data/estuarybank_12_v06/(rejects)",
                        "type": "text",
                        "action": self.update_move_destination
                    },

                    "move": {
                        "order": self.next_index(),
                        "tooltip": "Move the current image and it's PASCAL VOC file the to the class folder in move destination",
                        "type": "button",
                        "action": self.move
                    },

                    "set dirty": {
                        "order": self.next_index(),
                        "tooltip": "Whether the dirty flag should be set when assigning a default value (hence always saving when applied)",
                        "type": "checkbox",
                        "default": "yes" if self.defaults_dirty else "no",
                        "action": self.toggle_defaults_dirty
                    },

                    "run": {
                        "order": self.next_index(),
                        "tooltip": "Run through the image set.",
                        "type": "button",
                        "action": lambda : self.slideshow( )
                    },

                    "run_fps": {
                        "order": self.next_index(),
                        "tooltip": "Frames per second to run slideshow",
                        "default": "5",
                        "type": "text",
                        "action": self.update_slideshow_fps
                    }
                }
            )
        ]

        # generate checkbox for each class
        #filters = {}

        # generate checkbox for each class
        #for class_name in self.mainWindow.labelHist:
        #
        #    class_filters[ class_name ] = False
        #
        #    filters[ class_name ] = {
        #        "order": self.next_index(),
        #        "tooltip": "Whether to include images with recorded class [{}].".format( class_name ),
        #        "default": "no",
        #        "type": "checkbox",
        #        "action": eval( 'lambda: toggle( "{}" )'.format( class_name ) )
        #    }

        #g_defs.append( ( "Filters", "filters", filters, 2 ) )

        return g_defs




    # same action in all cases from AttributesWidgets
    def get_image_attribute_definitions( self ):
        return {
            "untruth": {
                "order": self.next_index(),
                "default": "",
                "type": "text",
                "action": self.update_image_attributes
            },
            "untruth-count": {
                "order": self.next_index(),
                "default": 0,
                "type": "text",
                "action": self.update_image_attributes
            },
            "quality": {
                "order": self.next_index(),
                "tooltip": "The overall image quality: focus, composition, interest, whatever",
                "default": "ok",
                "type": "combo",
                "choices": [
                    "bad",
                    "poor",
                    "ok",
                    "good",
                    "excellent"
                ],
                "action": self.update_image_attributes
            },
            "light": {
                "order": self.next_index(),
                "tooltip": "The quality of light in the image",
                "default": "",
                "type": "combo",
                "choices": [
                    "glary",
                    "sunny",
                    "bright",
                    "cloudy",
                    "dull",
                    "twilight",
                    "dark"
                ],
                "action": self.update_image_attributes
            },
            "weather": {
                "order": self.next_index(),
                "tooltip": "The quality of light in the image",
                "default": "",
                "type": "combo",
                "choices": [
                    "sunny",
                    "overcast",
                    "rainy",
                    "snowy"
                ],
                "action": self.update_image_attributes
            }
        }


    # same action in all cases from AttributesWidgets
    def get_label_attribute_definitions( self ):
        return {
            "aspect": {
                "order": self.next_index(),
                "tooltip": "How is the object oriented with respect to it's face",
                "default": "back",
                "type": "combo",
                "choices": [
                    "front",
                    "back",
                    "rear",
                    "left",
                    "right",
                    "top",
                    "bottom",
                    "front left",
                    "front right",
                    "rear left",
                    "rear right"
                ],
                "action": self.update_label_attributes
            },
            "quality": {
                "order": self.next_index(),
                "tooltip": "What span of the the category's features does this object exhibit",
                "default": "ok",
                "type": "combo",
                "choices": [
                    "bad",
                    "poor",
                    "ok",
                    "good",
                    "excellent"
                ],
                "action": self.update_label_attributes
            },
            "cardinality": {
                "order": self.next_index(),
                "tooltip": "How much of a stereotype, or archetype, of the category does this object represent: 1 - a little, 5 - a lot",
                "type": "text",
                "action": self.update_label_attributes
            },
            "box-score": {
                "order": self.next_index(),
                "default": "",
                "type": "text",
                "action": self.update_image_attributes
            },
            "class-error": {
                "order": self.next_index(),
                "default": "",
                "type": "text",
                "action": self.update_image_attributes
            },
            "class-error-score": {
                "order": self.next_index(),
                "default": "",
                "type": "text",
                "action": self.update_image_attributes
            }

        }
