import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")

def perform_financial_analysis():
    """
    Performs financial analysis of cost savings from waste reduction and labor precision.
    Based on industry benchmarks and BlueprintBot v2 reported improvements.
    """
    
    # 1. Define Industry Benchmarks (Average for a $100M Project)
    project_value = 100_000_000  # $100M USD
    
    # Cost Breakdown (Industry Averages)
    # Materials: 40%, Labor: 35%, Overhead/Profit: 25%
    material_cost_base = project_value * 0.40
    labor_cost_base = project_value * 0.35
    
    # 2. Define Inefficiency Benchmarks (Pre-BlueprintBot)
    # Material Waste: 30% of material budget is "thrown away" (Industry avg)
    # Labor Inefficiency: 30% of labor hours are "idle/inefficient" (Industry avg)
    material_waste_rate_pre = 0.30
    labor_inefficiency_rate_pre = 0.30
    
    # 3. BlueprintBot v2 Improvements
    # Material Waste Reduction: 75% reduction in waste (from 30% to 7.5%)
    # Labor Precision Improvement: 75% reduction in inefficiency (from 30% to 7.5%)
    improvement_factor = 0.75
    
    material_waste_rate_post = material_waste_rate_pre * (1 - improvement_factor)
    labor_inefficiency_rate_post = labor_inefficiency_rate_pre * (1 - improvement_factor)
    
    # 4. Calculate Financial Impact
    # Pre-BPB Costs of Inefficiency
    material_waste_cost_pre = material_cost_base * material_waste_rate_pre
    labor_inefficiency_cost_pre = labor_cost_base * labor_inefficiency_rate_pre
    total_inefficiency_cost_pre = material_waste_cost_pre + labor_inefficiency_cost_pre
    
    # Post-BPB Costs of Inefficiency
    material_waste_cost_post = material_cost_base * material_waste_rate_post
    labor_inefficiency_cost_post = labor_cost_base * labor_inefficiency_rate_post
    total_inefficiency_cost_post = material_waste_cost_post + labor_inefficiency_cost_post
    
    # Total Savings
    material_savings = material_waste_cost_pre - material_waste_cost_post
    labor_savings = labor_inefficiency_cost_pre - labor_inefficiency_cost_post
    total_savings = material_savings + labor_savings
    
    # 5. Create Data for Visualization
    data = {
        'Category': ['Material Waste', 'Labor Inefficiency', 'Total Inefficiency'],
        'Pre-BlueprintBot ($M)': [material_waste_cost_pre/1e6, labor_inefficiency_cost_pre/1e6, total_inefficiency_cost_pre/1e6],
        'Post-BlueprintBot ($M)': [material_waste_cost_post/1e6, labor_inefficiency_cost_post/1e6, total_inefficiency_cost_post/1e6],
        'Savings ($M)': [material_savings/1e6, labor_savings/1e6, total_savings/1e6]
    }
    df = pd.DataFrame(data)
    
    # 6. Generate Visualizations
    plt.figure(figsize=(12, 7))
    
    # Bar Chart: Pre vs Post Inefficiency Costs
    df_melted = df.melt(id_vars='Category', value_vars=['Pre-BlueprintBot ($M)', 'Post-BlueprintBot ($M)'], 
                        var_name='Status', value_name='Cost ($M)')
    
    sns.barplot(data=df_melted, x='Category', y='Cost ($M)', hue='Status', palette=['#EF4444', '#10B981'])
    
    plt.title('Financial Impact of BlueprintBot v2: Inefficiency Cost Reduction', fontsize=16, fontweight='bold')
    plt.ylabel('Cost in Millions ($USD)', fontsize=12)
    plt.xlabel('Cost Category', fontsize=12)
    plt.legend(title='System Status')
    
    # Add text labels for savings
    for i, row in df.iterrows():
        plt.text(i, row['Pre-BlueprintBot ($M)'] + 0.5, f"Save: ${row['Savings ($M)']}M", 
                 ha='center', color='#059669', fontweight='bold')

    plt.tight_layout()
    plt.savefig('/home/ubuntu/blueprintbot_v2/financial_impact_chart.png')
    
    # 7. Print Summary for Report
    print(f"--- Financial Analysis Summary (Per $100M Project) ---")
    print(f"Project Value: ${project_value/1e6}M")
    print(f"Material Savings: ${material_savings/1e6}M")
    print(f"Labor Savings: ${labor_savings/1e6}M")
    print(f"Total Savings: ${total_savings/1e6}M")
    print(f"Efficiency Gain: {(total_savings/project_value)*100:.2f}% of total project budget")
    print(f"------------------------------------------------------")

if __name__ == "__main__":
    perform_financial_analysis()
