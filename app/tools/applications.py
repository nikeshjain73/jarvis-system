import subprocess


APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
}


def open_application(application: str) -> str:

    application = application.lower().strip()

    if application not in APPLICATIONS:
        return f"I don't know how to open {application} yet."

    try:
        subprocess.Popen(
            APPLICATIONS[application],
            shell=True
        )

        return f"{application} is now open."

    except Exception as e:
        return f"I couldn't open {application}: {str(e)}"