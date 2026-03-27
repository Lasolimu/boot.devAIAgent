import os

def write_file(working_directory, file_path, content):
    try:
        absDirPath = os.path.abspath(working_directory)
        targetFile = os.path.normpath(os.path.join(absDirPath, file_path))
        validTargetFile = os.path.commonpath([absDirPath, targetFile]) == absDirPath

        if not validTargetFile:
            return f'Error: Cannot write to "{targetFile}" as it is outside the permitted working directory'
        if os.path.isdir(targetFile):
            return f'Error: Cannot write to "{targetFile}" as it is a directory'
        
        os.makedirs(absDirPath, exist_ok=True)
        
        with open(targetFile, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"