import json
import platform
import subprocess
from datetime import datetime
from pathlib import PurePath

SYSTEM = platform.system()


class SSFFormatter:
    def __init__(self, deno_script_path: str | None = None):
        """
        Initialize the SSFFormatter with an optional Deno script path.

        :param deno_script_path: Relative Path to the Deno script for formatting (default None)
        """
        self.deno_script_path = deno_script_path

    def format(
        self,
        fmt: str,
        value: str | int | float | bool | datetime | None,
        date1904: bool = False,
        date_nf: str | None = None,
        table: dict[int, str] | None = None,
    ) -> str | None:
        """
        Format value according to format string and SSF options.

        :param fmt: Format string (e.g., "0.00%", "m/d/yy")
        :param value: Value to format (number, string, boolean, date)
        :param date1904: Use 1904 date system (default False)
        :param dateNF: Custom date number format (default None)
        :param table: Custom format table as dict (default None)
        :return: Formatted string or None if error
        """
        # Initialize options dictionary for SSF formatting
        options = {
            "date1904": date1904,
        }
        if date_nf is not None:
            options["dateNF"] = date_nf
        if table is not None:
            options["table"] = table

        # Serialize options to JSON if they exist
        options_json = json.dumps(options) if options else ""
        # Convert value to string for subprocess call
        value_str = "" if value is None else str(value)

        # Determine the executable call based on the platform or provided Deno script
        if self.deno_script_path:
            exe_call = [
                "deno",
                "run",
                "--unstable-detect-cjs",
                PurePath(__file__).parent.parent / self.deno_script_path,
            ]
        elif SYSTEM == "Darwin":
            exe_call = [
                PurePath(__file__).parent.parent
                / "vendor/ssf_aarm"  # macOS ARM executable
            ]
        elif SYSTEM == "Windows":
            exe_call = [
                PurePath(__file__).parent.parent
                / "vendor/ssf_win.exe"  # Windows executabl
            ]
        else:
            raise ValueError("Unsupported platform")

        # Construct the full command to be executed
        cmd = [*exe_call, fmt, value_str]

        if options_json:
            cmd.append(options_json)
        try:
            # Run the external command
            result = subprocess.run(
                cmd,
                check=True,  # Raise an exception for non-zero exit codes
                capture_output=True,  # Capture stdout and stderr
                text=True,  # Decode stdout/stderr as text
            )
            return result.stdout.rstrip("\n")
        except subprocess.CalledProcessError as e:
            print("Error calling Deno script:", e.stderr)
            return None
