import os
from config import (MAX_CHARS)

def get_file_content(working_directory, file_path):
    try:
        absDirPath = os.path.abspath(working_directory)
        targetFile = os.path.normpath(os.path.join(absDirPath, file_path))
        validTargetFile = os.path.commonpath([absDirPath, targetFile]) == absDirPath

        if not validTargetFile:
            return f'Error: Cannot read "{targetFile}" as it is outside the permitted working directory'
        if not os.path.isfile(targetFile):
            return f'Error: File not found or is not a regular file: "{targetFile}"'
        
        fileContents= ""
        with open(targetFile, "r") as f:
            fileContents = f.read(MAX_CHARS)
            if f.read(1):
                fileContents += f'[...File "{targetFile}" truncated at {MAX_CHARS} characters]'
        return fileContents
        
    except Exception as e:
        return f"Error: {e}"