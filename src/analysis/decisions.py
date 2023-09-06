import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set a constant seed for reproducibility
np.random.seed(42)

def count_responses(group):
    counts = group.iloc[:, 2:].apply(lambda col: col.value_counts()).fillna(0)
    yes_count = counts.loc['Yes'].sum() if 'Yes' in counts.index else 0
    no_count = counts.loc['No'].sum() if 'No' in counts.index else 0
    return pd.Series({'Yes': yes_count, 'No': no_count})

def write_statistics_to_txt(df, OUTPUT_DIR, input_file_name):
    output_file_path = os.path.join(OUTPUT_DIR, f'statistics_summary_{input_file_name}.txt')
    with open(output_file_path, 'w') as f:
        f.write("Statistical Summary of Probability of Affirmative Response\n")
        f.write("=" * 60 + '\n')
        for index, row in df.iterrows():
            f.write(f"Context Key: {row['context_key']}\n")
            f.write(f"Mean: {row['Mean']:.4f}\n")
            f.write(f"95% Confidence Interval: ({row['CI_Lower']:.4f}, {row['CI_Upper']:.4f})\n")
            f.write("-" * 60 + '\n')

def plot_bar_chart(df, title, OUTPUT_DIR, input_file_name, group_name=None):
    plt.figure(figsize=(10, len(df['context_key']) * 0.4 + 2))  # Dynamic figure size based on number of context keys
    
    # Calculate the lengths of the error bars relative to the mean
    lower_error = df['Mean'] - df['CI_Lower']
    upper_error = df['CI_Upper'] - df['Mean']
    lower_upper_error = [lower_error, upper_error]
    
    plt.barh(df['context_key'], df['Mean'], xerr=lower_upper_error, 
             color='skyblue', edgecolor='black', height=0.4)  # Set bar height to 0.4
    plt.yticks(rotation=0, fontsize=10)
    plt.xticks(fontsize=10)
    plt.ylabel('Context Key', fontsize=12)
    plt.xlabel('Probability of Affirmative Response', fontsize=12)
    plt.title(title, fontsize=14)
    plt.tight_layout()
    
    if group_name:
        file_name = f"{input_file_name}_{group_name.replace('/', '_').replace(' ', '_').lower()}_bar_chart.png"
    else:
        file_name = f"{input_file_name}_overall_bar_chart.png"
        
    plot_path = os.path.join(OUTPUT_DIR, file_name)
    plt.savefig(plot_path)
    plt.close()

def perform_analysis_decisions(DECISIONS_PATH, OUTPUT_DIR):
    df = pd.read_csv(DECISIONS_PATH)
    grouped_counts = df.groupby('context_key').apply(count_responses).reset_index()

    grouped_counts['Total_Responses'] = grouped_counts['Yes'] + grouped_counts['No']
    grouped_counts['Mean'] = grouped_counts['Yes'] / grouped_counts['Total_Responses']

    z_score = 1.96
    grouped_counts['Std_Error'] = np.sqrt((grouped_counts['Mean'] * (1 - grouped_counts['Mean'])) / grouped_counts['Total_Responses'])
    grouped_counts['CI_Lower'] = grouped_counts['Mean'] - z_score * grouped_counts['Std_Error']
    grouped_counts['CI_Upper'] = grouped_counts['Mean'] + z_score * grouped_counts['Std_Error']

    input_file_name = os.path.splitext(os.path.basename(DECISIONS_PATH))[0]
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    write_statistics_to_txt(grouped_counts, OUTPUT_DIR, input_file_name)
    
    plot_bar_chart(grouped_counts, 'Overall Probability of Affirmative Response', OUTPUT_DIR, input_file_name)
    
    groupings = {
        "Cost": ['cost_10', 'cost_10000'],
        "Possibility of deterrence": ['deter_impossible', 'deter_possible', 'deter_others_impossible', 'deter_others_possible'],
        "Future interaction": ['interaction_continuous', 'interaction_not_continuous'],
        "Legal implications": ['legal_implications', 'legal_implications_none'],
        "Offense recurrence": ['offense_will_not_recur', 'offense_will_recur', 'offense_will_recur_despite_punishment'],
        "Others' stance": ['others_ambivalent', 'others_do_not_want_punishment', 'others_want_punishment', 'others_will_not_punish', 'others_will_punish'],
        "Reputation": ['reputation_decrease', 'reputation_improve', 'reputation_same'],
        "Retaliation": ['retaliation_expected', 'retaliation_not_expected', 'grim_trigger', 'tit_for_tat'],
        "Target's status/support": ['target_has_high_status', 'target_has_low_status', 'target_has_supporters', 'target_no_supporters']
    }
    
    for group_name, context_keys in groupings.items():
        subset_df = grouped_counts[grouped_counts['context_key'].isin(context_keys)]
        plot_bar_chart(subset_df, f'Probability of Affirmative Response for {group_name}', OUTPUT_DIR, input_file_name, group_name)
