import os
from google.genai import types

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
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be writted to the file"
            )
        },
    ),
)