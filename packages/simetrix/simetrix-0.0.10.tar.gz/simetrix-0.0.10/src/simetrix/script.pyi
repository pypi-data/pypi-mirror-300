# SPDX-FileCopyrightText: 2024-present SIMetrix Technologies Ltd, SIMPLIS Technologies Inc.
#
# SPDX-License-Identifier: SIMetrix and SIMetrix/SIMPLIS End User Licence Agreement
from enum import Enum

"""SIMetrix and SIMetrix/SIMPLIS Python Support for legacy SIMetrix Script operations.

Provides legacy SIMetrix Script specific functionality for SIMetrix/SIMPLIS Python integration.

This requires a running licensed instance of SIMetrix or SIMetrix/SIMPLIS.

Additional documentation can be found at:
https://www.simetrix.co.uk/documentation/"""

FormatType = Enum('FormatType', ['Engineering', 'Integer', 'Normal'])

def formatNumber(value: float, significantDigits: int, format: FormatType = FormatType.Engineering) -> str: 
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