def validate_data(patient_data):
    """Check data quality"""
    issues = []
    
    # Check for missing Patient_ID
    if 'Patient_ID' in patient_data.columns:
        missing_ids = patient_data['Patient_ID'].isna().sum()
        if missing_ids > 0:
            issues.append(f"❌ {missing_ids} missing Patient IDs")
    
    # Check Data Quality Score range
    if 'Data_Quality_Score' in patient_data.columns:
        invalid_scores = ((patient_data['Data_Quality_Score'] < 0) | 
                         (patient_data['Data_Quality_Score'] > 100)).sum()
        if invalid_scores > 0:
            issues.append(f"❌ {invalid_scores} invalid Data Quality Scores")
    
    return issues