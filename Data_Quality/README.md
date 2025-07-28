\# Job Data Quality Checker



Validates Canadian job postings for data quality.



\## Requirements

\- Python 3.7+

\- pandas

\- python-dateutil



\## Usage

1\. Save your job data as `job\_data.json`

2\. Run:

&nbsp;  ```bash

&nbsp;  python run\_quality\_checks.py





Checks Performed

1. Completeness (all required fields present)

&nbsp;	Job title

&nbsp;	Company

&nbsp;	Location

&nbsp;	Date

&nbsp;	Salary



2\. Location Validity

* Must be Canadian province or "Various locations"
* Example valid formats:

&nbsp;	Toronto, ON

&nbsp;	Vancouver (BC)

&nbsp;	Various locations





Output

&nbsp;	Console report showing:

&nbsp;		Passed checks (✅)

&nbsp;		Failed checks (❌) with sample invalid records

&nbsp;	JSON report (optional)





Customize

Edit check\_canadian\_locations() to:

* Add valid location formats
* Change validation rules



Example Failed Record

&nbsp;	❌ FAIL: canadian\_locations

&nbsp;	Invalid Count: 5

&nbsp;	Sample Issues:

&nbsp;	- ID: 123 | Location: New York, NY | Job: Developer







