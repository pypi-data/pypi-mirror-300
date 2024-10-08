# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

from . import Properties, Schematic

"""
imetrix.schematic
=================

Provides schematic specific functionality for SIMetrix/SIMPLIS Python integration. Accessed
via a `simetrix.Schematic` element, this subpackage provides implementations for schematic objects
including component instances.

"""

class AbstractSchematicObject:
    """Base class for all schematic objects.
    
    Schematic objects are objects that exist within a schematic. They have a unique to the schematic
    handle, along with a set of properties.    
    """
    def handle(self) -> str: 
        """Returns the object handle.
        
        Returns
        -------
        str
            Handle for this object.        
        """
        ...
    def hasProperty(self, name: str) -> bool: 
        """Returns whether the object has a property with the given name.
        
        Properties are compared using a case-insensitive comparison of their names.

        Parameters
        ----------
        name : str
            Name of the property to search for.

        Returns
        -------
        bool
            True if a property with the specified name exists in this object, false otherwise.        
        """        
        ...

    def properties(self) -> Properties: 
        """Returns the set of properties for this object.
        
        Returns
        -------
        simetrix.Properties
            Set of properties for this object.
        """    
        ...

    def propertyNames(self) -> list[str]: 
        """Returns a list of all property names for this object.
        
        Returns
        -------
        list[str]
            List of property names for this object.        
        """
        ...

    def propertyValue(self, name: str) -> str: 
        """Returns the value for the property with the given name.
        
        Properties within this object are searched for using a case-insensitive comparison of the names.

        Returns
        -------
        str
            Value for the property in this object with the given name, or None if there is no property with the given name in this object.        
        """
        ...

    def schematic(self) -> Schematic: 
        """Returns the Schematic that this object is containined within.
        
        Returns
        -------
        Schematic
            The Schematic containing this object.        
        """
        ...


    def setProperty(self, name: str, value: str) -> None: 
        """Sets a property for this object with the given name and value.
        
        If a property already exists within this object with the same name as provided, the existing property 
        is overwritten with the new property. Otherwise if no property exists with the provided name, a new 
        property is added to this object.
        
        Properties are compared using a case-insensitive comparison of their names.

        Parameters
        ----------
        name : str
            Name of the property.
        value : 
            Value of the property.
        """
        ...

class Instance(AbstractSchematicObject):
    """Represents an instance of a particular symbol within a schematic."""
    def symbolName(self) -> str: 
        """Returns the name of the symbol.
        
        Returns
        -------
        str
            Name of the associated symbol.
        """
        ...


    
