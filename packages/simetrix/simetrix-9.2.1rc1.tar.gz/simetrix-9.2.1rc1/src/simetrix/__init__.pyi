# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

"""
SIMetrix and SIMetrix/SIMPLIS Python Support
============================================

Provides a Python interface to some portions of the `SIMetrix/SIMPLIS <https://www.simetrix.co.uk>`__ application.

This is currently an experimental feature for use only with the `Design Verification Module (DVM) <https://www.simplistechnologies.com/product/dvm>`__,
running within a licensed instance of SIMetrix or SIMetrix/SIMPLIS.

Subpackages
-----------

dvm
    Design Verificaton Module (DVM) functionality.

script
    Functionality that implements certain functions from within the SIMetrix Script library.
"""

from __future__ import annotations
from typing import Iterator
from enum import Enum

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

class GraphObjectType(Enum):
    """Flag for specifying the type for a `GraphObject`."""
    NONE = 0
    """No type."""
    AXIS = 1
    """Axis type."""
    CROSSHAIR = 2
    """Crosshair type."""
    CROSSHAIRDIMENSION = 3
    """Crosshair dimension type."""
    CURVE = 4
    """Curve type."""
    CURVEDATA = 5
    """Curve data type."""
    CURVEMARKER = 6
    """Curve marker type."""
    FREETEXT = 7
    """Freetext type."""
    GRAPH = 8
    """Graph type."""
    GRID = 9
    """Grid type."""
    HISTOGRAM = 10
    """Histogram type."""
    LEGENDBOX = 11
    """Legend box type."""
    LEGENDTEXT = 12
    """Legend type."""
    MEASUREMENT = 13
    """Measurement type."""
    SHAREDAXIS = 14
    """Shared axis type."""
    SCATTERPLOT = 15
    """Scatter plot type."""
    SMALLCURSOR = 16
    """Small cursor type."""
    TEXTBOX = 17
    """Textbox type."""

class NumericValueType(Enum):
    """Flag for specifying whether a numeric value is a real or complex value."""
    REAL=0
    """Real number type."""
    COMPLEX=1
    """Complex number type."""

class GraphObject:
    """Base class for objects contained within a Graph.
    
    Graph objects have an id that is unique to the graph, along with a set of properties and a type.    
    """
    def id(self) -> int: 
        """Returns the ID of the object.
        
        Returns
        -------
        int
            ID of the object.        
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

    def type(self) -> GraphObjectType: 
        """Returns the object type.
        
        Returns
        -------
        GraphObjectType
            Object type.
        """        
        ...

class AbstractDataVector:
    """Base class for data vectors."""
    def size(self) -> int: 
        """Returns the number of elements in the vector.
        
        Returns
        -------
        int
            Number of elements in the vector.        
        """
        ...

    def type(self) -> NumericValueType: 
        """Returns the numeric value types for the data this contains.
        
        Data values are either real or complex values.

        Returns
        -------
        ValueType
            Numeric type for the values this holds.
        """
        ...

class AbstractXYDataVector:
    """Base clsas for data vectors containing X and Y data."""
    def size(self) -> int: 
        """Returns the number of elements in the vector.
        
        Returns
        -------
        int
            Number of elements in the vector.        
        """
        ...

    def type(self) -> NumericValueType:
        """Returns the numeric value types for the data this contains.
        
        Data values are either real or complex values.

        Returns
        -------
        ValueType
            Numeric type for the values this holds.
        """
        ...

    def x(self) -> AbstractDataVector: 
        """Returns a vector containing the X data.
        
        Returns
        -------
        AbstractDataVector
            Data vector containing the X data.        
        """
        ...
    def y(self) -> AbstractDataVector: 
        """Returns a vector containing the Y data.
        
        Returns
        -------
        AbstractDataVector
            Data vector containing the Y data.        
        """
        ...

class CurveData(GraphObject):
    """Represents the data held within a specific curve.
    
    A curve contains X-Y data vectors that can be accessed using the division(index: int) function.
    In many cases a curve may only contain a single division, but cases such as Monte-Carlo
    analysis there will be multiple divisions (in the case of Monte-Carlo analysis a division for
    each simulation run in the analysis). Each division will contain a full set of corresponding X and Y
    data.   
    """
    def division(self, index: int) -> AbstractXYDataVector: 
        """Returns the X-Y data vector for the given division index.
        
        Indexes start from 0, with a valid index being one in the range 0 <= index < numberDivisions().
        
        The first division can be obtained using 'division(0)'.

        Parameters
        ----------
        index : int
            Division index to obtain.

        Returns
        -------
        AbstractXYDataVector
            X-Y data vector at the given division index, or None if the index is invalid.        
        """
        ...

    def numberDivisions(self) -> int: 
        """Returns the number of divisions this contains.
        
        Returns
        -------
        int
            Number of divisions this contains.        
        """
        ...

class Curve(GraphObject):
    """Represents a curve within a Graph."""
    def data(self) -> CurveData: 
        """Returns the CurveData for the curve.
        
        Returns
        -------
        CurveData
            Data for this curve.        
        """
        ...



class RealDataVector(AbstractDataVector):
    """Data vector containing real values."""
    def __len__(self) -> int:
        """Returns the length of the array."""
        ...
    def __getitem__(self, index : int) -> float:
        """Returns the element at the given index.
        
        Parameters
        ----------
        index : int
            Index into the array.
        
        """
        ...
    def __iter__(self) -> Iterator[float]:
        """Value iterator."""
        ...
    

class RealXYDataVector(AbstractXYDataVector):
    """X-Y data vector containing real values."""
    def x(self) -> RealDataVector: 
        """Returns a vector containing the X data.
        
        Returns
        -------
        AbstractDataVector
            Data vector containing the X data.        
        """
        ...

    def y(self) -> RealDataVector:
        """Returns a vector containing the Y data.
        
        Returns
        -------
        AbstractDataVector
            Data vector containing the Y data.        
        """
        ...

class ComplexDataVector(AbstractDataVector):
    """Data vector containing complex values."""
    def __len__(self) -> int:
        """Returns the length of the array."""
        ...
    def __getitem__(self, index : int) -> complex:
        """Returns the element at the given index.
        
        Parameters
        ----------
        index : int
            Index into the array.
        
        """
        ...
    def __iter__(self) -> Iterator[complex]:
        """Value iterator."""
        ...

class ComplexXYDataVector(AbstractXYDataVector):
    """X-Y data vector containing complex values."""
    def x(self) -> ComplexDataVector: 
        """Returns a vector containing the X data.
        
        Returns
        -------
        AbstractDataVector
            Data vector containing the X data.        
        """
        ...
    def y(self) -> ComplexDataVector: 
        """Returns a vector containing the Y data.
        
        Returns
        -------
        AbstractDataVector
            Data vector containing the Y data.        
        """
        ...

class Graph(GraphObject):
    """Represents a graph. 
    
    A graph contains a set of curves.    
    """
    def curves(self) -> list[Curve]: 
        """Returns a list of curves this graph contains.
        
        Returns
        -------
        list[Curve]
            List of curves this graph contains.        
        """
        ...




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

class PartInstance(AbstractSchematicObject):
    """Represents an instance of a particular part within a schematic."""
    def symbolName(self) -> str: 
        """Returns the name of the symbol.
        
        Returns
        -------
        str
            Name of the associated symbol.
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

    def instance(self, handle: str) -> PartInstance: 
        """Returns the instance with the given handle.
        
        Parameters
        ----------
        handle : str
            Handle for the instance to return.
        
        Returns
        -------
        PartInstance
            The PartInstance within this schematic with that has the specified handle, or None if this contains
            no instance with that handle.        
        """        
        ...

    def instances(self) -> list[PartInstance]: 
        """Returns a list of the instances this contains.
        
        Returns
        -------
        list[PartInstance]
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

