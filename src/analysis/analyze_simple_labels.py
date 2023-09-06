import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Reworked plotting function for better text alignment and visibility
def plot_heatmap(df, OUTPUT_DIR, output_filename, title, count_column, ci_lower_column, ci_upper_column):
    # Pivot the DataFrame to switch the axes
    df['count'].fillna(0, inplace=True)
    df['CI_Lower'].fillna(0, inplace=True)
    df['CI_Upper'].fillna(0, inplace=True)
    df_pivot = df.pivot("context_key", "labels", count_column).fillna(0)
    ci_lower_pivot = df.pivot("context_key", "labels", ci_lower_column).fillna(0)
    ci_upper_pivot = df.pivot("context_key", "labels", ci_upper_column).fillna(0)

    fig, ax = plt.subplots(figsize=(18, 12))
    cax = sns.heatmap(df_pivot, annot=False, fmt=".2f", linewidths=.5, cmap="YlGnBu", ax=ax, cbar_kws={'label': 'Count'})
    
    # Iterate through each cell to place the text
    for i, (idx, row) in enumerate(df_pivot.iterrows()):
        for j, (colname, value) in enumerate(row.iteritems()):
            ci_lower = ci_lower_pivot.loc[idx, colname]
            ci_upper = ci_upper_pivot.loc[idx, colname]
            
            # Determine text color based on cell value, which indirectly relates to its background color
            normed_value = (value - df_pivot.min().min()) / (df_pivot.max().max() - df_pivot.min().min())
            if normed_value > 0.5:  # high values are likely to have dark background
                text_color = 'white'
            else:
                text_color = 'black'
            
            # Place count text at the upper-middle part of the cell with adjusted font size
            ax.text(j + 0.5, i + 0.25, f"{value:.2f}", ha="center", va="center", fontsize=9, color=text_color)
            
            # Place confidence intervals at the lower-middle part of the cell with adjusted font size
            ax.text(j + 0.5, i + 0.75, f"({ci_lower:.2f}, {ci_upper:.2f})", ha="center", va="center", fontsize=9, color=text_color)
    
    plt.title(title)
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"{output_filename}.png"))
    #plt.show()

def perform_analysis_completions(LABELS_PATH, OUTPUT_DIR, title=None):
    df = pd.read_csv(LABELS_PATH)
    output_filename = os.path.basename(LABELS_PATH).replace('.csv', '')
    if not title:
        title = f'{output_filename}_heatmap_count.png'
    
    false_counts = df[df['labels'] == 'False'].groupby('context_key').size().reset_index(name='count')
    filtered_df = df[df['labels'] != 'False']
    combination_counts = filtered_df.groupby(['context_key', 'labels']).size().reset_index(name='count')
    
    all_bootstrap_counts = pd.DataFrame(columns=['context_key', 'labels', 'CI_Lower', 'CI_Upper'])

    for context_key in filtered_df['context_key'].unique():
        specific_group_df = filtered_df[filtered_df['context_key'] == context_key]
        
        bootstrap_samples = {label: [] for label in specific_group_df['labels'].unique()}
        
        for i in range(1000):
            bootstrap_sample = specific_group_df.sample(n=len(specific_group_df), replace=True, random_state=i)
            bootstrap_counts = bootstrap_sample['labels'].value_counts()
            
            for label in bootstrap_samples.keys():
                bootstrap_samples[label].append(bootstrap_counts.get(label, 0))
        
        for label, samples in bootstrap_samples.items():
            CI_Lower = np.percentile(samples, 2.5)
            CI_Upper = np.percentile(samples, 97.5)
            
            all_bootstrap_counts = all_bootstrap_counts.append({
                'context_key': context_key,
                'labels': label,
                'CI_Lower': CI_Lower,
                'CI_Upper': CI_Upper
            }, ignore_index=True)
    
    groupings = {
        "Cost": ['cost_10', 'cost_10000'],
        "Deterrence of target": ['deter_impossible', 'deter_possible'],
        "Deterrence of others": ['deter_others_impossible', 'deter_others_possible'],
        "Future interaction": ['interaction_continuous', 'interaction_not_continuous'],
        "Legal implications": ['legal_implications', 'legal_implications_none'],
        "Offense recurrence": ['offense_will_not_recur', 'offense_will_recur', 'offense_will_recur_despite_punishment'],
        "Default punishment": ['others_will_not_punish', 'others_will_punish'],
        "Others' stance": ['others_ambivalent', 'others_do_not_want_punishment', 'others_want_punishment'],
        "Reputation": ['reputation_decrease', 'reputation_improve', 'reputation_same'],
        "Retaliation": ['retaliation_expected', 'retaliation_not_expected'],
        "Retaliation strategy": ['grim_trigger', 'tit_for_tat', 'no_context'],
        "Target's status": ['target_has_high_status', 'target_has_low_status'],
        "Target's support": ['target_has_supporters', 'target_no_supporters']
    }
    """
    # Add "no_context" to each of the lists
    for key in groupings.keys():
        groupings[key].append("no_context")
    """
    non_overlapping_pairs = []
    # Check for non-overlapping intervals across different context_keys for the same label
    for label in filtered_df['labels'].unique():
        label_bootstrap_counts = all_bootstrap_counts[all_bootstrap_counts['labels'] == label]
        for i, row1 in label_bootstrap_counts.iterrows():
            for j, row2 in label_bootstrap_counts.iterrows():
                if i >= j:  # Skip duplicate and self comparisons
                    continue
                
                # Check if intervals overlap
                if row1['CI_Upper'] <= row2['CI_Lower'] or row2['CI_Upper'] <= row1['CI_Lower']:
                    context_key1 = row1['context_key']
                    context_key2 = row2['context_key']

                    direction = None
                    if row1['CI_Upper'] <= row2['CI_Lower']:
                        direction = "<="
                    else:
                        direction = ">="
                    
                    # Check if the pair is meaningful
                    for group in groupings.values():
                        if context_key1 in group and context_key2 in group:
                            non_overlapping_pairs.append((label, context_key1, context_key2, direction))
                            break
    
    combination_counts = pd.merge(combination_counts, all_bootstrap_counts, on=['context_key', 'labels'], how='outer')
    combination_counts[['count', 'CI_Lower', 'CI_Upper']] = combination_counts[['count', 'CI_Lower', 'CI_Upper']].fillna(0)
    """
    context_total = combination_counts.groupby('context_key')['count'].transform('sum')
    combination_counts['context_normalized'] = (combination_counts['count'] / context_total) * 100
    
    label_total = combination_counts.groupby('labels')['count'].transform('sum')
    combination_counts['label_normalized'] = (combination_counts['count'] / label_total) * 100
    
    # Normalize confidence intervals by context_key
    df['CI_Lower_context_normalized'] = (df['CI_Lower'] / df['context_total']) * 100
    df['CI_Upper_context_normalized'] = (df['CI_Upper'] / df['context_total']) * 100
    
    # Normalize confidence intervals by labels
    df['CI_Lower_label_normalized'] = (df['CI_Lower'] / df['label_total']) * 100
    df['CI_Upper_label_normalized'] = (df['CI_Upper'] / df['label_total']) * 100
    """

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    csv_file_path = os.path.join(OUTPUT_DIR, f'{output_filename}_statistical_analysis.csv')
    combination_counts.to_csv(csv_file_path, index=False)

    # Write the non-overlapping pairs to a text file
    txt_file_path = os.path.join(OUTPUT_DIR, f'{output_filename}_non_overlapping_pairs.txt')
    with open(txt_file_path, 'w') as f:
        for label, context_key1, context_key2, direction in non_overlapping_pairs:
            f.write(f"Label: {label}, Context Keys: {context_key1} {direction} {context_key2}\n")
    
    # Adding the heatmap plots
    plot_heatmap(combination_counts, OUTPUT_DIR, output_filename, title, 'count', 'CI_Lower', 'CI_Upper')
    #plot_heatmap(combination_counts, OUTPUT_DIR, 'heatmap_context_normalized.png', 'Context-Normalized Counts with 95% CI', 'context_normalized', 'CI_Lower_context_normalized', 'CI_Upper_context_normalized')
    #plot_heatmap(combination_counts, OUTPUT_DIR, 'heatmap_label_normalized.png', 'Label-Normalized Counts with 95% CI', 'label_normalized', 'CI_Lower_label_normalized', 'CI_Upper_label_normalized')