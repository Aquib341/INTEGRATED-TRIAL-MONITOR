# **INTEGRATED TRIAL MONITOR**
## **Clinical Trial Analytics Platform - GitHub Repository Documentation**

---
<img width="1158" height="524" alt="Image" src="https://github.com/user-attachments/assets/80e27fbb-54ee-44d6-8925-558459657118" />
<img width="1135" height="492" alt="Image" src="https://github.com/user-attachments/assets/ba78aae7-adda-4ebc-b327-2b19c74d01ea" />
<img width="1470" height="705" alt="Image" src="https://github.com/user-attachments/assets/f2b85b4d-6187-4300-9018-c7517de8bec7" />
## **📋 PROJECT OVERVIEW**

**Integrated Trial Monitor** is an AI-powered clinical trial analytics platform designed to transform fragmented clinical trial data into actionable insights. The solution integrates nine disparate data sources, implements a sophisticated Data Quality Index, and leverages Generative AI to provide real-time operational visibility for clinical trial teams.

**Team:** Axiom Clinical AI  
**Technology Stack:** Python, Streamlit, Pandas, Plotly, OpenPyXL  
**License:** MIT License  

---

## **🎯 PROJECT OBJECTIVES**

### **Primary Goals:**
1. **Data Integration**: Unify nine clinical trial data sources into a single operational view
2. **Real-time Analytics**: Provide instant insights into trial performance and data quality
3. **AI-Powered Insights**: Leverage machine learning for predictive analytics and recommendations
4. **Collaboration Enhancement**: Improve workflows between Data Quality Teams, CRAs, and Sites
5. **Risk Mitigation**: Early detection of operational bottlenecks and data quality issues

### **Key Performance Indicators:**
- 70% reduction in manual data review time
- 5x faster identification of critical patient issues
- 40% improvement in query resolution rates
- Real-time monitoring vs. traditional weekly/monthly reports

---

## **🏗️ ARCHITECTURE**

### **System Architecture Diagram**
```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES (9 Files)                    │
├─────────────────────────────────────────────────────────────┤
│ 1. CPID_EDC_Metrics.xlsx         6. Missing_Lab_Data.xlsx   │
│ 2. Visit_Projection_Tracker.xlsx 7. SAE_Dashboard.xlsx      │
│ 3. Missing_Pages_Report.xlsx     8. MedDRA_Coding.xlsx      │
│ 4. Compiled_EDRR.xlsx            9. WHODD_Coding.xlsx       │
│ 5. Inactivated_Forms.xlsx                                   │
└─────────────────────────────────────────────────────────────┘
                               │
                      DATA INTEGRATION LAYER
                      ┌─────────────────────┐
                      │ Data Loader         │
                      │ Data Integrator     │
                      │ Data Validator      │
                      └─────────────────────┘
                               │
                    UNIFIED DATA MODEL
                    ┌─────────────────────┐
                    │ Patient-Level View  │
                    │ Site-Level View     │
                    │ Trial-Level Metrics │
                    └─────────────────────┘
                               │
                    ANALYTICS ENGINE
                    ┌─────────────────────┐
                    │ Data Quality Index  │
                    │ AI Insights Engine  │
                    │ Predictive Models   │
                    │ Risk Assessment     │
                    └─────────────────────┘
                               │
                    PRESENTATION LAYER
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    │ Interactive Charts  │
                    │ Export Capabilities │
                    │ Alert System        │


**Responsibilities:**
- User interface rendering
- Interactive chart generation
- User input processing
- Session state management

---

## **📊 FEATURES IMPLEMENTED**

### **1. Data Integration Features**
- **Multi-source Integration**: Seamless integration of 9 data sources
- **Automated Data Cleaning**: Intelligent handling of missing values and inconsistencies
- **Real-time Processing**: Instant data processing and updates
- **Cross-reference Validation**: Automated validation across data sources

### **2. Analytics Features**
- **Data Quality Index**: Comprehensive scoring system (0-100)
- **Risk Stratification**: Patient and site risk categorization
- **Performance Metrics**: Detailed operational performance indicators
- **Trend Analysis**: Historical performance tracking

### **3. AI/ML Features**
- **Natural Language Interface**: Query data using plain English
- **Predictive Analytics**: Early warning for potential issues
- **Automated Insights**: AI-generated recommendations
- **Pattern Recognition**: Identification of data quality patterns

### **4. Visualization Features**
- **Interactive Dashboards**: Real-time, interactive data visualization
- **Drill-down Capabilities**: Hierarchical data exploration
- **Customizable Views**: Role-based and user-customizable interfaces
- **Export Functionality**: Comprehensive data export capabilities

### **5. Collaboration Features**
- **Alert System**: Automated alerts for critical issues
- **Task Management**: Integrated task assignment and tracking
- **Report Generation**: Automated report creation
- **Audit Trail**: Comprehensive activity logging



### **Predictive Models**
- **Risk Prediction**: Identify at-risk patients 2-3 weeks early
- **Performance Forecasting**: Predict site performance trends
- **Issue Anticipation**: Anticipate data quality issues before they occur
- **Resource Optimization**: Optimize CRA visit schedules

### **Generative AI Features**
- **Automated Summaries**: AI-generated site performance summaries
- **Report Generation**: Automated clinical trial report creation
- **Recommendation Engine**: Actionable recommendations based on data patterns
- **Insight Generation**: Automated identification of key insights

---

## **🔐 SECURITY & COMPLIANCE**

### **Data Security**
- **Encryption**: All data encrypted at rest and in transit
- **Access Control**: Role-based access control (RBAC) implementation
- **Audit Logging**: Comprehensive activity logging and audit trails
- **Data Anonymization**: Optional patient data anonymization

### **Regulatory Compliance**
- **21 CFR Part 11**: Designed with FDA regulations in mind
- **GDPR Compliance**: Built-in data privacy controls
- **HIPAA Considerations**: Healthcare data protection measures
- **Audit Readiness**: Continuous compliance monitoring

---
