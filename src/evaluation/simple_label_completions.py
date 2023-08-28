import os
import pandas as pd
from ..utils.labeling_prompts import labeling_prompts
from ..utils.helper_functions import chat_completion_with_retries, save_labels, get_last_processed_row

def simple_label_completions(EMBEDDINGS_PATH,
                             MODEL = 'gpt-3.5-turbo-0301',
                             LABELING_PROMPT_FILTER = "simple_methods",
                             LABELS_PATH = None,
                             acceptable_answers = None
                             ):
    # Generate LABELS_PATH from EMBEDDINGS_PATH if not provided
    try:
        if not LABELS_PATH:
            dir_path, filename = os.path.split(EMBEDDINGS_PATH) # Split off the filename
            parent_dir, tail = os.path.split(dir_path) # Split the directory path to get the parent directory and the 'embeddings' part
            tail = 'labels'  # Replace 'embeddings' with 'labels'
            LABELS_PATH = os.path.join(parent_dir, tail, filename) # Join everything back together
    except:
        print("Error: Invalid EMBEDDINGS_PATH path.")
        return

    # Load and sort extracted completions
    try:
        completions = pd.read_csv(EMBEDDINGS_PATH)
    except FileNotFoundError:
        print(f"Error: {EMBEDDINGS_PATH} not found.")
        return

    completions = completions.drop(columns=['embedding'])
    completions = completions.sort_values(by=['scenario_id', 'context_key', 'split_index'])

    # Set acceptable answers if not provided
    if not acceptable_answers:
        acceptable_answers = ["Use the legal system or law enforcement", "Involve other authorities outside legal system", "Public shaming or damage reputation",
                              "Other social or interpersonal consequences", "Communicate, confront, or seek apology", "Physical violence or revenge",
                              "Financial or professional consequences", "Mediation or arbitration", "Education or community service",
                              "Forgiveness or restorative justice", "None of the above"]
        acceptable_answers_joined = '"' + '",\n"'.join(acceptable_answers) + '"'

    # Parse output for answer
    def parse_output_for_answer(output):
        # Try to find <answer></answer> tags in output
        try:
            answer = output.split("<answer>")[1].split("</answer>")[0]
            included_answers = []
            for acceptable_answer in acceptable_answers:
                if acceptable_answer in answer:
                    included_answers.append(acceptable_answer)
            if len(included_answers) == 1:
                return included_answers[0]
        except:
            pass
        
        # Check if the output contains any of the acceptable answers
        included_answers = []
        for acceptable_answer in acceptable_answers:
            if acceptable_answer in output:
                included_answers.append(acceptable_answer)
        if len(included_answers) == 1:
            return included_answers[0]
        else:
            return False

    # Get answer from completion
    def get_answer(scenario_id, context_key, split_index, completion):
        content = labeling_prompts(LABELING_PROMPT_FILTER).format(acceptable_answers_joined = acceptable_answers_joined, samples_text=completion)
        messages = [{"role": "user", "content": content}]
        res = chat_completion_with_retries(model=MODEL, messages=messages, temperature=0.3, validation_fn=parse_output_for_answer)
        response_text = res["choices"][0]["message"]["content"] if res else ""
        extracted_answer = parse_output_for_answer(response_text)
        save_labels(path=LABELS_PATH, rows=[[scenario_id, context_key, split_index, response_text, str(extracted_answer)]], 
                    columns=['scenario_id', 'context_key', 'split_index', 'response_text', 'labels'], mode='a', header=False)

    # Get the last processed row number from the results CSV and determine the first row to process based on it
    start_row = get_last_processed_row(path=LABELS_PATH, default_header="scenario_id,context_key,split_index,response_text,labels\n")
    completions = completions[start_row:]
    
    # Process every row
    for _, row in completions.iterrows():
        get_answer(scenario_id=row['scenario_id'], context_key=row['context_key'], split_index=row['split_index'], completion=row['completion'])

    return LABELS_PATH