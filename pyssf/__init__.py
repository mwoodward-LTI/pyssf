import json
import subprocess
from datetime import datetime


class SSFFormatter:
    def __init__(self, deno_script_path: str):
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
        options = {
            "date1904": date1904,
        }
        if date_nf is not None:
            options["dateNF"] = date_nf
        if table is not None:
            options["table"] = table

        options_json = json.dumps(options) if options else ""
        value_str = "" if value is None else str(value)

        cmd = [
            "deno", "run",
            self.deno_script_path,
            fmt,
            value_str,
        ]
        if options_json:
            cmd.append(options_json)

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.rstrip("\n")
        except subprocess.CalledProcessError as e:
            print("Error calling Deno script:", e.stderr)
            return None
