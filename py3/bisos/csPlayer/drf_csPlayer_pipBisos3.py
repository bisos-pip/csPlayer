from __future__ import annotations

from bisos.csPlayer import drf_csPlayer_abstract as drf
from bisos.csPlayer import drf_csPlayer_common
import pathlib

operationsData = {}

facterDescription = '''
# facterBx.cs

A **CS-Lib** for creating and managing BPO's gpg and encryption/decryption.
'''

facterOptions = drf.ParameterOptionsToList(name='-i', description='List of commands for facter')

paramList = drf.ParameterList(name='cmdbSummary');
paramList.parameters.append(drf.ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = drf.ParameterList(name='csxuFpsToGraphviz');
paramList.parameters.append(drf.ParameterStringValue(name='--csxuFpsBasePath', description='Path to fps'))
paramList.parameters.append(drf.ParameterStringValue(name='--csxuName', description='Name of csxu'))
paramList.parameters.append(drf.ParameterStringValue(name='--pyDictResultPath', description='Path to dict result file'))
paramList.parameters.append(drf.ParameterStringValue(name='--graphvizResultPath', description='Path to graphviz result file'))
facterOptions.options.append(paramList)

paramList = drf.ParameterList(name='csxuFpsToPyDict');
paramList.parameters.append(drf.ParameterStringValue(name='--csxuFpsBasePath', description='Path to fps'))
paramList.parameters.append(drf.ParameterStringValue(name='--csxuName', description='Name of csxu'))
paramList.parameters.append(drf.ParameterStringValue(name='--pyDictResultPath', description='Path to dict result file'))
facterOptions.options.append(paramList)

facterOptions.options.append(drf.ParameterList(name='csxuInSchema'))

facterOptions.options.append(drf.ParameterList(name='examples_csu'))

paramList = drf.ParameterList(name='factName');
paramList.parameters.append(drf.ParameterPreference(name='--cache', description='Apply cache'))
paramList.parameters.append(drf.ParameterStringValue(name='--fromFile', description='Path to the fromFile'))
paramList.parameters.append(drf.ParameterStringValue(name='--perfName', description='Name of the Perf'))
paramList.parameters.append(drf.ParameterStringValue(name='', mandatory=True, description='factName component'))
facterOptions.options.append(paramList)

paramList = drf.ParameterList(name='factNameGetattr');
paramList.parameters.append(drf.ParameterPreference(name='--cache', description='Apply cache'))
paramList.parameters.append(drf.ParameterStringValue(name='--fromFile', description='Path to the fromFile'))
paramList.parameters.append(drf.ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

facterOptions.options.append(drf.ParameterList(name='facterJsonOutputBytes'))

paramList = drf.ParameterList(name='facterJsonOutputBytesToFile');
paramList.parameters.append(drf.ParameterStringValue(name='--fromFile', mandatory=True, description='Path to the fromFile'))
paramList.parameters.append(drf.ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = drf.ParameterList(name='roCmnd_examples');
paramList.parameters.append(drf.ParameterStringValue(name='--sectionTitle', mandatory=True, description='Title for this section'))
paramList.parameters.append(drf.ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = drf.ParameterList(name='roInv_examples_csu');
paramList.parameters.append(drf.ParameterStringValue(name='--sectionTitle', mandatory=True, description='Title for this section'))
paramList.parameters.append(drf.ParameterStringValue(name='--perfName', description='Name of the Perf'))
facterOptions.options.append(paramList)

paramList = drf.ParameterList(name='roPerf_examples_csu');
paramList.parameters.append(drf.ParameterStringValue(name='--sectionTitle', mandatory=True, description='Title for this section'))
facterOptions.options.append(paramList)

operationsData['facterBx.cs'] = {'description': facterDescription, 'parameters': facterOptions}

class LibraryAPIImpl(drf.LibraryAPI):
    libraryFolder = drf.OperationFolder(name="pip:bisos3")  # Must Match Registration
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

    def submitOperation(self, operationBranch: list[str], command: list[str], servers: list[str]) -> dict:
        """Execute the operation with the given command and servers."""
        return drf_csPlayer_common.csxuLineExecute(operationBranch, command, servers)
