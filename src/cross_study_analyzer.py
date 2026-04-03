import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional

class CrossStudyAnalyzer:
    """Analyze and compare multiple clinical studies"""
    
    def __init__(self, multi_study_loader):
        self.loader = multi_study_loader
        self.study_metrics = pd.DataFrame()
    
    def calculate_study_metrics(self) -> pd.DataFrame:
        """Calculate key metrics for all loaded studies"""
        print("📊 Calculating study metrics...")
        
        metrics_list = []
        
        for study_id in self.loader.get_loaded_studies():
            if study_id in self.loader.study_data:
                metrics = self._calculate_single_study_metrics(study_id)
                metrics_list.append(metrics)
        
        if metrics_list:
            self.study_metrics = pd.DataFrame(metrics_list)
            print(f"✅ Calculated metrics for {len(metrics_list)} studies")
            return self.study_metrics
        else:
            print("❌ No loaded studies found!")
            return pd.DataFrame()
    
    def _calculate_single_study_metrics(self, study_id: str) -> Dict:
        """Calculate metrics for a single study"""
        study_data = self.loader.study_data[study_id]['files']
        
        # Initialize metrics
        metrics = {
            'Study_ID': study_id,
            'File_Count': len(study_data),
            'Total_Rows': 0,
            'Total_Columns': 0,
            'Data_Quality_Score': 0,
            'Estimated_Patients': 0,
            'Issue_Count': 0,
            'Completeness_Rate': 0
        }
        
        # Calculate aggregated metrics
        total_rows = 0
        total_columns = 0
        total_missing = 0
        total_cells = 0
        
        for file_name, df in study_data.items():
            total_rows += len(df)
            total_columns += len(df.columns)
            total_missing += df.isnull().sum().sum()
            total_cells += df.size
            
            # Try to estimate patient count
            patient_cols = [col for col in df.columns if 'patient' in str(col).lower() or 'id' in str(col).lower()]
            if patient_cols:
                patient_col = patient_cols[0]
                try:
                    unique_patients = df[patient_col].nunique()
                    metrics['Estimated_Patients'] = max(metrics['Estimated_Patients'], unique_patients)
                except:
                    pass
        
        metrics['Total_Rows'] = total_rows
        metrics['Total_Columns'] = total_columns
        
        # Calculate data quality score
        if total_cells > 0:
            completeness = 1 - (total_missing / total_cells)
            metrics['Completeness_Rate'] = round(completeness * 100, 1)
            metrics['Data_Quality_Score'] = round(completeness * 100, 1)
        
        # Estimate issue count
        metrics['Issue_Count'] = int(total_missing * 0.1)  # Simplified
        
        return metrics
    
    def compare_studies(self, metric: str = 'Data_Quality_Score'):
        """Create comparison chart for studies"""
        if self.study_metrics.empty:
            self.calculate_study_metrics()
        
        if self.study_metrics.empty:
            print("❌ No study metrics available!")
            return go.Figure()
        
        if metric not in self.study_metrics.columns:
            metric = 'Data_Quality_Score'
        
        # Create bar chart
        fig = px.bar(
            self.study_metrics,
            x='Study_ID',
            y=metric,
            title=f'Study Comparison: {metric}',
            color='Study_ID',
            text=metric,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            xaxis_title="Study ID",
            yaxis_title=metric,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        
        return fig
    
    def create_study_heatmap(self):
        """Create heatmap of study metrics"""
        if self.study_metrics.empty:
            self.calculate_study_metrics()
        
        if self.study_metrics.empty:
            print("❌ No study metrics available!")
            return go.Figure()
        
        # Select numeric columns for heatmap
        numeric_cols = self.study_metrics.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numeric metrics available!")
            return go.Figure()
        
        # Prepare data for heatmap
        heatmap_df = self.study_metrics[['Study_ID'] + list(numeric_cols)]
        heatmap_values = heatmap_df.set_index('Study_ID').values
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_values,
            x=numeric_cols,
            y=heatmap_df['Study_ID'],
            colorscale='Viridis',
            showscale=True,
            text=np.round(heatmap_values, 1),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Study Metrics Heatmap',
            xaxis_title="Metrics",
            yaxis_title="Study ID",
            height=400
        )
        
        return fig
    
    def identify_top_performers(self, top_n: int = 5):
        """Identify top performing studies"""
        if self.study_metrics.empty:
            self.calculate_study_metrics()
        
        if self.study_metrics.empty:
            return pd.DataFrame()
        
        if 'Data_Quality_Score' in self.study_metrics.columns:
            top_studies = self.study_metrics.nlargest(top_n, 'Data_Quality_Score')
            return top_studies[['Study_ID', 'Data_Quality_Score', 'Completeness_Rate', 'Estimated_Patients']]
        
        return pd.DataFrame()
    
    def generate_cross_study_report(self) -> Dict[str, Any]:
        """Generate comprehensive cross-study report"""
        if self.study_metrics.empty:
            self.calculate_study_metrics()
        
        report = {
            'summary': {},
            'recommendations': [],
            'insights': []
        }
        
        if not self.study_metrics.empty:
            # Basic summary
            report['summary'] = {
                'total_studies': len(self.study_metrics),
                'avg_data_quality': round(self.study_metrics['Data_Quality_Score'].mean(), 1),
                'total_estimated_patients': int(self.study_metrics['Estimated_Patients'].sum()),
                'total_files': int(self.study_metrics['File_Count'].sum()),
                'best_study': self.study_metrics.loc[self.study_metrics['Data_Quality_Score'].idxmax(), 'Study_ID'] if len(self.study_metrics) > 0 else 'N/A',
                'worst_study': self.study_metrics.loc[self.study_metrics['Data_Quality_Score'].idxmin(), 'Study_ID'] if len(self.study_metrics) > 0 else 'N/A'
            }
            
            # Generate recommendations
            avg_quality = report['summary']['avg_data_quality']
            if avg_quality < 70:
                report['recommendations'].append("Overall data quality is below target (70). Implement standardized data collection procedures.")
            elif avg_quality < 80:
                report['recommendations'].append("Data quality is acceptable but could be improved. Consider additional data validation checks.")
            else:
                report['recommendations'].append("Excellent data quality! Maintain current standards.")
            
            # Generate insights
            report['insights'].append(f"Average data quality across {len(self.study_metrics)} studies: {avg_quality}/100")
            report['insights'].append(f"Total estimated patients across all studies: {report['summary']['total_estimated_patients']}")
            report['insights'].append(f"Total files analyzed: {report['summary']['total_files']}")
        
        return report

# Test the analyzer
if __name__ == "__main__":
    print("Testing CrossStudyAnalyzer...")
    print("=" * 50)
    
    from multi_study_loader import MultiStudyClinicalDataLoader
    
    loader = MultiStudyClinicalDataLoader("data")
    
    if loader.studies:
        # Load first 2 studies for testing
        study_ids = list(loader.studies.keys())[:2]
        for study_id in study_ids:
            loader.load_study(study_id)
        
        if loader.study_data:
            analyzer = CrossStudyAnalyzer(loader)
            
            # Calculate metrics
            metrics = analyzer.calculate_study_metrics()
            print(f"\n📊 Study Metrics:")
            print(metrics.to_string())
            
            # Generate report
            report = analyzer.generate_cross_study_report()
            print(f"\n📋 Cross-Study Report:")
            print(f"  Total Studies: {report['summary'].get('total_studies', 0)}")
            print(f"  Average Data Quality: {report['summary'].get('avg_data_quality', 0)}/100")
            print(f"  Total Estimated Patients: {report['summary'].get('total_estimated_patients', 0)}")
            
            print(f"\n💡 Insights:")
            for insight in report['insights']:
                print(f"  • {insight}")
            
            print(f"\n🎯 Recommendations:")
            for rec in report['recommendations']:
                print(f"  • {rec}")
            
            print("\n✅ Test completed successfully!")
    else:
        print("❌ No studies found to analyze!")