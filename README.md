# pyssf

`pyssf` is a Python library for working with SSF (Standard Spreadsheet Format) numbers, providing robust formatting and parsing capabilities.

## Features

-   **Number Formatting:** Format numbers according to SSF specifications.

## Installation
### Using uv (Recommended)

clone the repo, then run `uv sync`

## Usage

```python
from pyssf import format_number

# Example: Formatting a number
formatted_value = format_number(1234.56, '#,##0.00')
print(f"Formatted: {formatted_value}") # Output: Formatted: 1,234.56
```

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Third-Party Components

This project utilizes `ssf.js`, which is also licensed under the Apache License, Version 2.0. A modification has been made to the original `ssf.js` file (`vendor/main.ts`) to export its functionality using ES module format to facilitate integration with this project.
