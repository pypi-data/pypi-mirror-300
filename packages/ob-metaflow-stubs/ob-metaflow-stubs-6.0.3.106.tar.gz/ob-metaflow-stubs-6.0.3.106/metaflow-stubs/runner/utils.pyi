##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.12.24.1+obcheckpoint(0.0.11);ob(v1)                              #
# Generated on 2024-10-04T19:10:58.921967                                        #
##################################################################################

from __future__ import annotations

import typing

TYPE_CHECKING: bool

def get_current_cell(ipython):
    ...

def format_flowfile(cell):
    """
    Formats the given cell content to create a valid Python script that can be executed as a Metaflow flow.
    """
    ...

def clear_and_set_os_environ(env: typing.Dict):
    ...

def check_process_status(command_obj: "CommandManager"):
    ...

def read_from_file_when_ready(file_path: str, command_obj: "CommandManager", timeout: float = 5):
    ...

def handle_timeout(tfp_runner_attribute, command_obj: "CommandManager", file_read_timeout: int):
    """
    Handle the timeout for a running subprocess command that reads a file
    and raises an error with appropriate logs if a TimeoutError occurs.
    
    Parameters
    ----------
    tfp_runner_attribute : NamedTemporaryFile
        Temporary file that stores runner attribute data.
    command_obj : CommandManager
        Command manager object that encapsulates the running command details.
    file_read_timeout : int
        Timeout for reading the file.
    
    Returns
    -------
    str
        Content read from the temporary file.
    
    Raises
    ------
    RuntimeError
        If a TimeoutError occurs, it raises a RuntimeError with the command's
        stdout and stderr logs.
    """
    ...

