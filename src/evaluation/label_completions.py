import os
import pandas as pd
import json
import string
import time
from typing import List
from ..utils.labeling_prompts import filter_to_labeling_prompt
from ..utils.helper_functions import chat_completion_with_retries

def label_completions(MODEL = 'gpt-4-0314', BATCH_SIZE = 10,
                      PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'processed', 'generated_prompts.csv'),
                      FILTER = "benefits_desc",
                      COMPLETIONS_PATH = None,
                      LABELS_PATH = None
                      ):
    if not LABELS_PATH:
        LABELS_PATH = COMPLETIONS_PATH.replace('completions', 'labels')
    
    # Read files into dataframes
    try:
        prompts = pd.read_csv(PROMPTS_PATH)
    except FileNotFoundError:
        print(f"Error: {PROMPTS_PATH} not found.")
        return
    
    try:
        completions = pd.read_csv(COMPLETIONS_PATH)
    except FileNotFoundError:
        print(f"Error: {COMPLETIONS_PATH} not found.")
        return

    # Merge both files on scenario_id, context_key, and question_key
    try:
        merged_data = pd.merge(prompts, completions, on=['scenario_id', 'context_key', 'question_key'])
    except:
        print("Error: Could not merge prompts and completions.")
        return
    filtered_data = merged_data[merged_data['question_key'] == FILTER]
    sorted_data = filtered_data.sort_values(by=['scenario_id', 'context_key'])

    def save_labels(rows):
        df = pd.DataFrame(rows, columns=['scenario_id', 'context_key', 'labels'])
        df.to_csv(LABELS_PATH, mode='a', header=False, index=False)

    def get_last_processed_row():
        try:
            df = pd.read_csv(LABELS_PATH)
            return len(df)
        except FileNotFoundError: # Create CSV file if it doesn't exist
            with open(LABELS_PATH, 'w') as f:
                f.write("scenario_id,context_key,labels\n")
            return 0

    # Parse the response text to get the JSON outputs
    def parse_json_output(response_text, remaining_alphabet):
        json_list = []
        for json_output, alpha in zip(response_text.split("\n---\n"), remaining_alphabet):
            if not json_output.startswith(f"JSON {alpha}:"): # Validate the JSON object
                break
            try:
                json_individual_output = json_output[len(f"JSON {alpha}:"):].strip()
            except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
                print(e)
                print("Error parsing JSON output:", json_output)
                json_individual_output = "{}"
            json_list.append(json_individual_output)
        json_labels = [json.dumps(json.loads(label)) for label in json_list]
        return json_labels

    # Get the last processed row number from the results CSV and determine the rows to process based on it
    start_row = get_last_processed_row()
    print(f"Starting from row {start_row}")
    to_process = sorted_data[start_row:]

    # Process in batches
    # Based on https://github.com/aypan17/machiavelli
    for i in range(0, len(to_process), BATCH_SIZE):
        batch = to_process[i:i+BATCH_SIZE]
        if (start_row+i)%100 == 0:
            print(f"Processing batch beginning row no. {start_row+i}")
        
        scenario_id_list = batch['scenario_id'].tolist()
        context_keys_list = batch['context_key'].tolist()
        prompts_list = batch['prompt'].tolist()
        completions_list = batch['completion'].tolist()
        samples = ["Question: " + question + "\n" + answer for question, answer in zip(prompts_list, completions_list)]

        num_fewshot = 3
        remaining_alphabet = string.ascii_uppercase[num_fewshot:]
        samples_text = "\n---\n".join([f"SAMPLE {alpha}:\n{sample}" for alpha, sample in zip(remaining_alphabet, samples)])
        messages = [{"role": "user", "content": filter_to_labeling_prompt[FILTER].format(samples_text)}]

        tstart = time.time()
        res = chat_completion_with_retries(model=MODEL, messages=messages)
        print("Batch evaluation time taken:", time.time() - tstart, flush=True)

        response_text = res["choices"][0]["message"]["content"] if res else ""
        json_labels = parse_json_output(response_text, remaining_alphabet)

        rows = zip(scenario_id_list, context_keys_list, json_labels)
        save_labels(rows)

    return LABELS_PATH