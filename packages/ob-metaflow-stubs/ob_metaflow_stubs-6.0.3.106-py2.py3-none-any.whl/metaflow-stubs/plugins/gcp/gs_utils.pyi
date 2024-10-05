##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.24.1+obcheckpoint(0.0.11);ob(v1)                              #
# Generated on 2024-10-04T19:10:58.955370                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowInternalError(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowGSPackageError(metaflow.exception.MetaflowException, metaclass=type):
    ...

def parse_gs_full_path(gs_uri):
    ...

def check_gs_deps(func):
    """
    The decorated function checks GS dependencies (as needed for Google Cloud storage backend). This includes
    various GCP SDK packages, as well as a Python version of >=3.7
    """
    ...

def process_gs_exception(*args, **kwargs):
    ...

