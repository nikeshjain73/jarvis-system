import os
import subprocess
import psutil
import winreg

from pathlib import Path


class ApplicationManager:

    # Known/common applications.
    # These are aliases -> executable/path.
    APPLICATIONS = {

        # Windows
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",

        # Chrome
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        # Edge
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "microsoft edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",

        # VS Code
        "vscode": r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
        "vs code": r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",
        "visual studio code": r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe",

        # Android Studio
        "android studio": r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
    }

    # Additional aliases
    ALIASES = {
        "google": "chrome",
        "browser": "chrome",
        "ms edge": "edge",
        "code": "vs code",
        "visual studio": "vs code",
        "android": "android studio",

        # Microsoft Office
        "word": "microsoft word",
        "ms word": "microsoft word",
        "microsoft word": "winword.exe",

        "excel": "microsoft excel",
        "ms excel": "microsoft excel",
        "microsoft excel": "excel.exe",

        "powerpoint": "microsoft powerpoint",
        "ms powerpoint": "microsoft powerpoint",
        "microsoft powerpoint": "powerpnt.exe",

        "outlook": "microsoft outlook",
        "microsoft outlook": "outlook.exe",
    }

    def __init__(self):

        self.applications = {
            name: os.path.expandvars(path)
            for name, path in self.APPLICATIONS.items()
        }

        # Add Windows executable aliases.
        self.applications.update({
            "microsoft word": "winword.exe",
            "microsoft excel": "excel.exe",
            "microsoft powerpoint": "powerpnt.exe",
            "microsoft outlook": "outlook.exe",
        })

        # Discover installed applications.
        self.discovered_applications = {}

    # =========================================================
    # NORMALIZE APPLICATION NAME
    # =========================================================

    def normalize_name(self, name: str):

        name = name.lower().strip()

        # Remove common phrases
        removable = [
            "application",
            "app",
            "program",
        ]

        for word in removable:

            name = name.replace(
                f" {word}",
                ""
            )

        # Resolve aliases
        if name in self.ALIASES:

            name = self.ALIASES[name]

        return name.strip()

    # =========================================================
    # FIND APPLICATION
    # =========================================================

    def find_application(self, name: str):

        name = self.normalize_name(name)

        # -----------------------------------------
        # Known application
        # -----------------------------------------

        if name in self.applications:

            path = self.applications[name]

            if self._is_executable_available(path):

                return path

        # -----------------------------------------
        # Windows PATH
        # -----------------------------------------

        path = self._find_in_path(name)

        if path:

            return path

        # -----------------------------------------
        # Discovered applications
        # -----------------------------------------

        discovered = self.discover_applications()

        for app_name, data in discovered.items():

            if name == app_name:

                executable = data.get(
                    "executable"
                )

                if executable:

                    return executable

        return None

    # =========================================================
    # CHECK EXECUTABLE
    # =========================================================

    def _is_executable_available(self, path: str):

        # Executables available through Windows PATH
        if not os.path.isabs(path):

            return True

        return Path(path).exists()

    # =========================================================
    # SEARCH WINDOWS PATH
    # =========================================================

    def _find_in_path(self, name: str):

        try:

            result = subprocess.run(
                [
                    "where",
                    name
                ],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:

                paths = result.stdout.strip().splitlines()

                if paths:

                    return paths[0]

        except Exception:

            pass

        return None

    # =========================================================
    # OPEN APPLICATION
    # =========================================================

    def open_application(self, name: str):

        name = self.normalize_name(name)

        path = self.find_application(name)

        if not path:

            return {
                "success": False,
                "message": (
                    f"I couldn't find {name} "
                    "on this laptop."
                )
            }

        try:

            subprocess.Popen(
                path,
                shell=False
            )

            return {
                "success": True,
                "message": f"{name} is now open.",
                "application": name,
                "path": path
            }

        except Exception as error:

            return {
                "success": False,
                "message": (
                    f"I couldn't open {name}."
                ),
                "error": str(error)
            }

    # =========================================================
    # CHECK IF APPLICATION IS RUNNING
    # =========================================================

    def is_running(self, name: str):

        name = self.normalize_name(name)

        executable = self.find_application(name)

        if not executable:

            return False

        executable_name = Path(
            executable
        ).name.lower()

        for process in psutil.process_iter(
            ["name"]
        ):

            try:

                process_name = process.info["name"]

                if (
                    process_name
                    and process_name.lower()
                    == executable_name
                ):

                    return True

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                continue

        return False

    # =========================================================
    # CLOSE APPLICATION
    # =========================================================

    def close_application(self, name: str):

        name = self.normalize_name(name)

        executable = self.find_application(name)

        if not executable:

            return {
                "success": False,
                "message": (
                    f"I couldn't find {name}."
                )
            }

        executable_name = Path(
            executable
        ).name.lower()

        closed = False

        for process in psutil.process_iter(
            ["name", "pid"]
        ):

            try:

                process_name = process.info["name"]

                if (
                    process_name
                    and process_name.lower()
                    == executable_name
                ):

                    process.terminate()

                    closed = True

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                continue

        if closed:

            return {
                "success": True,
                "message": (
                    f"{name} has been closed."
                )
            }

        return {
            "success": False,
            "message": (
                f"{name} is not currently running."
            )
        }

    # =========================================================
    # RUNNING APPLICATIONS
    # =========================================================

    def get_running_applications(self):

        applications = []

        for process in psutil.process_iter(
            ["name"]
        ):

            try:

                name = process.info["name"]

                if name:

                    applications.append(name)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                continue

        return sorted(
            set(applications)
        )

    # =========================================================
    # DISCOVER WINDOWS APPLICATIONS
    # =========================================================

    def discover_applications(self):

        discovered = {}

        uninstall_paths = [

            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            ),

            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ),

            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            ),
        ]

        for root, registry_path in uninstall_paths:

            try:

                with winreg.OpenKey(
                    root,
                    registry_path
                ) as key:

                    number_of_entries = (
                        winreg.QueryInfoKey(key)[0]
                    )

                    for i in range(
                        number_of_entries
                    ):

                        try:

                            subkey_name = (
                                winreg.EnumKey(
                                    key,
                                    i
                                )
                            )

                            with winreg.OpenKey(
                                key,
                                subkey_name
                            ) as subkey:

                                # -------------------------
                                # Application name
                                # -------------------------

                                try:

                                    display_name = (
                                        winreg.QueryValueEx(
                                            subkey,
                                            "DisplayName"
                                        )[0]
                                    )

                                except FileNotFoundError:

                                    continue

                                if not display_name:

                                    continue

                                # -------------------------
                                # Install location
                                # -------------------------

                                try:

                                    install_location = (
                                        winreg.QueryValueEx(
                                            subkey,
                                            "InstallLocation"
                                        )[0]
                                    )

                                except FileNotFoundError:

                                    install_location = ""

                                # -------------------------
                                # Executable
                                # -------------------------

                                executable = (
                                    self._find_executable(
                                        subkey
                                    )
                                )

                                discovered[
                                    display_name.lower()
                                ] = {

                                    "name": display_name,

                                    "install_location":
                                        install_location,

                                    "executable":
                                        executable
                                }

                        except (
                            OSError,
                            FileNotFoundError
                        ):

                            continue

            except (
                OSError,
                FileNotFoundError
            ):

                continue

        self.discovered_applications = discovered

        return discovered

    # =========================================================
    # FIND EXECUTABLE FROM REGISTRY
    # =========================================================

    def _find_executable(self, subkey):

        # -----------------------------------------
        # DisplayIcon
        # -----------------------------------------

        try:

            display_icon = (
                winreg.QueryValueEx(
                    subkey,
                    "DisplayIcon"
                )[0]
            )

            if display_icon:

                display_icon = (
                    os.path.expandvars(
                        str(display_icon)
                    )
                )

                if os.path.isfile(display_icon):

                    return display_icon

        except (
            FileNotFoundError,
            OSError
        ):

            pass

        # -----------------------------------------
        # InstallLocation
        # -----------------------------------------

        try:

            install_location = (
                winreg.QueryValueEx(
                    subkey,
                    "InstallLocation"
                )[0]
            )

            if install_location:

                install_location = (
                    os.path.expandvars(
                        str(install_location)
                    )
                )

                if os.path.isdir(
                    install_location
                ):

                    executables = list(
                        Path(
                            install_location
                        ).glob("*.exe")
                    )

                    if executables:

                        return str(
                            executables[0]
                        )

        except (
            FileNotFoundError,
            OSError
        ):

            pass

        return None

    # =========================================================
    # LIST DISCOVERED APPLICATIONS
    # =========================================================

    def list_discovered_applications(self):

        applications = (
            self.discover_applications()
        )

        return sorted(
            [
                data["name"]
                for data in applications.values()
            ]
        )