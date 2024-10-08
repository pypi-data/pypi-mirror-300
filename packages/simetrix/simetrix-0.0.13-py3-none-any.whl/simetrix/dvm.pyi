# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

from .schematic import Instance
from enum import Enum

"""SIMetrix and SIMetrix/SIMPLIS Python Support for DVM

Provides DVM specific functionality for SIMetrix/SIMPLIS Python integration.

This requires a running licensed instance of SIMetrix or SIMetrix/SIMPLIS.

Additional documentation can be found at:
https://www.simetrix.co.uk/documentation/
"""

class TestStatus(Enum):
    """Flag to indicate the status of a test."""
    PASS=0,
    """Test passed."""
    WARN=1,
    """Test generated a warning."""
    FAIL=2
    """Test failed."""
    

class ControlSymbol(Instance):
    def circuitDescription(self) -> str: ...
    def circuitName(self) -> str: ...

class LogTestDataResult:
    def measurement(self) -> str: ...
    def target(self) -> str: ...
    def topology(self) -> str: ...
    def value(self) -> str: ...

class LogTestData:
    def executed(self) -> str: ...
    def logPath(self) -> str: ...
    def progress(self) -> tuple[int, int]: ...
    def rawData(self) -> list[str]: ...
    def reportPath(self) -> str: ...
    def results(self) -> list[LogTestDataResult]: ...
    def rstatus(self) -> str: ...
    def simulator(self) -> str: ...
    def status(self) -> str: ...

class LogFile:
    def data(self, label: str) -> LogTestData: ...

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
    def logData(self) -> LogTestData: ...
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
        ...
    def createSpecification(self, name: str, status: TestStatus, description: str) -> None: ...
    def createStatistic(self, name: str, value: str) -> None: ...
    def createStatisticSpecification(self, name: str, status: TestStatus, description: str) -> None: ...

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