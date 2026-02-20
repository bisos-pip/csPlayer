from __future__ import annotations

from os import path
import logging

from bisos.csPlayer import drf_csPlayer_abstract as drf

from bisos.csPlayer import auditTrail_csu

import pathlib

import subprocess
# import json

import importlib.util


logger = logging.getLogger(__name__)

def executablesInfo_load(executablesFolderName: str,) -> None:
    """ Walkthrough and load CSXU operations from enabled directory based on folder name """

    # Get the enabled base directory using the folder name
    enabledBaseDir = folderNameToEnabledBase(executablesFolderName)

    if enabledBaseDir is None:
        logger.error(f"Failed to get enabled base directory for folder: {executablesFolderName}")
        return None

    try:
        for each in enabledBaseDir.iterdir():
            if each.is_dir():
                # NOTE To AI: In  that directory look for a file called derived/drfExecutable.py
                # if that file exists, import it, otherwise log it as missing
                derived_file = each / "derived/drfExecutable.py"
                if derived_file.exists():
                    spec = importlib.util.spec_from_file_location("drfExecutable", str(derived_file))
                    drfExecutable = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(drfExecutable)
                else:
                    logger.warning(f"Missing derived/drfExecutable.py in {each}")
    except OSError as e:
        logger.error(f"Error iterating directory {enabledBaseDir}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in csxuFolderObtain: {e}")
        return None

    return


def csxuLineExecute(operationBranch: list[str], command: list[str], servers: list[str]) -> dict:
    """Execute the operation with the given command and servers."""

    print(f"submitOperation: operationBranch={operationBranch}, command={command}, servers={servers}")
    # print(f"submitOperation: fullCommand={fullCommand}")

    return (
        auditTrail_csu.drf_xuLineRun(
            xuSetTree=operationBranch,
            xuLineList=command,
            destinations=servers,
        )
    )


def folderNameToEnabledBase(folderName: str) -> pathlib.Path | None:
    nameToBaseDict = {
        "pip:bisos3": "/bisos/var/csxu/pip_bisos3/enabled",
        "pip:dev-bisos3": "/bisos/var/csxu/pip_dev-bisos3/enabled",
        "pipx": "/bisos/var/csxu/pipx/enabled",
        "modules:facter": "/bisos/var/csxu/moduled/facterModule.cs/enabled",
        "modules:soncli": "/bisos/var/csxu/moduled/soncli.cs/enabled",
    }
    
    if folderName not in nameToBaseDict:
        logger.error(f"Unknown folderName: {folderName}. Valid options are: {list(nameToBaseDict.keys())}")
        return None
    
    basePath = pathlib.Path(nameToBaseDict[folderName])
    
    if not basePath.exists():
        logger.error(f"Directory does not exist: {basePath}")
        return None
    
    if not basePath.is_dir():
        logger.error(f"Path is not a directory: {basePath}")
        return None
    
    return basePath

xuSetTreeNameToXuSetBaseDir = folderNameToEnabledBase


def csxuFolderObtain(csxuFolder: drf.OperationFolder,) -> drf.OperationFolder | None:
    """ Create list of executables """
    
    if csxuFolder is None:
        logger.error("csxuFolder parameter is None")
        return None
    
    folderName = csxuFolder.name
    if not folderName:
        logger.error("csxuFolder.name is empty")
        return None
    
    # Get the enabled base directory using the folder name
    enabledBaseDir = folderNameToEnabledBase(folderName)
    
    if enabledBaseDir is None:
        logger.error(f"Failed to get enabled base directory for folder: {folderName}")
        return None
    
    try:
        for each in enabledBaseDir.iterdir():
            if each.is_dir():
                csxuFolder.portfolio.append(drf.Operation(name=each.name, operation_type=drf.OperationType.PIPX))
    except OSError as e:
        logger.error(f"Error iterating directory {enabledBaseDir}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in csxuFolderObtain: {e}")
        return None
    
    return csxuFolder


def xuNameInXuSetBaseDir(
        xuName: str,
        xuSetBaseDir: pathlib.Path,
) -> pathlib.Path | None:
    """ Walkthrough xuSetBaseDir to find the specified xuName """
    if xuSetBaseDir is None:
        logger.error("xuSetBaseDir parameter is None")
        return None

    xuNamePath = xuSetBaseDir / xuName
    
    if not xuNamePath.exists():
        logger.error(f"xuName '{xuName}' not found in {xuSetBaseDir}")
        return None
    
    if not xuNamePath.is_dir():
        logger.error(f"xuName path is not a directory: {xuNamePath}")
        return None    
   
    return xuNamePath

