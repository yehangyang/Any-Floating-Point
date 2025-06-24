import math
import plotly.express as px
import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FloatRepresentation:

    def __init__(self, sign_bits=1, exponent_bits=8, mantissa_bits=23):
        self.sign_bits = sign_bits
        self.exponent_bits = exponent_bits
        self.mantissa_bits = mantissa_bits
        self.total_bits = sign_bits + exponent_bits + mantissa_bits

        # Validate IEEE constraints
        if exponent_bits < 1:
            raise ValueError("Exponent bits must be at least 1")
        if mantissa_bits < 0:
            raise ValueError("Mantissa bits cannot be negative")

        # Calculate bias for exponent
        self.bias = (1 << (exponent_bits - 1)) - 1

    def _binary_to_float(self, binary_str):
        """Convert binary string to float value"""
        if binary_str == '0' * self.total_bits:
            return 0.0

        # Split into components
        sign_bit = binary_str[0]
        exponent_str = binary_str[1:1 + self.exponent_bits]
        mantissa_str = binary_str[1 + self.exponent_bits:]

        # Handle special cases
        if all(c == '1' for c in exponent_str):
            if all(c == '0' for c in mantissa_str):
                return float('inf') if sign_bit == '0' else float('-inf')
            else:
                return float('nan')

        # Calculate exponent
        exponent = int(exponent_str, 2) - self.bias

        # Calculate mantissa
        if any(c == '1' for c in exponent_str):  # Normalized numbers
            mantissa = 1.0 + sum(int(bit) * (1 / (2**(i + 1))) for i, bit in enumerate(mantissa_str))
        else:  # Denormalized numbers
            mantissa = sum(int(bit) * (1 / (2**(i + 1))) for i, bit in enumerate(mantissa_str))

        # Apply sign
        value = (-1)**int(sign_bit) * mantissa * (2**exponent)
        return value

    def get_range(self):
        """Calculate the value range of the float representation"""
        # Minimum positive value (denormalized)
        min_pos = self._binary_to_float('0' + '0' * self.exponent_bits + '0' * (self.mantissa_bits - 1) + '1')

        # Maximum positive value (normalized)
        max_pos = self._binary_to_float('0' + '1' * (self.exponent_bits - 1) + '0' + '1' * self.mantissa_bits)

        # Minimum negative value
        min_neg = -max_pos

        # Maximum negative value
        max_neg = -min_pos

        return {
            'min_positive': min_pos,
            'max_positive': max_pos,
            'min_negative': min_neg,
            'max_negative': max_neg,
            'zero': 0.0
        }

    def get_values(self):
        """Plot the distribution of values in the float representation"""
        # Generate sample values
        values = []
        total_combinations = 1 << self.total_bits  # 2^total_bits
        for i in range(total_combinations):
            # Convert i to binary string with leading zeros
            binary_str = bin(i)[2:].zfill(self.total_bits)

            try:
                value = self._binary_to_float(binary_str)
                if not math.isnan(value) and not math.isinf(value):
                    values.append(value)
            except:
                pass

        return values


if __name__ == "__main__":
    Path("./output").mkdir(parents=True, exist_ok=True)

    bf16e8m7 = FloatRepresentation(sign_bits=1, exponent_bits=8, mantissa_bits=7)
    fp16e5m10 = FloatRepresentation(sign_bits=1, exponent_bits=5, mantissa_bits=10)
    fp8e4m3 = FloatRepresentation(sign_bits=1, exponent_bits=4, mantissa_bits=3)
    fp8e5m2 = FloatRepresentation(sign_bits=1, exponent_bits=5, mantissa_bits=2)
    fp8e2m1 = FloatRepresentation(sign_bits=1, exponent_bits=2, mantissa_bits=1)

    # Collect values using get_values
    batch_values = {}
    for name, obj in [('bf16e8m7', bf16e8m7), ('fp16e5m10', fp16e5m10), ('fp8e4m3', fp8e4m3), ('fp8e5m2', fp8e5m2),
                      ('fp8e2m1', fp8e2m1)]:
        values = obj.get_values()
        batch_values[f"{name}, {len(values)} valid values"] = values

    # Prepare data for plotting
    df = pd.DataFrame()
    for name, values in batch_values.items():
        temp_df = pd.DataFrame(values, columns=['Value'])
        temp_df['Type'] = name
        df = pd.concat([df, temp_df], ignore_index=True)


    # Create interactive distribution plot with Plotly
    fig = px.histogram(
        df,
        x="Value",
        color="Type",
        nbins=102400,  # Adjust bin count for better visualization
        opacity=0.7,
        barmode="stack",
        log_y=True,
        marginal="box",  # Add box plot for distribution details
        title="Float Value Distribution (Interactive)",
        labels={
            "Value": "Value",
            "Type": "Float Type"
        })

    # Update layout for better visualization
    fig.update_layout(xaxis_title="Value",
                      yaxis_title="Count(log scale)",
                      width=1200,
                      height=800,
                      legend_title="Float Type")

    # Save as interactive HTML file
    fig.write_html("./output/float_distribution_interactive.html")
    fig.show()

    # Save as csv
    df.to_csv("./output/values.csv")