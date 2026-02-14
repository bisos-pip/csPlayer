from __future__ import annotations

from bisos.csPlayer import drf_csPlayer_abstract as drf

from bisos.csPlayer import drf_csPlayer_abstract as drf
from bisos.csPlayer import drf_csPlayer_common
import pathlib

operationsData = {}

def thisExecutablesFolderName() -> str:
    return """modules:facter"""

drf_csPlayer_common.executablesInfo_load(executablesFolderName=thisExecutablesFolderName())

class LibraryAPIImpl(drf.LibraryAPI):
    libraryFolder = drf.OperationFolder(name=thisExecutablesFolderName())  # Must Match Registration
    libraryFolder = drf_csPlayer_common.csxuFolderObtain(libraryFolder)

    def getOperationHierarchy(self) -> drf.OperationFolder:
        return self.libraryFolder
    
    def getDescription(self, operationBranch: list[str]) -> str:
        operationName = "_".join(operationBranch)
        operationData = operationsData[operationName]
        if operationData is None:
            return None
        return operationData['description']
            
    def getParameters(self, operationBranch: list[str]) -> drf.ParameterData:
        operationName = "_".join(operationBranch)
        operationData = operationsData[operationName]
        if operationData is None:
            return None
        return operationData['parameters']
