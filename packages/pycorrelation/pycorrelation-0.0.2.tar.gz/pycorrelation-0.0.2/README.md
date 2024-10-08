
# PyCorrelation

**PyCorrelation** is a Python package designed to handle symmetric and correlation matrices efficiently. It builds upon the concept of symmetric matrices to provide a class dedicated to correlation operations, ensuring values fall within the valid range $(-1,1)$, and automatically maintaining correlations of 1 on the diagonal.

## Features

- A class ensuring symmetry in a matrix: $x_{i,j} = x_{j,i}$
- A class for managing correlation matrices with strict validation of correlation values.
- Methods to set, retrieve, and validate correlation pairs using user-friendly indexers.

## Installation

To install PyCorrelation, you can clone the repository and use pip:

```bash
git clone https://github.com/SRKX/PyCorrelation.git
cd PyCorrelation
pip install .
```

## Usage

Below is an example of how to use the package:

```python
from PyCorrelation import CorrelationMatrix

# Initialize a CorrelationMatrix
correl_matrix = CorrelationMatrix(keys=['A', 'B', 'C'], frozen_keys=True)

# Set correlations
correl_matrix[('A', 'B')] = 0.5
correl_matrix[('B', 'C')] = -0.2

# Access correlation values
print(correl_matrix[('B', 'A')])  # Outputs: 0.5

# Check if a key pair is in the matrix
print(('A', 'B') in correl_matrix)  # Outputs: True
```

## Classes and Methods

### `SymmetricMatrix`

This is the base class for symmetric matrices. It allows you to define and manipulate a matrix where elements are mirrored across the diagonal.

#### Public Methods

- **`keys()`**: Returns the keys of the matrix.
- **`to_2d_dict(selected_keys=None)`**: Converts the matrix into a 2D dictionary, extracting only the selected keys (or all if not specified).
- **`to_2d_array(ordered_keys)`**: Converts the matrix into a 2D array representation, returning a list of lists where the indices follow the ordered of the input parameter.

### `CorrelationMatrix`

This class extends `SymmetricMatrix` and is specialized for correlation matrices. It includes additional validation to ensure values are always in $(-1,1)$, and that identical keys always have a correlation of 1.

## License

This project is licensed under the MIT License.
