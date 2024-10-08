from enum import Enum
import os, sys, json
class ReturnValues(Enum):
    """
    Enum representing possible return values from functions.
    """
    SUCCESS = 0
    ERROR = 1
    CRED_CREATE_SUCCESS = 2
    CRED_CREATE_ERROR = 3
    CRED_FOUND = 4 
    CRED_NOT_FOUND = 5
    ENGINE_FOUND = 6
    ENGINE_NOT_FOUND = 7
    ENGINE_CREATE_SUCCESS = 8
    ENGINE_CREATE_ERROR = 9
    ENGINE_REMOVE_SUCCESS = 10
    ENGINE_REMOVE_ERROR = 11
    ENGINE_DEPLOY_SUCCESS = 12
    ENGINE_DEPLOY_ERROR = 13

    # UPT Repo Engine status
    UPT_ENGINE_CREATE_SUCCESS = 14
    UPT_ENGINE_CREATE_ERROR = 15
    UPT_ENGINE_UPDATE_SUCCESS = 16
    UPT_ENGINE_UPDATE_ERROR = 17
    UPT_ENGINE_DELETE_SUCCESS = 18
    UPT_ENGINE_DELETE_ERROR = 19

    # File Operation Ret
    DIR_FILE_OP_SUCCESS = 100
    DIR_FILE_OP_ERROR = 101
    

class DirFileHandlers:
    def __init__(self):
        pass

    def getFileContent(self, absFilePath: str, readMode: str = "r"):

        if not os.path.exists(absFilePath):
            print (f"Requested file {absFilePath} does not exist!!")
            return None
        
        content : str | None = None
        try:
            with open(absFilePath, readMode) as readFile:
                content = readFile.read()
            return content
        except Exception as e:
            print (f"Exception Occured while fetching file content: {e}")
            return None
        
    def writeFileContent(self, absFilePath: str, writeContent: str, writeMode: str = "w"):
        
        try:
            with open(absFilePath, writeMode) as writeFile:
                writeFile.write(writeContent)
        except Exception as e:
            print (f"Exception Occured while writing the file content: {e}")
            return None