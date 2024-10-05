##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.24.1+obcheckpoint(0.0.11);ob(v1)                              #
# Generated on 2024-10-04T19:10:58.955088                                        #
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

class MetaflowGSPackageError(metaflow.exception.MetaflowException, metaclass=type):
    ...

