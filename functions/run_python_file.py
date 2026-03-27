import os, subprocess

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