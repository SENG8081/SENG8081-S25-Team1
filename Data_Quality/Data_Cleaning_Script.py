import io
import os
import zipfile
import pandas as pd


def clean_csv(filename, output_path=None, zip_csv_name=None, compress=False,
              dropna=False, fillna_method="mean", skip_head=0, skip_tail=0, encoding="latin-1"):
    data_folder = os.path.join("..", "Data_Collection")
    file_path = os.path.join(data_folder, filename)

    # Determine base name for output
    base_name = zip_csv_name if zip_csv_name else os.path.basename(file_path)
    csv_filename = os.path.splitext(base_name)[0] + ".csv"

    # Generate output folder and path
    if output_path is None:
        output_dir = os.path.join(".", "CLEANED_DATA")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "CLEANED_" + csv_filename)

    # Load raw lines from CSV or ZIP
    if file_path.endswith(".zip"):
        if not zip_csv_name:
            raise ValueError("You must provide `zip_csv_name` for ZIP files.")
        with zipfile.ZipFile(file_path) as z:
            with z.open(zip_csv_name) as f:
                lines = f.read().decode(encoding).splitlines()
    else:
        with open(file_path, encoding=encoding) as f:
            lines = f.readlines()

    # Trim head/tail rows
    data_lines = lines[skip_head:len(lines) - skip_tail if skip_tail > 0 else None]
    cleaned_text = "\n".join(data_lines)

    # Load to DataFrame
    df = pd.read_csv(io.StringIO(cleaned_text))
    print(f"Original shape: {df.shape}")

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Remove rows/columns with ALL missing values
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # Remove columns with all empty strings or whitespace
    for col in df.columns:
        if df[col].dtype == object and all(df[col].astype(str).str.strip() == ""):
            df.drop(columns=[col], inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Strip string column whitespace
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

    # Handle missing values
    if dropna:
        df.dropna(inplace=True)
        print("Dropped rows with missing values")
    else:
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if fillna_method == "mean" and pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].mean(), inplace=True)
                elif fillna_method == "median" and pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    df[col].fillna("Unknown", inplace=True)
        print("Filled missing values")

    # Special cleaning
    if not filename.startswith("StatCan_"):
        existing_cols_to_remove = ['nom_de_la_profession']
        if existing_cols_to_remove:
            df.drop(columns=existing_cols_to_remove, inplace=True)
            print(f"Removed from {filename}: {existing_cols_to_remove}")
        else:
            print(f"No matching columns to remove from {filename}")

        if filename.startswith("labour_market_conditions_"):
            df.drop(df.columns[-1], axis=1, inplace=True)
            print(f"Removed from {filename}: conditions_rÃ©centes_sur_le_marchÃ©_du_travail")

    # Convert column types
    df = df.convert_dtypes()

    # Save cleaned file
    df.to_csv(output_path, index=False)
    print(f"Cleaned file saved to: {os.path.abspath(output_path)}")

    # Optional compression
    if compress:
        zip_path = output_path.replace(".csv", ".zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(output_path, arcname=os.path.basename(output_path))
        os.remove(output_path)
        print(f"Compressed and saved to: {os.path.abspath(zip_path)}")
        return os.path.abspath(zip_path)

    return os.path.abspath(output_path)


def main():
    # Adjust the path as required
    data_folder = os.path.join("..", "Data_Collection")
    files = os.listdir(data_folder)

    for f in files:
        full_path = os.path.join(data_folder, f)
        # Skip non-CSV and non-ZIP files
        if f.endswith(".csv"):
            print(f"\nCleaning {f}...")
            clean_csv(f)
        elif f.endswith(".zip"):
            # If there's only one .csv inside, we can infer its name
            with zipfile.ZipFile(full_path) as z:
                inner_csvs = [name for name in z.namelist() if name.endswith(".csv")]
                if len(inner_csvs) == 1:
                    print(f"\n Cleaning {f} [ZIP]...")
                    clean_csv(f, zip_csv_name=inner_csvs[0])
                else:
                    print(f"Skipped {f}: Contains multiple CSVs or none.")


# Run cleaning
if __name__ == "__main__":
    main()
