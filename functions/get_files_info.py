import os

def get_files_info(working_directory, directory="."):
    try:
        absDirPath = os.path.abspath(working_directory)
        targetDir = os.path.normpath(os.path.join(absDirPath, directory))
        validTargetdir = os.path.commonpath([absDirPath, targetDir]) == absDirPath

        if not validTargetdir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(absDirPath):
            return f'Error: "{directory}" is not a directory'
        
        fileInfo = []
        for point in os.listdir(targetDir):
            fileInfo.append(f"  - {point}: file_size={os.path.getsize(os.path.join(targetDir, point))} bytes, is_dir={os.path.isdir(os.path.join(targetDir, point))}")
        return "\n".join(fileInfo)
    except Exception as e:
        return f"Error: {e}"