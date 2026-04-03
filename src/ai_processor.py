class AISummarizer:
    """Basic AI-powered summarization (simulated for now)"""
    
    @staticmethod
    def summarize_site_performance(site_data):
        """Generate summary for site performance"""
        if len(site_data) == 0:
            return "No data available for this site."
        
        # Simple summary logic (replace with real AI later)
        avg_score = site_data['Data_Quality_Score'].mean()
        critical_count = (site_data['Patient_Status'] == 'Critical').sum()
        total_patients = len(site_data)
        
        summary = f"""
        **Site Performance Summary:**
        - Average Data Quality Score: {avg_score:.1f}/100
        - Critical Patients: {critical_count} out of {total_patients}
        - Clean Patients: {(site_data['Patient_Status'] == 'Clean').sum()}
        
        **Recommendations:**
        """
        
        if avg_score < 70:
            summary += "- Schedule immediate monitoring visit\n"
            summary += "- Review missing data collection processes\n"
        elif critical_count > 0:
            summary += "- Follow up on critical patients this week\n"
        else:
            summary += "- Performance is within acceptable limits\n"
        
        return summary
    
    @staticmethod
    def generate_risk_alerts(patient_data):
        """Generate risk alerts based on data"""
        alerts = []
        
        # Simple alert logic
        critical_patients = patient_data[patient_data['Patient_Status'] == 'Critical']
        
        for _, patient in critical_patients.iterrows():
            alert = {
                'patient_id': patient.get('Patient_ID', 'Unknown'),
                'score': patient.get('Data_Quality_Score', 0),
                'reason': 'Low data quality score',
                'priority': 'High'
            }
            alerts.append(alert)
        
        return alerts