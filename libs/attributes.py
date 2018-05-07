# base implementation for AttributesManager

from PyQt4.QtGui import *
from xml.etree.ElementTree import SubElement

# imported by pascal_voc_io.py
def write_attributes_to_element( parent_element, attributes, use_attributes_element = True, use_attribute_element = True ):
    if attributes is not None and len( attributes ) > 0:
        if use_attributes_element:
            attributes_element = SubElement( parent_element, 'attributes')
        else:
            attributes_element = parent_element

        for attr in attributes:
            if use_attribute_element:
                attribute_element = SubElement( attributes_element, 'attribute')
                attribute_element.set( "key", attr )
            else:
                attribute_element = SubElement( attributes_element, attr )

            attribute_element.text = str( attributes[ attr ] )

# imported by pascal_voc_io.py
def read_attributes_from_element( parent_element, attributes ):
    try:
        attributes_element = parent_element.find("attributes")
        if attributes_element is not None:
            for attribute_element in attributes_element.findall("attribute"):
                attributes[ attribute_element.get( "key" ) ] = attribute_element.text
    except Exception as e:
        print( "Failed to read attributes: {}".format( e ) )

# attributes and widgets
class AttributesWidgets():

    def get_global_attribute_definitions(self):
        pass

    def get_image_attribute_definitions(self):
        pass

    def get_label_attribute_definitions(self):
        pass

    def __init__( self, mainWindow, dockWidgetArea ):
        self.mainWindow = mainWindow
        self.dockWidgetArea = dockWidgetArea
        self.installWidgets()

    def maybe_update_attribute( self, key, existing_attributes, new_value ):
        existing_value = None
        if key in existing_attributes:
            existing_value = existing_attributes[ key ]
        if existing_value != new_value:
            existing_attributes[ key ] = new_value
            self.mainWindow.setDirty()
            print( "updated attribute: key=[{}], new-value=[{}], old-value=[{}]".format( key, new_value, existing_value ) )

    def set_widget_value( self, widget, value):
        if type(widget) is QLineEdit:
            widget.setText( value )
        elif type( widget ) is QCheckBox:
            widget.setChecked( value == "yes" )
        elif type( widget ) is QRadioButton:
            widget.setChecked( value == "yes" )
        elif type(widget) is QComboBox:
            index = widget.findText( value )
            widget.setCurrentIndex( index)
        else:
            print( "set_widget_value: Unexpected type: {}".format( type( widget ) ) )

    def get_widget_value( self, widget ):
        if type(widget) is QLineEdit:
            return widget.text()
        elif type( widget ) is QCheckBox:
            if widget.isChecked():
                return "yes"
            else:
                return "no"
        elif type( widget ) is QRadioButton:
            if widget.isChecked():
                return "yes"
            else:
                return "no"
        elif type(widget) is QComboBox:
            return widget.currentText()
        else:
            print( "get_widget_value: Unexpected type: {}".format( type( widget ) ) )

    def build_widget( self, key, definition ):
        if "type" in definition:
            type = definition[ "type" ]
        else:
            type = "text"

        if "action" in definition:
            action = definition["action"]
        else:
            action = None

        if type == "text":
            widget = QLineEdit( self.mainWindow )
            if action is not None:
                widget.textEdited.connect( action )

        elif type == "button":
            widget = QPushButton( self.mainWindow )
            widget.setText( key )
            if action is not None:
                widget.pressed.connect( action )

        elif type == "radio":
            widget = QRadioButton( self.mainWindow )
            widget.setText( key )
            if action is not None:
                widget.toggled.connect( action )

        elif type == "checkbox":
            widget = QCheckBox( self.mainWindow )
            widget.setText( key )
            if action is not None:
                widget.toggled.connect( action )

        elif type == "combo":
            widget = QComboBox( self.mainWindow )
            if "choices" in definition:
                choices = definition["choices"]
                for choice in choices:
                    widget.addItem( choice )
            if "default" in definition:
                widget.defaultValue = definition["default"]
            else:
                widget.defaultValue = ""

            if action is not None:
                widget.activated.connect( action )
        else:
            raise ValueError( "Unexpected widget type: {}".format( type ) )

        if "tooltip" in definition and definition["tooltip"] is not None:
            widget.setToolTip( definition["tooltip"] )

        return widget;

    def build_widgets( self, layout, definitions ):
        widgets = {}

        # sort by explicit order if given else definition key
        sortedList = [ { "key": aw, "definition": definitions[ aw ], "order": aw if "order" not in definitions[ aw ] else definitions[ aw ]["order"] } for aw in definitions ]
        sortedList.sort( key=lambda x: x["order"] )

        for item in sortedList:
            key = item["key"]
            widget = self.build_widget( key, item["definition"] )
            layout.addRow( key, widget )
            widgets[ key ] = widget
        return widgets

    def installWidgetScope( self, widgetTitle, widgetName, definitions ):
        attributesLayout = QFormLayout()
        attributesContainer = QWidget()
        attributesContainer.setLayout( attributesLayout )
        attributesDock = QDockWidget( widgetTitle, self.mainWindow )
        attributesDock.setObjectName( widgetName )
        attributesDock.setWidget(attributesContainer)

        attributeWidgets = self.build_widgets( attributesLayout, definitions )
        self.mainWindow.addDockWidget( self.dockWidgetArea, attributesDock )
        return attributeWidgets

    def installWidgets( self ):
        self.mainWindow.attributes = {}

        self.imageAttributeWidgets = self.installWidgetScope(
            "Image Attributes",
            "ImageAttributes",
            self.get_image_attribute_definitions() )

        self.labelAttributeWidgets = self.installWidgetScope(
            "Label Attributes",
            "LabelAttributes",
            self.get_label_attribute_definitions() )

        self.globalAttributeWidgets = self.installWidgetScope(
            "Custom Operations",
            "CustomAttributes",
            self.get_global_attribute_definitions() )

    def loadAttributes(self, attributes, widgets ):
        for attr in widgets:
            widget = widgets[ attr ]
            if attributes is None:
                value = None
            elif attr in attributes:
                value = attributes[ attr ]
            elif hasattr( widget, "defaultValue" ):
                value = widget.defaultValue
                attributes[ attr ] = value
                print( "Assigned default attribute value: key=[{}], value=[{}]".format( attr, value ) )
                self.mainWindow.setDirty()
            else:
                value = None
            self.set_widget_value( widget, value )

    def update_image_attributes( self ):
        # but only if there's an image loaded
        if self.mainWindow.filePath:
            for w in self.imageAttributeWidgets:
                self.maybe_update_attribute(
                    w,
                    self.mainWindow.attributes,
                    self.get_widget_value( self.imageAttributeWidgets[ w ] ) )
        else:
            print( "No filepath: {}".format( self.mainWindow.filePath ) )

    def update_label_attributes( self ):
        shape = self.mainWindow.canvas.selectedShape
        if shape:
            for w in self.labelAttributeWidgets:
                self.maybe_update_attribute(
                    w,
                    shape.attributes,
                    self.get_widget_value( self.labelAttributeWidgets[ w ] ) )

# methods called by labelImg.py
class AbstractAttributesWidgets( AttributesWidgets ):

    def resetState( self ):
        for w in self.imageAttributeWidgets:
            self.set_widget_value( self.imageAttributeWidgets[w], None )
        for w in self.labelAttributeWidgets:
            self.set_widget_value( self.labelAttributeWidgets[w], None )

    def loadImageAttributes(self, image_attributes):
        self.mainWindow.attributes = image_attributes
        self.loadAttributes( image_attributes, self.imageAttributeWidgets)

    def loadLabelAttributes( self, label_attributes ):
        self.loadAttributes( label_attributes, self.labelAttributeWidgets)
