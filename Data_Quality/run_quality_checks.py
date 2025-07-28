"""
run_quality_checks.py - Consolidated Canadian Job Market Data_Quality Checker

Usage:
    python run_quality_checks.py [--json-path PATH] [--output FILE]

Features:
- Loads job data from specified JSON file
- Performs comprehensive data quality checks
- Outputs console report and optional JSON report
"""

import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import re
from dateutil.parser import parse

# Constants
DEFAULT_JSON_PATH = Path("C:/My Courses/Big Data/Semester2/Case Studies/Group Project/job_trends.jobbank.json")
ALTERNATE_PATHS = [Path("./data/jobs.json"), Path("../jobs.json")]

# Configuration
QUALITY_THRESHOLDS = {
    'completeness': {
        'critical': 20.0,  # >20% missing = CRITICAL
        'warning': 5.0     # >5% missing = WARNING
    },
    'salary': {
        'min_hourly': 14,    # Minimum wage in Canada
        'max_hourly': 250,
        'min_annual': 20000,
        'max_annual': 500000
    }
}

class JobDataQualityChecker:
    def __init__(self, job_data: List[Dict[str, Any]]):
        """Initialize with job data in the specified JSON format"""
        self._setup_logging()
        self.data = job_data
        self.df = self._convert_to_dataframe()
        self.results = {'summary': {}, 'details': {}}
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging"""
        self.logger = logging.getLogger('JobDataQuality')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _convert_to_dataframe(self) -> pd.DataFrame:
        """Convert JSON data to DataFrame with standardized columns"""
        try:
            df = pd.json_normalize(self.data)
            column_map = {'business': 'company', 'noctitle': 'job_title', 'date': 'posted_date'}
            df = df.rename(columns=column_map)
            
            if 'posted_date' in df.columns:
                df['posted_date'] = df['posted_date'].apply(self._parse_date)
            
            self.logger.info(f"Loaded {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Data conversion failed: {str(e)}")
            raise

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats into datetime objects"""
        try:
            return parse(date_str) if pd.notna(date_str) else None
        except (ValueError, TypeError):
            self.logger.warning(f"Couldn't parse date: {date_str}")
            return None

    def check_completeness(self) -> Dict[str, Any]:
        """Check for missing values in critical fields"""
        critical_fields = ['job_title', 'company', 'location', 'posted_date', 'salary']
        results = {}
        
        for field in critical_fields:
            missing = self.df[field].isna().sum() if field in self.df.columns else len(self.df)
            pct_missing = (missing / len(self.df)) * 100
            
            status = "OK"
            if pct_missing > QUALITY_THRESHOLDS['completeness']['critical']:
                status = "CRITICAL"
            elif pct_missing > QUALITY_THRESHOLDS['completeness']['warning']:
                status = "WARNING"
                
            results[field] = {
                'missing': int(missing),
                'pct_missing': round(pct_missing, 2),
                'status': status
            }
        
        self.results['completeness'] = results
        return results

    def check_canadian_locations(self) -> Dict[str, Any]:
        """Strict validation that accepts 'Various locations' as valid"""
        result = {
            'invalid_count': 0,
            'pct_invalid': 0.0,
            'status': 'OK',
            'sample_failures': [],
            'requirement': '100% Canadian locations or "Various locations"'
        }

        if 'location' not in self.df.columns:
            return {
                'canadian_locations': {
                    'status': 'CRITICAL',
                    'error': 'location field missing',
                    'requirement': '100% Canadian locations or "Various locations"'
                }
            }

        # Canadian province patterns
        canadian_provinces = ['AB','BC','MB','NB','NL','NT','NS','NU','ON','PE','QC','SK','YT']
        province_patterns = []
    
        for province in canadian_provinces:
            province_patterns.extend([
                rf'\({province}\)',
                rf'{province}[ ,]',
                rf' {province}$'
            ])
    
        province_patterns.extend([
            'Canada', 'CAN', 'CA\-', r'\bCA\b',
            'Alberta', 'British Columbia', 'Manitoba',
            'New Brunswick', 'Newfoundland', 'Northwest Territories',
            'Nova Scotia', 'Nunavut', 'Ontario',
            'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'
        ])
    
        pattern = '|'.join(province_patterns)

        # Check each location
        invalid_mask = ~(
            self.df['location'].str.contains(pattern, case=False, na=False) |
            self.df['location'].eq('Various locations') |
            self.df['location'].isna()
        )
    
        invalid_count = invalid_mask.sum()
        pct_invalid = (invalid_count / len(self.df)) * 100

        result.update({
            'invalid_count': invalid_count,
            'pct_invalid': round(pct_invalid, 4),
            'status': 'FAIL' if invalid_count > 0 else 'OK'
        })

        # Get sample failures
        if invalid_count > 0:
            failures = self.df[invalid_mask]
            result['sample_failures'] = [
                f"ID: {row['id']} | Location: {row['location']} | Job: {row['job_title']}"
                for _, row in failures.head(10).iterrows()
            ]

        return {'canadian_locations': result}

    def run_all_checks(self) -> bool:
        """Execute all quality checks"""
        try:
            # Reset results
            self.results = {'summary': {}, 'details': {}}
        
            # Run checks
            self.results['completeness'] = self.check_completeness()
            self.results['location_validity'] = self.check_canadian_locations()  # Ensure this is included
            self._generate_summary()
            return True
        except Exception as e:
            self.logger.error(f"Quality checks failed: {str(e)}", exc_info=True)
            return False

    def _generate_summary(self):
        """Generate summary statistics that match our checks"""
        checks = 0
        passed = 0
    
        # Define expected check categories
        expected_checks = {
            'completeness': ['job_title', 'company', 'location', 'posted_date', 'salary'],
            'location_validity': ['canadian_locations']
        }
    
        # Count checks
        for category, check_names in expected_checks.items():
            if category in self.results:
                for check_name in check_names:
                    checks += 1
                    result = self.results[category].get(check_name, {})
                    if isinstance(result, dict) and result.get('status') == 'OK':
                        passed += 1
    
        self.results['summary'] = {
            'total_records': len(self.df),
            'checks_performed': checks,
            'passed_checks': passed,
            'warning_checks': checks - passed,
            'timestamp': datetime.now().isoformat()
        }

    def print_report(self):
        """Print report with enhanced location failure details"""
        print("\n" + "="*60)
        print("DETAILED JOB DATA QUALITY REPORT".center(60))
        print("="*60)
    
        summary = self.results.get('summary', {})
        print(f"\nSUMMARY: {summary.get('passed_checks', 0)}/{summary.get('checks_performed', 0)} checks passed")
        print("-"*60)
    
        for category, checks in self.results.items():
            if category == 'summary':
                continue
            
            print(f"\n{category.upper().replace('_', ' ')}:")
            if isinstance(checks, dict):
                for check_name, result in checks.items():
                    status = "✅ PASS" if result.get('status') == 'OK' else "⚠️ FAIL"
                    print(f"\n{status}: {check_name}")
                
                    # Print metrics
                    for k, v in result.items():
                        if k not in ['status', 'sample_failures', 'requirement']:
                            print(f"  {k.replace('_', ' ').title()}: {v}")
                
                    # Print requirement
                    if 'requirement' in result:
                        print(f"  Requirement: {result['requirement']}")
                
                    # Enhanced failure display
                    if result.get('status') != 'OK' and 'sample_failures' in result:
                        print("\n  Sample Problem Records:")
                        for sample in result['sample_failures'][:10]:  # Show first 10
                            print(f"  - {sample}")
                                    
    def _get_sample_failures(self, category: str, check_name: str) -> list:
        """Get sample records that failed specific checks"""
        samples = []
    
        if category == 'location_validity' and check_name == 'canadian_locations':
            # Get non-Canadian locations
            canadian_provinces = ['AB','BC','MB','NB','NL','NT','NS','NU','ON','PE','QC','SK','YT']
            pattern = '|'.join(f'\({p}\)|{p}$' for p in canadian_provinces)
            invalid = self.df[~self.df['location'].str.contains(pattern, na=False)]
        
            for _, row in invalid.head(3).iterrows():
                samples.append(f"ID: {row.get('id')} | {row.get('location')} | Job: {row.get('job_title')}")
    
        elif category == 'completeness' and 'missing' in check_name:
            # Get records with missing values
            field = check_name.replace('_missing', '')
            if field in self.df.columns:
                invalid = self.df[self.df[field].isna()]
                for _, row in invalid.head(3).iterrows():
                    samples.append(f"ID: {row.get('id')} | Missing {field}")
    
        return samples

def load_job_data(json_path: Path = None) -> List[Dict[str, Any]]:
    """Load job data from JSON file"""
    possible_paths = [json_path] if json_path else [DEFAULT_JSON_PATH] + ALTERNATE_PATHS
    
    for path in possible_paths:
        try:
            if path and path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logging.info(f"Loaded {len(data)} records from {path}")
                    return data
        except Exception as e:
            logging.warning(f"Failed to load {path}: {str(e)}")
    
    raise FileNotFoundError(f"Could not find job data in: {possible_paths}")

def main():
    parser = argparse.ArgumentParser(description="Canadian Job Market Data_Quality Checker")
    parser.add_argument('--json-path', help="Path to JSON input file", default=None)
    parser.add_argument('--output', help="Save JSON report to file", default=None)
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Load and validate data
        job_data = load_job_data(Path(args.json_path) if args.json_path else None)
        
        # Run quality checks
        checker = JobDataQualityChecker(job_data)
        if checker.run_all_checks():
            checker.print_report()
            
            # Save report if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(checker.results, f, indent=2)
                logging.info(f"Saved report to {args.output}")
                
        else:
            logging.error("Quality checks failed")
            
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()