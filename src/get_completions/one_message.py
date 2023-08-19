import os
import pandas as pd
from ..utils.helper_functions import chat_completion_with_retries, save_labels, get_last_processed_row

def get_completions(MODEL = 'gpt-4-0314',
                    TEMPERATURE = 0,
                    FILTER = 'benefits_desc',
                    PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'processed', 'generated_prompts.csv'),
                    COMPLETIONS_PATH = None):
    # If COMPLETIONS_PATH is not provided, generate it using the FILTER and MODEL name
    if not COMPLETIONS_PATH:
        COMPLETIONS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'completions', f'{FILTER}_{MODEL}.csv')

    try:
        prompts = pd.read_csv(PROMPTS_PATH)
    except FileNotFoundError:
        print(f"Error: File {PROMPTS_PATH} not found.")
        return
    filtered_prompts = prompts[prompts['question_key'] == FILTER]
    sorted_prompts = filtered_prompts.sort_values(by=['scenario_id', 'context_key'])
    
    # Get and save a completion by creating a one row dataframe and appending it to the csv file.
    # For loop over the sorted_prompts dataframe.
    # Save the completion by appending to the csv file.
    last_processed_row = get_last_processed_row(COMPLETIONS_PATH, "scenario_id,context_key,completion\n")
    for i, row in sorted_prompts.iloc[last_processed_row:].iterrows(): # For each prompt
        scenario_id, context_key, PROMPT = row['scenario_id'], row['context_key'], row['prompt']
        messages = [{"role": "user", "content": PROMPT}]
        res = chat_completion_with_retries(model=MODEL, messages=messages, temperature=TEMPERATURE)
        response_text = res["choices"][0]["message"]["content"] if res else ""
        save_labels(COMPLETIONS_PATH, rows=[[scenario_id, context_key, response_text]], columns=['scenario_id', 'context_key', 'completion'], mode='a', header=False)
    
    print(f"Finished running file {os.path.dirname(__file__)} for {MODEL}.")
    return COMPLETIONS_PATH