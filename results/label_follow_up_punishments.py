import pandas as pd
import os
import time
from eval_punishments_prompt import get_punishment_labels

# Load both files
prompts = pd.read_csv('generated_prompts.csv')
results = pd.read_csv('results/results_follow_up.csv')

# Merge both files on scenario_id, context_key, and question_key, then sort by those columns
merged_data = pd.merge(prompts, results, on=['scenario_id', 'context_key', 'question_key'])
sorted_data = merged_data.sort_values(by=['scenario_id', 'context_key', 'question_key'], ascending=True)

# Load or create the labels DataFrame
model = "gpt-4-0314"
labels_file_name = f"analysis/{model}_follow_up_punishment_labels.csv"
if os.path.exists(labels_file_name):
    df_labels = pd.read_csv(labels_file_name)
else:
    df_labels = pd.DataFrame(columns=['scenario_id', 'context_key', 'question_key', 'labels'])
    df_labels.to_csv(labels_file_name, index=False)
start_row = df_labels.shape[0]

previous_scenario = None
chunk = []

# Iterate through the sorted data
for index, row in sorted_data.iterrows():
    if index < start_row:
        continue
    scenario_id = row['scenario_id']

    # If the scenario_id changes or the chunk size reaches 10, process the current chunk
    if chunk and ((previous_scenario != scenario_id) or (len(chunk) == 10)):
        scenario_ids, context_keys, question_keys, prompts, responses = zip(*chunk)
        labels, _, __ = get_punishment_labels(model, prompts, responses)

        # Create a dataframe for the results and then append to the labels csv file
        if labels:
            row_df = pd.DataFrame({
                'scenario_id': scenario_ids,
                'context_key': context_keys,
                'question_key': question_keys,
                'labels': labels
                })
            row_df.to_csv(labels_file_name, mode='a', header=False, index=False)
        else:
            print(f"Error. Index: {index}")
        # Reset the chunk after processing
        chunk = []

    # Add the current row to the chunk and update the scenario
    chunk.append((row['scenario_id'], row['context_key'], row['question_key'], row['prompt'], row['response']))
    previous_scenario = scenario_id

# Process any remaining rows in the last chunk
if chunk:
    scenario_ids, context_keys, question_keys, prompts, responses = zip(*chunk)
    labels, _, __ = get_punishment_labels(model, prompts, responses)
    if labels:
        row_df = pd.DataFrame({
            'scenario_id': scenario_ids,
            'context_key': context_keys,
            'question_key': question_keys,
            'labels': labels
            })
        row_df.to_csv(labels_file_name, mode='a', header=False, index=False)
    else:
        print(f"Error. Index: {index}")

print("Done!")