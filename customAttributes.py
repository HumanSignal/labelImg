
from libs.attributes import AbstractAttributesWidgets
import os
import shutil

class AttributesManager( AbstractAttributesWidgets ):

    # used to implement the "natural order" of the various attributes definitions
    global_index = 0
    def next_index( self ):
        self.global_index = self.global_index + 1
        return self.global_index

    # just capture the destination
    def update_destination( self, destination ):
        self.destination = destination
        return True     

    # try to copy the current image file and create a new label file at the destination
    def copy_to_destination( self ):
        if self.destination is None:
            raise ValueError( "Can't copy to destination as destination is None" )

        if not os.path.isdir( self.destination ):
            raise ValueError( "Destination does not exist: {}".format( self.destination ) )
            
        image_filename = os.path.basename( self.mainWindow.filePath )
        # only need the root
        classification_filename = image_filename.split(".")[0]

        targetImagePath = os.path.join( self.destination, image_filename )
        targetClassificationPath = os.path.join( self.destination, classification_filename )

        print( "copy_to_destination: {}".format( targetImagePath )  )

        shutil.copyfile( self.mainWindow.filePath, targetImagePath ) 
        self.mainWindow.saveLabels( targetClassificationPath )
        
        return True     
        

    # specific actions specified above
    def get_global_attribute_definitions( self ):
        return {
            "destination": {
                "order": self.next_index(),
                "tooltip": "The directory to which the current image and it's PASCAL VOC file will be copied",            
                "default": "",
                "type": "text",
                "action": self.update_destination
            },
            "copy": {
                "order": self.next_index(),
                "tooltip": "Copy the current image and it's PASCAL VOC file the to directory specified in 'destination'",            
                "type": "button",
                "action": self.copy_to_destination
            }
        }  

    # same action in all cases from AttributesWidgets
    def get_image_attribute_definitions( self ):
        return {
            "comment": {
                "order": self.next_index(),
                "default": "",
                "type": "text",
                "action": self.update_image_attributes
            },
            "full-screen": {
                "order": self.next_index(),
                "tooltip": "Whether the full image is a candidate for training, or just crops of its objects",
                "default": "no",
                "type": "combo",
                "choices": [ "no", "yes" ],
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
            "weather": {
                "order": self.next_index(),
                "tooltip": "The quality of light in the image",
                "default": "cloudy",
                "type": "combo",
                "choices": [
                    "glary",                    
                    "sunny",
                    "bright", 
                    "cloudy", 
                    "dull",
                    "twilight",
                    "rainy", 
                    "snowy"
                ],
                "action": self.update_image_attributes
            },
            "duplicate": {
                "order": self.next_index(),
                "tooltip": "Is this image an effective duplicate of another",
                "default": "no",
                "type": "combo",
                "choices": [ "no", "yes" ],
                "action": self.update_image_attributes
            }
        }    

        
    # same action in all cases from AttributesWidgets
    def get_label_attribute_definitions( self ):
        return {
            "aspect": {
                "order": self.next_index(),
                "tooltip": "How is the object oriented with respect to it's face",
                "default": "",
                "type": "combo",
                "choices": [ 
                    "front", 
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
                "default": "3",
                "type": "combo",
                "choices": [ 
                    "1", 
                    "2", 
                    "3", 
                    "4", 
                    "5" 
                ],
                "action": self.update_label_attributes
            }
        }  
        