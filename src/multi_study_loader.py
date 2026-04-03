import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

class MultiStudyClinicalDataLoader:
    """Load and manage multiple clinical studies from your folder structure"""
    
    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        self.studies = {}  # Store study metadata
        self.study_data = {}  # Store loaded study data
        self._discover_studies()
    
    def _discover_studies(self) -> Dict[str, Dict]:
        """Discover all studies in the base directory"""
        studies = {}
        
        if not os.path.exists(self.base_path):
            print(f"❌ Data directory '{self.base_path}' not found!")
            return studies
        
        # Look for study directories (folders in data/)
        for item in os.listdir(self.base_path):
            item_path = os.path.join(self.base_path, item)
            if os.path.isdir(item_path):
                # Check for Excel files in this folder
                excel_files = self._scan_for_excel_files(item_path)
                if excel_files:
                    studies[item] = {
                        'path': item_path,
                        'files': excel_files,
                        'file_count': len(excel_files),
                        'status': 'Discovered'
                    }
                    print(f"📁 Found study: {item} ({len(excel_files)} Excel files)")
        
        self.studies = studies
        print(f"✅ Discovered {len(studies)} studies")
        return studies
    
    def _scan_for_excel_files(self, folder_path: str) -> Dict[str, str]:
        """Scan a folder for Excel files"""
        excel_files = {}
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.xlsx', '.xls')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)
                    excel_files[relative_path] = file_path
        
        return excel_files
    
    def load_study(self, study_id: str) -> Dict[str, pd.DataFrame]:
        """Load all Excel files for a specific study"""
        if study_id not in self.studies:
            print(f"❌ Study '{study_id}' not found!")
            return {}
        
        print(f"📂 Loading study: {study_id}")
        study_info = self.studies[study_id]
        loaded_data = {}
        
        for file_name, file_path in study_info['files'].items():
            try:
                # Load Excel file
                excel_file = pd.ExcelFile(file_path)
                
                # Load each sheet
                for sheet_name in excel_file.sheet_names:
                    df = excel_file.parse(sheet_name)
                    key = f"{os.path.basename(file_path)} - {sheet_name}"
                    loaded_data[key] = df
                    
                    print(f"  ✅ Loaded: {os.path.basename(file_path)} - {sheet_name} ({len(df)} rows)")
                
            except Exception as e:
                print(f"  ❌ Error loading {file_name}: {str(e)}")
                continue
        
        self.study_data[study_id] = {
            'files': loaded_data,
            'info': study_info,
            'dataframes': loaded_data,
            'loaded_at': pd.Timestamp.now()
        }
        
        self.studies[study_id]['status'] = 'Loaded'
        print(f"✅ Successfully loaded {len(loaded_data)} dataframes from {study_id}")
        
        return loaded_data
    
    def load_all_studies(self) -> Dict[str, Dict]:
        """Load all discovered studies"""
        print(f"📂 Loading all {len(self.studies)} studies...")
        
        for study_id in self.studies.keys():
            self.load_study(study_id)
        
        return self.study_data
    
    def get_study_summary(self, study_id: str) -> Dict[str, Any]:
        """Get summary statistics for a study"""
        if study_id not in self.study_data:
            print(f"Study '{study_id}' not loaded. Loading now...")
            self.load_study(study_id)
        
        if study_id not in self.study_data:
            return {}
        
        study_data = self.study_data[study_id]['files']
        summary = {
            'study_id': study_id,
            'file_count': len(study_data),
            'total_rows': 0,
            'total_columns': 0,
            'file_details': []
        }
        
        for file_name, df in study_data.items():
            file_info = {
                'file': file_name,
                'rows': len(df),
                'columns': len(df.columns),
                'missing_values': df.isnull().sum().sum(),
                'dtypes': str(df.dtypes.to_dict())
            }
            summary['file_details'].append(file_info)
            summary['total_rows'] += len(df)
            summary['total_columns'] += len(df.columns)
        
        return summary
    
    def list_studies(self) -> List[str]:
        """List all discovered studies"""
        return list(self.studies.keys())
    
    def get_loaded_studies(self) -> List[str]:
        """List all loaded studies"""
        return list(self.study_data.keys())

# Test the loader
if __name__ == "__main__":
    print("Testing MultiStudyClinicalDataLoader...")
    print("=" * 50)
    
    loader = MultiStudyClinicalDataLoader("data")
    
    if loader.studies:
        print(f"\n📋 Discovered Studies:")
        for study_id, info in list(loader.studies.items())[:5]:
            print(f"  • {study_id}: {info['file_count']} files")
        
        # Load first study as test
        if loader.studies:
            first_study = list(loader.studies.keys())[0]
            print(f"\n📂 Loading first study: {first_study}")
            data = loader.load_study(first_study)
            
            if data:
                print(f"✅ Successfully loaded {len(data)} files from {first_study}")
                
                # Get summary
                summary = loader.get_study_summary(first_study)
                print(f"\n📊 Study Summary:")
                print(f"  Files: {summary.get('file_count', 0)}")
                print(f"  Total Rows: {summary.get('total_rows', 0)}")
                print(f"  Total Columns: {summary.get('total_columns', 0)}")
    else:
        print("❌ No studies found!")
        print("Current files in 'data':", os.listdir("data"))