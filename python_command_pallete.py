# import subprocess

# # Open the VS Code Command Palette with "Ask Copilot" focused
# #subprocess.run(["code", "--command", "workbench.action.quickCommand", "--args", "Ask Copilot"])
# file_path = 'D:/gowrishankar.p/Python Script/'
# subprocess.run(["code",file_path], check=True)

# #subprocess.run


# #Write a python code to control vscode via script to open a file

import subprocess

# Replace 'your_command' with the command you want to run
#command = 'code'
command = 'code --command "workbench.action.quickCommand" --args "Ask Copilot"'

# Run the command and capture the output
#result = subprocess.run(command, shell=True, capture_output=True, text=True)
result = subprocess.run(command,shell=True)

# The stdout attribute contains the output of the command
print(result.stdout)