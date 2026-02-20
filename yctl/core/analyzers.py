def load_data(file_path):
    import pandas as pd
    import csv
    from pathlib import Path

    # Ensuring file exists
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Try loading using comma as the first delimiter
    try:
        data = pd.read_csv(file_path, delimiter=',')
        return data
    except pd.errors.ParserError:
        print("Comma delimiter failed, trying automatic delimiter detection.")

    # Attempt automatic delimiter detection
    with open(file_path, 'r') as f:
        # Read first few lines to infer delimiter
        sample_lines = [next(f) for _ in range(5)]

        # Try different common delimiters
        delimiters = [',', ';', '\t']
        for delimiter in delimiters:
            try:
                f.seek(0)  # Reset file pointer
                data = pd.read_csv(f, delimiter=delimiter)
                return data
            except pd.errors.ParserError:
                continue

    raise ValueError("Failed to load data. No suitable delimiter found." )
