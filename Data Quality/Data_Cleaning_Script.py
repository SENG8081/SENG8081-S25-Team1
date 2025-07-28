import io
import os
import zipfile

import pandas as pd


def clean_csv(file_path, output_path=None, zip_csv_name=None, compress=False,
              dropna=False, fillna_method="mean", skip_head=0, skip_tail=0, encoding="utf-8-sig"):
    # Decide base name: use zip_csv_name if reading from zip, otherwise file_path
    if file_path.endswith(".zip"):
        if not zip_csv_name:
            raise ValueError("You must provide `zip_csv_name` when reading from a .zip file.")
        base_name = os.path.basename(zip_csv_name)
    else:
        base_name = os.path.basename(file_path)

    # Force output .csv filename from base_name
    csv_filename = os.path.splitext(base_name)[0] + ".csv"

    # If output_path not given, create it in ./CLEANED_DATA/
    if output_path is None:
        output_dir = os.path.join(".", "CLEANED_DATA")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "CLEANED_" + csv_filename)

    # Read file content: from zip or normal file
    if file_path.endswith(".zip"):
        with zipfile.ZipFile(file_path) as z:
            with z.open(zip_csv_name) as f:
                lines = f.read().decode(encoding).splitlines()
    else:
        with open(file_path, encoding=encoding) as f:
            lines = f.readlines()

    # Trim head and tail lines
    data_lines = lines[skip_head:len(lines) - skip_tail if skip_tail > 0 else None]
    cleaned_text = "\n".join(data_lines)

    # Load into DataFrame
    df = pd.read_csv(io.StringIO(cleaned_text))
    print(f"Original data shape: {df.shape}")

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Drop duplicates
    df = df.drop_duplicates()
    print(f"Shape after removing duplicates: {df.shape}")

    # Strip whitespace in string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Handle missing values
    if dropna:
        df = df.dropna()
        print("Dropped all rows with missing values")
    else:
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if fillna_method == "mean" and pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                elif fillna_method == "median" and pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna("unknown")
        print("Missing values filled")

    # Convert column types
    df = df.convert_dtypes()

    # Save CSV
    df.to_csv(output_path, index=False)
    abs_csv_path = os.path.abspath(output_path)
    print(f"Cleaned data saved to: {abs_csv_path}")

    # Optionally compress and delete intermediate CSV
    if compress:
        zip_path = output_path.replace(".csv", ".zip")
        abs_zip_path = os.path.abspath(zip_path)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(abs_csv_path, arcname=os.path.basename(abs_csv_path))

        os.remove(abs_csv_path)
        print(f"Compressed ZIP saved to: {abs_zip_path}")
        print(f"Deleted intermediate CSV: {abs_csv_path}")
        return abs_zip_path

    return abs_csv_path


if __name__ == '__main__':
    clean_csv("1410028701-canada_stat.csv")
    clean_csv("linkedin_canada.csv")
    clean_csv("36100676-eng.zip", zip_csv_name="36100676.csv", compress=True)
    pass
