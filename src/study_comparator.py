import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional

class StudyComparator:
    """Advanced comparison and benchmarking between studies"""
    
    def __init__(self, cross_study_analyzer):
        self.analyzer = cross_study_analyzer
    
    def benchmark_studies(self, benchmark_metric: str = 'Data_Quality_Score') -> pd.DataFrame:
        """Benchmark studies against each other"""
        metrics_df = self.analyzer.calculate_study_metrics()
        
        if metrics_df.empty:
            return pd.DataFrame()
        
        if benchmark_metric not in metrics_df.columns:
            benchmark_metric = 'Data_Quality_Score'
        
        # Calculate rankings
        metrics_df[f'{benchmark_metric}_Rank'] = metrics_df[benchmark_metric].rank(ascending=False, method='min')
        metrics_df[f'{benchmark_metric}_Percentile'] = metrics_df[benchmark_metric].rank(pct=True) * 100
        
        # Add performance category
        def categorize_performance(score):
            if score >= 90:
                return 'Excellent'
            elif score >= 80:
                return 'Good'
            elif score >= 70:
                return 'Fair'
            else:
                return 'Needs Improvement'
        
        metrics_df['Performance_Category'] = metrics_df[benchmark_metric].apply(categorize_performance)
        
        return metrics_df
    
    def identify_best_practices(self) -> Dict[str, List[str]]:
        """Identify potential best practices from top-performing studies"""
        metrics_df = self.analyzer.calculate_study_metrics()
        
        if metrics_df.empty or len(metrics_df) < 2:
            return {}
        
        # Get top 3 studies
        top_studies = metrics_df.nlargest(3, 'Data_Quality_Score')
        
        best_practices = {
            'top_studies': top_studies['Study_ID'].tolist(),
            'avg_score_top3': round(top_studies['Data_Quality_Score'].mean(), 1),
            'characteristics': []
        }
        
        # Analyze characteristics
        for study_id in top_studies['Study_ID']:
            score = top_studies.loc[top_studies['Study_ID'] == study_id, 'Data_Quality_Score'].iloc[0]
            best_practices['characteristics'].append(f"{study_id}: Score {score}/100")
        
        return best_practices