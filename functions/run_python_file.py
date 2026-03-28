import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        absDirPath = os.path.abspath(working_directory)
        targetFile = os.path.normpath(os.path.join(absDirPath, file_path))
        validTargetFile = os.path.commonpath([absDirPath, targetFile]) == absDirPath

        if not validTargetFile:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(targetFile):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", targetFile]
        if args != None:
            command.extend(args)

        completed = subprocess.run(command, cwd=absDirPath, capture_output=True, text=True, timeout=30)

        outputString = ""
        if len(completed.stdout) != 0:
            outputString = f"STDOUT: {outputString}{completed.stdout}\n"
        if len(completed.stderr) != 0:
            outputString = f"STDERR: {outputString}\n{completed.stderr}\n"
        if len(outputString) == 0:
            outputString = "No output produced"
            
        if completed.returncode != 0:
            outputString += f"Process exited with code {completed.returncode}\n{outputString}"
        
        return outputString
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python scripts in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the script to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The list of arguments to pass into the Python script",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="An arguement passed into the python script"
                )
            ),
        },
    ),
)