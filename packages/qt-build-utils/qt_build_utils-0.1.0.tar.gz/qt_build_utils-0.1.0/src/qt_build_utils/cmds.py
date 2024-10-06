import distutils.spawn
import subprocess


def pyside_uic_run(command: str):
    EXECUTABLE = ["pyside6-uic", "pyside2-uic"]

    # Try to find the pyside-uic executable
    for executable_name in EXECUTABLE:
        executable = distutils.spawn.find_executable(executable_name)
        if executable:
            subprocess.run(f"{executable_name} {command}", shell=True)
            return

    raise SystemError("pyside-uic executable not found")


def pyside_designer_run(command: str):
    EXECUTABLE = ["pyside6-designer", "pyside2-designer"]

    # Try to find the pyside-uic executable
    for executable_name in EXECUTABLE:
        executable = distutils.spawn.find_executable(executable_name)
        if executable:
            subprocess.run(f"{executable_name} {command}", shell=True)
            return

    raise SystemError("pyside-designer executable not found")
