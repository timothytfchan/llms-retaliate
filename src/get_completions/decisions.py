import os
import pandas as pd
from ..utils.helper_functions import chat_completion_with_retries, save_labels, get_last_processed_row

def get_completions_decision(MODEL = 'gpt-4-0314',
                             PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'processed', 'generated_prompts.csv'),
                             FILTER = 'decisions_desc',
                             COMPLETIONS_PATH = None,
                             NUM_SAMPLES = 20):
    # If COMPLETIONS_PATH is not provided, generate it using the MODEL name
    if not COMPLETIONS_PATH:
        COMPLETIONS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'completions', f'{FILTER}_{MODEL}.csv')

    TEMPERATURE = 1 # Temperature 1 for estimation of the distribution of the next token.
    sample_columns = [f'sample_{i}' for i in range(NUM_SAMPLES)] # Token will be sampled sample_column times.

    try:
        prompts = pd.read_csv(PROMPTS_PATH)
    except FileNotFoundError:
        print(f"Error: File {PROMPTS_PATH} not found.")
        return
    filtered_prompts = prompts[prompts['question_key'] == FILTER]
    sorted_prompts = filtered_prompts.sort_values(by=['scenario_id', 'context_key'])
    
    # Get and save completions by creating a one row dataframe and appending it to the csv file.
    # For loop over the sorted_prompts dataframe. Then, inside the loop, for each prompt, get NUM_SAMPLES completions.
    # Save the completions by appending to the csv file.
    last_processed_row = get_last_processed_row(COMPLETIONS_PATH, f"scenario_id,context_key,{','.join(sample_columns)}\n")
    for i, row in sorted_prompts.iloc[last_processed_row:].iterrows(): # For each prompt
        scenario_id, context_key, PROMPT = row['scenario_id'], row['context_key'], row['prompt']
        new_row = [scenario_id, context_key]
        messages = [{"role": "user", "content": PROMPT}]
        for j in range(NUM_SAMPLES): # Get NUM_SAMPLES completions
            res = chat_completion_with_retries(model=MODEL, messages=messages, temperature=TEMPERATURE, max_tokens=1)
            response_text = res["choices"][0]["message"]["content"] if res else ""
            new_row.append(response_text)
        save_labels(COMPLETIONS_PATH, rows=[new_row], columns=['scenario_id', 'context_key'] + sample_columns, mode='a', header=False)
    
    print(f"Finished running file {os.path.dirname(__file__)} for {MODEL}.")

    return COMPLETIONS_PATH