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
    enabledBaseDir = auditTrail_csu.xuSetTreeNameToXuSetBaseDir(executablesFolderName)

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

