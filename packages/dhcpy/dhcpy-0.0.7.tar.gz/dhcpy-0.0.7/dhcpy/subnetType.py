"""
This file contains the SubnetType enum. This is used to determine the type of subnet that KEA is handling. This is
used to determine the type of pool to use and the commands to run on the server.
"""
from enum import Enum

class SubnetType(Enum):
    """Different types of subnets that KEA can handle. This is used to determine the type of pool to use and the
    commands to run on the server."""
    none = None
    """No subnet type set"""
    v4 = "subnet4"  # TODO: This is a guess
    """IPv4 subnet"""
    v6 = "subnet6"
    """IPv6 NA subnet"""
    pd = "subnet6-pd"  # TODO: This is a guess
    """IPv6 PD subnet"""
