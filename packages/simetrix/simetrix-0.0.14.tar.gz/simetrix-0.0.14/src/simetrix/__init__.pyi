# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

"""SIMetrix and SIMetrix/SIMPLIS Python Support

Provides Python script access to portions of the SIMetrix/SIMPLIS application.

This requires a running licensed instance of SIMetrix or SIMetrix/SIMPLIS.

Additional documentation can be found at:
https://www.simetrix.co.uk/documentation/
"""

from typing import Iterator

from . import schematic as schematic
from . import waveform as waveform

class Property:
    """Data structure representing a property.

    A property is a combination of a name and a value, where property values are represented 
    as strings.

    Once created, a property cannot have its name changed. This is to prevent a set of properties
    from becoming invalid with two properties having the same name.
    """
    def name(self) -> str: 
        """Returns the name of the property."""
        ...
    def value(self) -> str: 
        """Returns the value of the property as a string."""
        ...
    def setValue(self, value: str) -> str: 
        """Sets the property value."""
        ...


class Properties:
    """Data structure representing a collection of property values.
    
    The collection of properties is a set with uniqueness determined by the property name using a 
    case-insensitive comparison. When properties are added, any existing property with the same 
    name are overwritten with the new property.     
    """
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Property: ...
    def __iter__(self) -> Iterator[Property]: ...
    def add(self, name: str, value: str) -> None: 
        """Adds a property.
        
        If a property already exists with the same name using case-insensitive comparison, the existing 
        property is replaced with this new property.

        Parameters
        ----------
        name : str
            The name of the property.
        value : str
            The value of the property.        
        """
        ...
    def add(self, property: Property) -> None: 
        """Adds a property.

        If a property already exists with the same name using case-insensitive comparison, the existing 
        property is replaced with this new property.
        
        Parameters
        ----------
        property : Property
            The property to add.
        """
        ...
    def contains(self, name: str) -> bool: 
        """Returns whether a property with the given name exists within this set of properties.
        
        Properties are searched for using a case-insensitive search of the name.

        Parameters
        ----------
        name : str
            Name of the property to find.

        Returns
        -------
        bool
            True if this contains a property with the given name, false otherwise. 
        """
        ...

class Graph(waveform.GraphObject):
    """Represents a graph. 
    
    A graph contains a set of curves.    
    """
    def curves(self) -> list[waveform.Curve]: 
        """Returns a list of curves this graph contains.
        
        Returns
        -------
        list[Curve]
            List of curves this graph contains.        
        """
        ...

class Schematic:
    """Represents a schematic.
    
    A schematic contains a collection of schematic objects, such as symbol instances. It also contains
    a set of properties along with a handle that is unique to the running application.    
    """
    def handle(self) -> str: 
        """Returns the handle.
        
        Returns
        -------
        str
            Returns the handle.        
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

    def instance(self, handle: str) -> schematic.Instance: 
        """Returns the instance with the given handle.
        
        Parameters
        ----------
        handle : str
            Handle for the instance to return.
        
        Returns
        -------
        Instance
            The Instance within this schematic with that has the specified handle, or None if this contains
            no instance with that handle.        
        """        
        ...

    def instances(self) -> list[schematic.Instance]: 
        """Returns a list of the instances this contains.
        
        Returns
        -------
        list[Instance]
            List of instances that this schematic contains.        
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

    def select(self) -> None: ...

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



def currentGraph() -> Graph: 
    """Returns the currently active graph.
    
    Returns
    -------
    Graph
        The currently active graph, or None if there is no active graph.
    """
    ...
def currentSchematic() -> Schematic: 
    """Returns the currently active schematic.
    
    Returns
    -------
    Schematic
        The currently active schematic, or None if there is no active schematic.
    """
    ...

def getSchematicFromHandle(handle: int) -> Schematic: 
    """Returns the schematic with the given handle.
    
    Parameters
    ----------
    handle : int
        Handle of the schematic to obtain.

    Returns
    -------
    Schematic
        The schematic with the given handle, or None if there is no schematic with that handle.    
    """
    ...

def graphs() -> list[Graph]: 
    """Returns a list of open graphs.
    
    Returns
    -------
    list[Graph]
        A list of open graphs.    
    """
    ...
    
def openSchematic(path: str) -> Schematic: 
    """Opens a schematic.
    
    Parameters
    ----------
    path : str
        Path of the schematic to open.

    Returns
    -------
    Schematic
        Schematic that was opened, or None if the schematic could not be opened.    
    """
    ...

def schematics() -> list[Schematic]: 
    """Returns a list of open schematics.
    
    Returns
    -------
    list[Schematic]
        List of open schematics.
    """
    ...

