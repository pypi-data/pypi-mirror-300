# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

from . import Properties
from enum import Enum, auto

"""SIMetrix and SIMetrix/SIMPLIS Python Support for Graphs.

Provides graph specific functionality for SIMetrix/SIMPLIS Python integration.

This requires a running licensed instance of SIMetrix or SIMetrix/SIMPLIS.

Additional documentation can be found at:
https://www.simetrix.co.uk/documentation/
"""

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

class ValueType(Enum):
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

    def type(self) -> ValueType: 
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

    def type(self) -> ValueType:
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
    pass

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
    pass

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
