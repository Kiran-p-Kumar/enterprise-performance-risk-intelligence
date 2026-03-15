import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. UPDATED PATHS (Direct paths from the Project Root)
DATA_PATH = 'processed_data/Enterprise_Intelligence_Refined_40k.csv'
VISUALS_DIR = 'visuals'

# Create visuals folder if it doesn't exist in the root
if not os.path.exists(VISUALS_DIR):
    os.makedirs(VISUALS_DIR)

# 2. LOAD DATA
print("--- PROJECT: Enterprise Performance and Risk Intelligence Engine ---")
print(f"--- Step 1: Ingesting Data from: {DATA_PATH} ---")

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print("ERROR: Could not find the file. Ensure you are running the script from the Project Root folder!")
    exit()

# 3. CALCULATE THE LEAKAGE
leakage_mask = (df['Efficiency_Ratio'] < 1.5) & (df['Monthly_Salary'] > 8500)
total_leakage = df[leakage_mask]['Monthly_Salary'].sum()
print(f"--- Step 2: Audit Result: Monthly Leakage Identified: ${total_leakage:,.2f} ---")

# 4. GENERATE THE BURNOUT CHART
plt.figure(figsize=(12, 7))
sns.scatterplot(data=df.sample(2000), x='Overtime_Hrs', y='Satisfaction_Score', 
                hue='Dept', palette='magma', alpha=0.6)

plt.axvline(x=45, color='red', linestyle='--', linewidth=3, label='Critical Burnout Wall (45 hrs)')
plt.title('Diagnostic: Operational Risk Thresholds', fontsize=15)
plt.xlabel('Monthly Overtime Hours')
plt.ylabel('Employee Satisfaction Score')
plt.legend()

# 5. SAVE THE VISUAL
save_path = os.path.join(VISUALS_DIR, 'burnout_diagnostic_plot.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"--- Step 3: SUCCESS: Visual saved to {save_path} ---")

# 6. SHOW THE PLOT
plt.show()