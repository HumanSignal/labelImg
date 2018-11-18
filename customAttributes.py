
from libs.attributes import AbstractAttributesWidgets
import os
import shutil

class AttributesManager( AbstractAttributesWidgets ):

    # used to implement the "natural order" of the various attributes definitions
    global_index = 0
    def next_index( self ):
        self.global_index = self.global_index + 1
        return self.global_index

    # 
    def toggle_defaults_dirty( self, toggle ):
        self.defaults_dirty = toggle
        print( "defaults_dirty={}".format( self.defaults_dirty ) )
        return True     


    # just capture the destination
    def update_destination( self, destination ):
        self.destination = destination
        return True     

    def update_destination_class( self, destination_class_id ):
        print( "destination_class={}".format( self.mainWindow.labelHist[ destination_class_id ] ) )
        self.destination_class = self.mainWindow.labelHist[ destination_class_id ]
        return True          
        
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
        
        return True     

    # just capture rejects
    def update_rejects( self, rejects ):
        self.rejects = rejects
        return True          
        
    # move the current image file and label file to rejected
    def reject( self ):
        if not hasattr(self, "rejects") or self.rejects is None:
            self.mainWindow.errorMessage( "Copy to Rejects", "Rejects not defined!" )
            raise ValueError( "Rejects not defined!" )
        if not hasattr(self, "destination_class") or self.destination_class is None:
            self.mainWindow.errorMessage( "Copy to Rejects", "Destination Class not defined!" )
            raise ValueError( "Rejects Class not defined!" )

        try:
            rejects_path = os.path.join( self.rejects, self.destination_class )
        except Exception as e:
            print( "rejects={}, class={}".format( self.rejects, self.destination_class ) )
            raise e
            
            
        if not os.path.isdir( rejects_path ):
            self.mainWindow.errorMessage( "Copy to Rejects", "Rejects path does not exist: {}".format( rejects_path )  )
            raise ValueError( "Rejects path does not exist: {}".format( rejects_path ) )
            
        image_filename = os.path.basename( self.mainWindow.filePath )
        targetImagePath = os.path.join( rejects_path, image_filename )

        classification_root = self.mainWindow.filePath.split(".")[0] + ".xml"
        classification_filename = image_filename.split(".")[0] + ".xml"
        targetClassificationPath = os.path.join( rejects_path, classification_filename )
        
        shutil.move( self.mainWindow.filePath, targetImagePath )
        shutil.move( classification_root, targetClassificationPath )

        print( "rejected: {}".format( targetImagePath )  )

        
        return True             

    # specific actions specified above
    def get_global_attribute_definitions( self ):
        return {
            "destination": {
                "order": self.next_index(),
                "tooltip": "The root directory for class directories (to which the current image and it's PASCAL VOC file will be copied)",            
                "default": "D:/animals-count/data/estuarybank_12_v06/(pending)",
                "type": "text",
                "action": self.update_destination
            },
            "class": {
                "order": self.next_index(),
                "tooltip": "The class directory (under the root directory) to which the current image and it's PASCAL VOC file will be copied",
                "default": "unclassified",
                "type": "combo",
                "choices": [ c for c in self.mainWindow.labelHist ],
                "action": self.update_destination_class
            },
            "copy": {
                "order": self.next_index(),
                "tooltip": "Copy the current image and it's PASCAL VOC file the to directory specified in 'destination'",            
                "type": "button",
                "action": self.copy_to_destination_class
            },
            "set dirty": {
                "order": self.next_index(),
                "tooltip": "Whether the dirty flag should be set when assigning a default value (hence always saving when applied)",            
                "type": "checkbox",
                "default": "yes" if self.defaults_dirty else "no",
                "action": self.toggle_defaults_dirty
            },
            "rejects": {
                "order": self.next_index(),
                "tooltip": "The root directory for class directories (to which the current image and it's PASCAL VOC file will be rejected)",            
                "default": "D:/animals-count/data/estuarybank_12_v06/(rejects)",
                "type": "text",
                "action": self.update_rejects
            },
            "reject": {
                "order": self.next_index(),
                "tooltip": "Reject the current image and it's PASCAL VOC file the to rejection specified in 'rejects'",            
                "type": "button",
                "action": self.reject
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
                "type": "checkbox",
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
            },
            "duplicate": {
                "order": self.next_index(),
                "tooltip": "Is this image an effective duplicate of another",
                "default": "no",
                "type": "checkbox",
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
            "class-score": {
                "order": self.next_index(),
                "default": "",
                "type": "text",
                "action": self.update_image_attributes
            }

        }  
        