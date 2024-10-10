# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

"""
Design Verification Module (DVM) - (simetrix.dvm)
=================================================

Provides DVM specific functionality for SIMetrix/SIMPLIS Python integration. Functionality is provided
for testplan pre-processing, post-processing and final-processing, by allowing access to the 
current testplan context and schematic control symbol.
"""

from . import PartInstance
from enum import Enum

class TestStatus(Enum):
    """Flag to indicate the status of a test."""
    PASS=0,
    """Test passed."""
    WARN=1,
    """Test generated a warning."""
    FAIL=2
    """Test failed."""
    

class ControlSymbol(PartInstance):
    """Represents the DVM control symbol in the schematic.
    
    This can be used to access circuit specifications for the test via the `properties()`, 
    along with the schematic it resides in and other component instances within the 
    same schematic.    
    """

    def circuitDescription(self) -> str: 
        """Returns the circuit description value.
        
        This is a convenience function and is equivalent to calling `propertyValue("CKT_DESC)`.
        """
        ...

    def circuitName(self) -> str: 
        """Returns the circuit name.
        
        This is a convenience function and is equivalent to calling `propertyValue("CKT_NAME)`.
        """
        ...

class LogTestDataResult:
    """Contains data held within the log file about a single result for a test."""
    def measurement(self) -> str: 
        """Returns the measurement."""
        ...
    def target(self) -> str: 
        """Returns the target."""
        ...
    def topology(self) -> str: 
        """Returns the topology."""
        ...
    def value(self) -> str: 
        """Returns the value."""
        ...

class LogTestData:
    """Contains data held within the log file about a single test. """
    def executed(self) -> str: 
        """Returns the executed string."""
        ...
    def logPath(self) -> str: 
        """Returns the path to the log file."""
        ...
    def progress(self) -> tuple[int, int]: 
        """Returns the progress as a tuple containing first the test number, and second
        the number of tests being run.
        """
        ...
    def rawData(self) -> list[str]: 
        """Returns the raw data from the log file."""
        ...

    def reportPath(self) -> str: 
        """Returns the path to the report file."""
        ...
    def results(self) -> list[LogTestDataResult]: 
        """Returns the results for the test."""
        ...
    def rstatus(self) -> str: 
        """Returns the status string."""
        ...
    def simulator(self) -> str: 
        """Returns the simulator statement."""
        ...
    def status(self) -> str: 
        """Returns the status string."""
        ...

class LogFile:
    """Represents the test log file."""
    def data(self, label: str) -> LogTestData: 
        """Reads the log file and returns the contents for the test with the given label.
        
        Parameters
        ----------

        label : str
                Label for the test to obtain the test data about.        
        """
        ...

class BasicTestContext:
    """Provides contextual information about a currently executing DVM test."""
    def label(self) -> str: 
        """Returns the label for the test.
        
        Returns
        -------
        str
            Label for the test.
        """
        ...
    def logData(self) -> LogTestData: 
        """Returns the log data about the active test."""
        ...
    def reportDirectory(self) -> str: 
        """Returns the path of the directory containing the report.
        
        Returns
        -------
        str
            Path of the directory containing the report.
        """
        ...

class ComplexTestContext(BasicTestContext):
    """
    Provides contextual information about a currently executing DVM test.
    """
    def promoteGraph(self, name: str, weight: int = None, fuzzyLogic: bool = None) -> None: 
        """Adds a graph to the overview report.

        This allows for multiple graphs to be listed within the report.
        
        Parameters
        ----------
        name : str
            Name of a DVM-generated graph to promote.
        weight : int, optional
            A number that indicates the order in which you want the graph to appear with the higher numbered graphs appearing first in the report.
        fuzzyLogic : bool, optional
            States whether the provided name is only an approximation, where if set to true the name will be searched for in the actual graph names in report.txt.        
        """
        ...
    def promoteScalar(self, name: str, value: str, newName: str = None) -> None: 
        """Adds a scalar to the overview report. 

        This allows for custom values to be specified within the report.
        
        Parameters
        ----------
        name : str
            Name of the scalar to add.
        value : str
            String value for the scalar to add.
        newName : str, optional
            New name for the added scalar.        
        """
        ...    
    def createScalar(self, name: str, value: str) -> None: 
        """Creates a scalar measurement.
        
        Parameters
        ----------
        name : str
            Name of the scalar.
        value : str
            Value for the scalar.        
        """
        ...
    def createSpecification(self, name: str, status: TestStatus, description: str) -> None: 
        """Creates a test specification.
        
        Parameters
        ----------
        name : str
            Name of the specification.
        status : TestStatus
            Status of the test.
        description : str
            Description for the specification.
        """
        ...
    def createStatistic(self, name: str, value: str) -> None: 
        """Creates a statistic.
        
        Parameters
        ----------
        name : str
            Name of the statistic.
        value : str
            Value for the statistic.        
        """
        ...
    def createStatisticSpecification(self, name: str, status: TestStatus, description: str) -> None: 
        """Creates a statistic specification.
        
        Parameters
        ----------
        name : str
            Name of the specification.
        status : TestStatus
            Status of the test.
        description : str
            Description for the specification.
        """
        ...

class PreTestContext(BasicTestContext):
    """
    Provides contextual information about a currently executing DVM.        
    """
    ...

class PostTestContext(ComplexTestContext):
    """
    Provides contextual information about a currently executing DVM.        
    """
    ...

class FinalTestContext(ComplexTestContext):
    """
    Provides contextual information about a currently executing DVM.        
    """
    ...