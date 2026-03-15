import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def generate_dashboard_csv():
    # 1. SET PATHS
    input_file = 'processed_data/Enterprise_Intelligence_Refined_40k.csv'
    output_file = 'processed_data/Enterprise_Final_Intelligence_40k.csv'

    if not os.path.exists(input_file):
        logging.error("Source file not found! Run the Phase 2 cleaning script first.")
        return

    # 2. LOAD DATA
    df = pd.read_csv(input_file)
    
    # 3. PREPARE AI FEATURES
    features = ['Monthly_Salary', 'Efficiency_Ratio', 'Strain_Index']
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features].fillna(0))

    # 4. K-MEANS CLUSTERING (Segmentation)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster_ID'] = kmeans.fit_predict(scaled_features)

    # 5. ISOLATION FOREST (Identifying the 'Outliers')
    iso = IsolationForest(contamination=0.01, random_state=42)
    df['Anomaly_Flag'] = iso.fit_predict(scaled_features)
    df['Is_Outlier'] = df['Anomaly_Flag'].map({1: 'No', -1: 'Yes'})

    # 6. BUSINESS LABELING (The Dashboard Categories)
    # We map the AI's math to real-world business segments
    segment_map = {
        0: 'Steady Professional',
        1: 'High-Impact Asset',
        2: 'Critical Burnout Risk',
        3: 'Operational Leakage (Low ROI)'
    }
    df['Performance_Segment'] = df['Cluster_ID'].map(segment_map)

    # 7. EXPORT THE "DASHBOARD-READY" CSV
    # We drop the helper columns to keep it clean for Power BI
    cols_to_keep = [
        'Emp_ID', 'Dept', 'Monthly_Salary', 'Revenue_Impact', 
        'Tickets_Resolved', 'Overtime_Hrs', 'Satisfaction_Score', 
        'Efficiency_Ratio', 'Strain_Index', 'Performance_Segment', 'Is_Outlier'
    ]
    df[cols_to_keep].to_csv(output_file, index=False)
    
    logging.info("="*50)
    logging.info(f"DASHBOARD DATA GENERATED: {output_file}")
    logging.info(f"Total Records Exported: {len(df)}")
    logging.info("="*50)

if __name__ == "__main__":
    generate_dashboard_csv()