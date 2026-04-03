import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime

class DataIntegrator:
    """Integrate and process clinical trial data from multiple sources"""
    
    def __init__(self, data_loader):
        self.loader = data_loader
        self.data = data_loader.dataframes
        self.unified_data = None
        self.patient_metrics = None
    
    def create_unified_patient_view(self) -> pd.DataFrame:
        """Create a unified view of patient data from multiple sources"""
        print("🔧 Creating unified patient view...")
        
        patient_records = []
        
        for key, df in self.data.items():
            # Look for patient-related data
            patient_cols = [col for col in df.columns if 'patient' in str(col).lower() or 'id' in str(col).lower()]
            
            if patient_cols:
                # Use the first patient column found
                patient_col = patient_cols[0]
                
                # Create basic patient record
                for idx, row in df.iterrows():
                    patient_id = str(row[patient_col]) if pd.notna(row[patient_col]) else f"Unknown_{key}_{idx}"
                    
                    record = {
                        'Patient_ID': patient_id,
                        'Source_File': key,
                        'Row_Index': idx,
                        'Study': key.split(' - ')[0] if ' - ' in key else 'Unknown'
                    }
                    
                    # Add other columns
                    for col in df.columns:
                        if col != patient_col:
                            record[col] = row[col]
                    
                    patient_records.append(record)
        
        if patient_records:
            unified_df = pd.DataFrame(patient_records)
            self.unified_data = unified_df
            print(f"✅ Created unified view with {len(unified_df)} patient records")
            return unified_df
        else:
            print("❌ No patient data found!")
            return pd.DataFrame()
    
    def calculate_patient_metrics(self) -> pd.DataFrame:
        """Calculate metrics for each patient"""
        if self.unified_data is None:
            self.create_unified_patient_view()
        
        if self.unified_data.empty:
            print("❌ No data available for metrics calculation")
            return pd.DataFrame()
        
        print("📊 Calculating patient metrics...")
        
        # Group by patient
        patient_groups = self.unified_data.groupby('Patient_ID')
        
        metrics_list = []
        
        for patient_id, group in patient_groups:
            # Basic metrics
            record_count = len(group)
            source_count = group['Source_File'].nunique()
            study_count = group['Study'].nunique()
            
            # Calculate data quality indicators
            missing_values = group.isnull().sum().sum()
            total_cells = group.size
            completeness_score = 100 - (missing_values / total_cells * 100) if total_cells > 0 else 0
            
            # Count issues (simplified)
            issue_count = 0
            
            # Check for common issues
            for col in group.columns:
                if 'missing' in str(col).lower() or 'incomplete' in str(col).lower():
                    issue_count += group[col].astype(str).str.contains('yes|true|1', case=False).sum()
            
            # Determine patient status based on metrics
            if completeness_score >= 90 and issue_count == 0:
                status = 'Clean'
                risk_level = 'Low'
            elif completeness_score >= 75:
                status = 'Needs Review'
                risk_level = 'Medium'
            else:
                status = 'Critical'
                risk_level = 'High'
            
            metrics = {
                'Patient_ID': patient_id,
                'Record_Count': record_count,
                'Source_Count': source_count,
                'Study_Count': study_count,
                'Data_Quality_Score': round(completeness_score, 1),
                'Issue_Count': int(issue_count),
                'Patient_Status': status,
                'Risk_Level': risk_level,
                'Studies': ', '.join(group['Study'].unique())
            }
            
            metrics_list.append(metrics)
        
        metrics_df = pd.DataFrame(metrics_list)
        self.patient_metrics = metrics_df
        
        print(f"✅ Calculated metrics for {len(metrics_df)} patients")
        return metrics_df
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for all data"""
        if self.patient_metrics is None:
            self.calculate_patient_metrics()
        
        if self.patient_metrics.empty:
            return {
                'total_patients': 0,
                'avg_data_quality_score': 0,
                'critical_patients': 0,
                'clean_patients': 0
            }
        
        total_patients = len(self.patient_metrics)
        avg_score = self.patient_metrics['Data_Quality_Score'].mean()
        critical_count = (self.patient_metrics['Patient_Status'] == 'Critical').sum()
        clean_count = (self.patient_metrics['Patient_Status'] == 'Clean').sum()
        needs_review_count = (self.patient_metrics['Patient_Status'] == 'Needs Review').sum()
        
        summary = {
            'total_patients': total_patients,
            'avg_data_quality_score': round(avg_score, 1),
            'critical_patients': critical_count,
            'clean_patients': clean_count,
            'needs_review_patients': needs_review_count,
            'critical_percentage': round((critical_count / total_patients) * 100, 1) if total_patients > 0 else 0,
            'clean_percentage': round((clean_count / total_patients) * 100, 1) if total_patients > 0 else 0,
            'total_studies': len(self.loader.study_folders),
            'total_dataframes': len(self.data)
        }
        
        return summary
    
    def get_top_patients_by_issue(self, issue_type: str = 'total_issues', n: int = 10) -> pd.DataFrame:
        """Get top patients with most issues"""
        if self.patient_metrics is None:
            self.calculate_patient_metrics()
        
        if self.patient_metrics.empty:
            return pd.DataFrame()
        
        # Sort by issue count (descending)
        top_patients = self.patient_metrics.sort_values('Issue_Count', ascending=False).head(n)
        
        return top_patients[['Patient_ID', 'Data_Quality_Score', 'Issue_Count', 'Patient_Status', 'Risk_Level']]

# Test the integrator
if __name__ == "__main__":
    print("Testing DataIntegrator...")
    print("=" * 50)
    
    from data_loader import ClinicalDataLoader
    
    loader = ClinicalDataLoader("data")
    data = loader.load_all_data()
    
    if data:
        integrator = DataIntegrator(loader)
        
        # Create unified view
        unified_data = integrator.create_unified_patient_view()
        
        if not unified_data.empty:
            print(f"\n📋 Unified Data Sample ({len(unified_data)} records):")
            print(unified_data.head())
            
            # Calculate metrics
            metrics = integrator.calculate_patient_metrics()
            
            if not metrics.empty:
                print(f"\n📊 Patient Metrics ({len(metrics)} patients):")
                print(metrics.head())
                
                # Get summary
                summary = integrator.get_summary_stats()
                print(f"\n📈 Summary Statistics:")
                for key, value in summary.items():
                    print(f"  {key}: {value}")
                
                # Get top patients with issues
                top_patients = integrator.get_top_patients_by_issue(n=5)
                print(f"\n🚨 Top 5 Patients with Most Issues:")
                print(top_patients.to_string())
                
                print("\n✅ Test completed successfully!")
    else:
        print("❌ No data loaded!")