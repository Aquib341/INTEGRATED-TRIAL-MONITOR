import pandas as pd
import numpy as np
import os
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

class ClinicalDataLoader:
    """Load clinical trial data from Excel files in subdirectories"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.dataframes = {}
        self.study_folders = []
        self._discover_study_folders()
    
    def _discover_study_folders(self):
        """Discover all study folders in the data directory"""
        if not os.path.exists(self.data_path):
            print(f"❌ Data directory '{self.data_path}' not found!")
            return
        
        # List all items in data directory
        items = os.listdir(self.data_path)
        
        # Filter for directories that look like studies
        self.study_folders = []
        for item in items:
            item_path = os.path.join(self.data_path, item)
            if os.path.isdir(item_path):
                # Check if it has Excel files
                excel_files = self._find_excel_files(item_path)
                if excel_files:
                    self.study_folders.append({
                        'name': item,
                        'path': item_path,
                        'excel_files': excel_files
                    })
        
        print(f"📁 Found {len(self.study_folders)} study folders")
    
    def _find_excel_files(self, folder_path: str) -> List[str]:
        """Find all Excel files in a folder (including subfolders)"""
        excel_files = []
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.xlsx', '.xls')):
                    full_path = os.path.join(root, file)
                    excel_files.append(full_path)
        
        return excel_files
    
    def load_all_data(self) -> Dict[str, Dict]:
        """Load data from all study folders"""
        print("📂 Loading data from all study folders...")
        
        all_data = {}
        
        for study in self.study_folders:
            study_name = study['name']
            print(f"  📁 Processing: {study_name}")
            
            study_data = {}
            for excel_file in study['excel_files']:
                file_name = os.path.basename(excel_file)
                try:
                    # Try to load all sheets from the Excel file
                    excel_data = pd.ExcelFile(excel_file)
                    
                    for sheet_name in excel_data.sheet_names:
                        df = excel_data.parse(sheet_name)
                        key = f"{file_name} - {sheet_name}"
                        study_data[key] = df
                        
                        # Also add to main dataframes with study prefix
                        main_key = f"{study_name} - {key}"
                        self.dataframes[main_key] = df
                        
                        print(f"    ✅ Loaded: {file_name} - {sheet_name} ({len(df)} rows)")
                        
                except Exception as e:
                    print(f"    ❌ Error loading {file_name}: {str(e)}")
                    continue
            
            all_data[study_name] = study_data
        
        print(f"✅ Loaded {len(self.dataframes)} dataframes from {len(self.study_folders)} studies")
        return all_data
    
    def get_summary(self) -> pd.DataFrame:
        """Get summary of all loaded data"""
        summary_data = []
        
        for key, df in self.dataframes.items():
            # Extract study name and file name
            if ' - ' in key:
                study_name, rest = key.split(' - ', 1)
                if ' - ' in rest:
                    file_name, sheet_name = rest.split(' - ', 1)
                else:
                    file_name = rest
                    sheet_name = 'Sheet1'
            else:
                study_name = 'Unknown'
                file_name = key
                sheet_name = 'Sheet1'
            
            summary_data.append({
                'Study': study_name,
                'File': file_name,
                'Sheet': sheet_name,
                'Rows': len(df),
                'Columns': len(df.columns),
                'Missing_Values': df.isnull().sum().sum(),
                'File_Type': 'Excel'
            })
        
        return pd.DataFrame(summary_data)
    
    def get_study_names(self) -> List[str]:
        """Get list of all study names"""
        return [study['name'] for study in self.study_folders]
    
    def load_specific_study(self, study_name: str) -> Dict[str, pd.DataFrame]:
        """Load data from a specific study"""
        for study in self.study_folders:
            if study['name'] == study_name:
                study_data = {}
                
                for excel_file in study['excel_files']:
                    file_name = os.path.basename(excel_file)
                    try:
                        excel_data = pd.ExcelFile(excel_file)
                        
                        for sheet_name in excel_data.sheet_names:
                            df = excel_data.parse(sheet_name)
                            key = f"{file_name} - {sheet_name}"
                            study_data[key] = df
                            
                            # Also add to main dataframes
                            main_key = f"{study_name} - {key}"
                            self.dataframes[main_key] = df
                            
                    except Exception as e:
                        print(f"Error loading {file_name} from {study_name}: {str(e)}")
                        continue
                
                return study_data
        
        print(f"Study '{study_name}' not found!")
        return {}

# Test the loader
if __name__ == "__main__":
    print("Testing ClinicalDataLoader...")
    print("=" * 50)
    
    loader = ClinicalDataLoader("data")
    
    if not loader.study_folders:
        print("No study folders found with Excel files!")
        print("Current files in 'data':", os.listdir("data"))
    else:
        print(f"Found {len(loader.study_folders)} study folders:")
        for study in loader.study_folders[:5]:  # Show first 5
            print(f"  • {study['name']}: {len(study['excel_files'])} Excel files")
        
        if len(loader.study_folders) > 5:
            print(f"  ... and {len(loader.study_folders) - 5} more")
        
        print("\nLoading data...")
        data = loader.load_all_data()
        
        print("\n📊 Summary:")
        summary = loader.get_summary()
        print(summary.to_string())
        
        print("\n✅ Test completed successfully!")