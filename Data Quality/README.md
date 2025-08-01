## Data Quality

This module performs automated quality validation on all `.csv` files in the project’s dataset directories. It ensures that each dataset meets basic quality standards before further processing or analysis.

---

##### Checks Performed

- **Empty File Check**: Skips files that are completely empty.
- **Missing Values**: Detects nulls, NaNs, or empty string fields.
- **Duplicate Rows**: Flags rows that are exact duplicates.
- **Blank Columns**: Identifies columns with only missing/blank values.
- **Whitespace Trimming**: Ensures no extra spaces in string fields.
- **Invalid Encodings**: Ensures data is in UTF-8 and contains valid characters.
- **Column Type Consistency**: Validates if columns have consistent types.

---

##### Output

A report is generated for each file scanned:

- **Location**: Saved as `data_quality_report.html` in the root or script directory.
- **Content Includes**:
  - Total Records Count
  - Number of Records Passed and Failed
  - Summary Table with Row-wise Error Info (if any)
  - ✅ `ALL PASS` indicator if no failures
  - ❌ `X FAILED` indicator if errors are found

---

##### How to Run

```bash
python check_data_quality.py
