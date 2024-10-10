# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement

"""
simetrix.script
===============

Provides implementations of some SIMetrix Script functions.

"""

from enum import Enum

class FormatType(Enum):
    """Flag for specifying the format type to apply when using functions such as formatNumber()."""
    ENGINEERING=0
    """Engineering notation."""
    NORMAL=1,
    """Normal notation using 'E' if necessary."""
    INTEGER=2
    """Returns integer rounded to nearest value. Note rounding is in the same direction for negative and positive values. -1.2 -> -1, -1.7 -> -2.0"""

#FormatType = Enum('FormatType', ['Engineering', 'Integer', 'Normal'])

def formatNumber(value: float, significantDigits: int, format: FormatType = FormatType.ENGINEERING) -> str: 
    """Formats a real value and returns a string representation of it.
    
    Parameters
    ----------
    value : float
        Number to be formatted.
    significantDigits : int
        Significant digits to format for.
    format: FormatType, optional
        Specifies the format to apply.
    """
    ...