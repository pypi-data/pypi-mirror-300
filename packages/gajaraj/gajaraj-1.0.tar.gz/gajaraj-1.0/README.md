# Gajaraj

Gajaraj is a Pandas alternative library in Python. It aims to provide similar functionalities as Pandas, enabling users to perform data manipulation and analysis seamlessly. The library is designed to be intuitive and user-friendly, making data handling straightforward for both beginners and experienced users.

## Features

- **DataFrame Creation**: Easily create DataFrames from various data sources.
- **I/O Operations**: Read and write data in formats like CSV and JSON.
- **Data Manipulation**: Filter, select, and aggregate data efficiently.
- **Compatibility**: Designed to work seamlessly alongside Pandas.

## Installation

You can install Gajaraj using pip:

```bash
pip install gajaraj
```

## Usage

Here's a quick example of how to use Gajaraj:

```python
import gajaraj as gj

# Read a CSV file
df = gj.read_csv("your_file.csv")

# Display the first few rows
print(df.head())

# Select specific columns
selected = df.select("Column1", "Column2")
print(selected)
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to contribute to the library, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Akshat Shukla - [GitHub](https://github.com/binarybardakshat)