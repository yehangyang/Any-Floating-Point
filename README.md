# Float Representation Analyzer

## Overview

This project provides a Python implementation to analyze and visualize the range and distribution of floating-point numbers based on custom bit configurations. It simulates IEEE 754-like floating-point representations and generates interactive visualizations using Plotly.

## Features

- Customizable float representation (sign, exponent, mantissa bits)
- Range calculation for positive/negative values
- Value distribution analysis
- Interactive histogram visualization
- Support for multiple float formats (e.g., fp16e5m10, fp8e4m3)

## Usage

### Installation

1. Ensure Python 3.x is installed
2. Install dependencies:

```bash
uv install
```

### Running the Analysis

```bash
python main.py
```

### Output

- Interactive histogram saved at `output/float_distribution_interactive.html`
- Visualizes value distributions for:
  - fp16e5m10 (16-bit, 5 exponent, 10 mantissa)
  - fp8e4m3 (8-bit, 4 exponent, 3 mantissa)
  - fp8e5m2 (8-bit, 5 exponent, 2 mantissa)
  - fp4e2m1 (4-bit, 2 exponent, 1 mantissa)

## Key Classes/Methods

### FloatRepresentation

- `__init__(sign_bits, exponent_bits, mantissa_bits)`: Configure float format
- `_binary_to_float(binary_str)`: Convert binary string to float value
- `get_range()`: Calculate value range boundaries
- `get_values()`: Generate sample values for visualization

## Configuration

Modify the float format parameters in the main section:

```python
fp16e5m10 = FloatRepresentation(sign_bits=1, exponent_bits=5, mantissa_bits=10)
fp8e4m3 = FloatRepresentation(sign_bits=1, exponent_bits=4, mantissa_bits=3)
```

## License

MIT License

Copyright (c) 2025 AnyFloatingPoint

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
