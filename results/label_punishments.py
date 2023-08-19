import json
import csv
import pandas as pd
import os
from eval_punishments_prompt import get_punishment_labels 
#get_punishment_labels(model, questions: List[str], answers: List[str], temperature, retry_interval_sec: int = 20)

# Load both files
prompts = pd.read_csv('generated_prompts.csv')
results = pd.read_csv('results.csv')

# Merge both files on scenario_id, context_key, and question_key
merged_data = pd.merge(prompts, results, on=['scenario_id', 'context_key', 'question_key'])

# Function to process 10 rows at a time for the same scenario_id
def process_rows(group):
    # Iterate through the group, 10 rows at a time
    for i in range(0, len(group), 10):
        subset = group.iloc[i:i+10]
        current_scenario_id = subset['scenario_id'].iloc[0]
        prompts_list = subset['prompt'].tolist()
        responses_list = subset['response'].tolist()
        context_keys_list = subset['context_key'].tolist()
        question_keys_list = subset['question_key'].tolist()
        # Call labeling function with the two lists
        try:
            json_list, _, _ = get_punishment_labels("gpt-4-0314", prompts_list, responses_list)
            # Write current_scenario_id, context_key_list, question_key_list, and json_list to a CSV file
            with open('methods_of_punishment_labels.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                for context_key, question_key, json_obj in zip(context_keys_list, question_keys_list, json_list):
                    writer.writerow([current_scenario_id, context_key, question_key, json.dumps(json_obj)])
        except:
            print("Error labeling scenario_id: ", subset['scenario_id'].iloc[0], " with prompts: ", prompts_list)
    
    # Save progress by current_scenario_id
    with open('methods_of_punishment_labels_progress.txt', 'w') as f:
        f.write(str(current_scenario_id))

# Create CSV file if it doesn't exist
if not os.path.exists('methods_of_punishment_labels.csv'):
    with open('methods_of_punishment_labels.csv', 'w') as f:
        f.write("scenario_id,context_key,question_key,labels\n")

#Filter for methods_of_punishments
filtered_data = merged_data[merged_data['question_key'] == 'methods_of_punishment']

# Read last processed scenario_id from progress file
last_processed_scenario_id = None
if os.path.exists('methods_of_punishment_labels_progress.txt'):
    with open('methods_of_punishment_labels_progress.txt', 'r') as f:
        last_processed_scenario_id = f.readline().strip()

# If last_processed_scenario_id exists, convert it to the appropriate type
if last_processed_scenario_id:
    last_processed_scenario_id = int(last_processed_scenario_id)  # or float, depending on the data type

# Filter scenarios that have been processed already
if last_processed_scenario_id:
    filtered_data = filtered_data[filtered_data['scenario_id'] > last_processed_scenario_id]

# Group by scenario_id and apply the function
filtered_data.groupby('scenario_id').apply(process_rows)