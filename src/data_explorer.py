import pandas as pd
import os

def explore_excel_file(file_path):
    """Explore what's inside an Excel file"""
    print(f"\n{'='*60}")
    print(f"Exploring: {os.path.basename(file_path)}")
    print('='*60)
    
    # Read Excel file
    try:
        # Get all sheet names
        xls = pd.ExcelFile(file_path, engine='openpyxl')  # ADD THIS
        sheets = xls.sheet_names
        print(f"Number of sheets: {len(sheets)}")
        print(f"Sheet names: {sheets}")
        
        # Show first few rows of each sheet
        for sheet in sheets[:3]:  # First 3 sheets only
            print(f"\n--- Sheet: {sheet} ---")
            df = pd.read_excel(file_path, sheet_name=sheet, nrows=5, engine='openpyxl')  # ADD THIS
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("\nFirst 3 rows:")
            print(df.head(3))
            
    except Exception as e:
        print(f"Error reading file: {e}")
        # Try to get more details
        import traceback
        traceback.print_exc()

def main():
    # List all Excel files in data folder
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        print(f"Create a 'data' folder and put your Excel files there!")
        os.makedirs(data_folder, exist_ok=True)
        print(f"Created 'data' folder. Please add your Excel files there.")
        return
    
    excel_files = [f for f in os.listdir(data_folder) if f.endswith('.xlsx') or f.endswith('.xls')]
    
    if not excel_files:
        print("No Excel files found in data folder!")
        print(f"Current files in '{data_folder}': {os.listdir(data_folder)}")
        return
    
    print(f"Found {len(excel_files)} Excel files:")
    for file in excel_files:
        print(f"  - {file}")
    
    # Explore each file
    for file in excel_files:
        file_path = os.path.join(data_folder, file)
        explore_excel_file(file_path)

if __name__ == "__main__":
    main()