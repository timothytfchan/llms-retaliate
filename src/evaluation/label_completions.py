import os
import pandas as pd
import json
import string
import time
from typing import List
from ..utils.labeling_prompts import labeling_prompts
from ..utils.helper_functions import chat_completion_with_retries, save_labels, get_last_processed_row

def label_completions(COMPLETIONS_PATH,
                      MODEL = 'gpt-4-0314', BATCH_SIZE = 10,
                      PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'processed', 'generated_prompts.csv'),
                      LABELING_PROMPT_FILTER = "benefits_desc",
                      LABELS_PATH = None
                      ):
    # Generate LABELS_PATH from COMPLETIONS_PATH if not provided
    try:
        if not LABELS_PATH:
            dir_path, filename = os.path.split(COMPLETIONS_PATH) # Split off the filename
            parent_dir, tail = os.path.split(dir_path) # Split the directory path to get the parent directory and the 'completions' part
            tail = 'labels'  # Replace 'completions' with 'labels'
            LABELS_PATH = os.path.join(parent_dir, tail, filename) # Join everything back together
    except:
        print("Error: Invalid COMPLETIONS_PATH path.")
        return
    
    # Read the prompts (questions) and completions (answers) CSV files
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

    # Filter for questions used in evaluation with the LABELING_PROMPT_FILTER
    try:
        prompts = prompts[prompts['question_key'] == LABELING_PROMPT_FILTER]
    except:
        print(f"Error: Could not filter prompts by {LABELING_PROMPT_FILTER}.")
        return

    # Merge question and answer files on scenario_id and context_key
    try:
        merged_data = pd.merge(prompts, completions, on=['scenario_id', 'context_key'])
    except:
        print("Error: Could not merge prompts and completions.")
        return
    sorted_data = merged_data.sort_values(by=['scenario_id', 'context_key'])

    # Define a function to parse the batched response text to get the JSON outputs
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

    # Get the last processed row number from the results CSV and determine the first row to process based on it
    start_row = get_last_processed_row(path=LABELS_PATH, default_header="scenario_id,context_key,labels\n")
    print(f"Starting from row {start_row}")
    to_process = sorted_data[start_row:]

    # Process in batches, based on https://github.com/aypan17/machiavelli
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
        messages = [{"role": "user", "content": labeling_prompts[LABELING_PROMPT_FILTER].format(samples_text)}]

        tstart = time.time()
        res = chat_completion_with_retries(model=MODEL, messages=messages)
        print("Batch evaluation time taken:", time.time() - tstart, flush=True)

        response_text = res["choices"][0]["message"]["content"] if res else ""
        json_labels = parse_json_output(response_text, remaining_alphabet)

        rows = list(zip(scenario_id_list, context_keys_list, json_labels))
        save_labels(path=LABELS_PATH, rows=rows, columns=['scenario_id', 'context_key', 'labels'], mode='a', header=False)

    return LABELS_PATH