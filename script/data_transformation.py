import pandas as pd

# 1. PATHS 
# Root Folder: EnterPrise Performance and Risk Intelligence Engine
# MAKE SURE THE EXTENSION IS .csv
INPUT_PATH = 'raw_data/Enterprise_Raw_Intelligence_40k.csv'
OUTPUT_PATH = 'processed_data/Enterprise_Intelligence_Refined_40k.csv'

print("--- PROJECT: Enterprise Performance and Risk Intelligence Engine ---")

# 2. LOAD DATA
print(f"--- Step 1: Ingesting Raw Data from: {INPUT_PATH} ---")
df = pd.read_csv(INPUT_PATH)

# 3. DEDUPLICATION
initial_rows = len(df)
df.drop_duplicates(inplace=True)
print(f"--- Step 2: Cleanse Complete. Removed {initial_rows - len(df)} redundant system entries. ---")

# 4. IMPUTATION (The 8% Gap)
df['Revenue_Impact'] = df.groupby('Dept')['Revenue_Impact'].transform(lambda x: x.fillna(x.median()))
print("--- Step 3: Resolved 8% Data Gap using Departmental Median Imputation. ---")

# 5. FEATURE ENGINEERING
# Efficiency Ratio: Revenue per $1 spent on Salary
df['Efficiency_Ratio'] = (df['Revenue_Impact'] / (df['Monthly_Salary'] + 0.01)).round(2)

# Strain Index: Overtime relative to Satisfaction
df['Strain_Index'] = (df['Overtime_Hrs'] / df['Satisfaction_Score']).round(2)
print("--- Step 4: Efficiency Metrics and Strain Indices Synthesized. ---")

# 6. SAVE
df.to_csv(OUTPUT_PATH, index=False)
print(f"--- SUCCESS: Sanitized file saved to: {OUTPUT_PATH} ---")