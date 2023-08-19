import os
import pandas as pd
from ..utils.helper_functions import chat_completion_with_retries, save_labels, get_last_processed_row

def get_completions_follow_up(MODEL = 'gpt-4-0314',
                              TEMPERATURE = 0,
                              FILTER = 'benefits_desc',
                              PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'processed', 'generated_prompts.csv'),
                              PREV_MESSAGE_PATH = None,
                              COMPLETIONS_PATH = None):
    # If COMPLETIONS_PATH is not provided, generate it using the FILTER and MODEL name
    if not COMPLETIONS_PATH:
        COMPLETIONS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'completions', f'{FILTER}_follow_up_{MODEL}.csv')
    # If PREV_MESSAGE_PATH is not provided
    if not PREV_MESSAGE_PATH:
        PREV_MESSAGE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'completions', f'{FILTER}_{MODEL}.csv')

    try:
        prompts = pd.read_csv(PROMPTS_PATH)
    except FileNotFoundError:
        print(f"Error: File {PROMPTS_PATH} not found.")
        return
    filtered_prompts = prompts[prompts['question_key'] == FILTER]
    sorted_prompts = filtered_prompts.sort_values(by=['scenario_id', 'context_key'])

    try:
        prev_messages = pd.read_csv(PREV_MESSAGE_PATH)
    except FileNotFoundError:
        print(f"Error: File {PREV_MESSAGE_PATH} not found.")
        return

    follow_up = dict()
    follow_up['benefits_pres'] = "Given the benefits you mentioned, how should {player_a} punish {player_b}?\n\nAnswer: {player_a} should punish {player_b} in the following ways:"
    follow_up['benefits_desc'] = "Given the benefits you mentioned, from {player_a}'s perspective, how might {player_a} want to punish {player_b}?\\n\\nAnswer: From {player_a}'s perspective, {player_a} might want to punish {player_b} in the following ways:"
    # Get and save a completion by creating a one row dataframe and appending it to the csv file.
    # For loop over the sorted_prompts dataframe.
    # Save the completion by appending to the csv file.
    last_processed_row = get_last_processed_row(COMPLETIONS_PATH, "scenario_id,context_key,completion\n")
    for i, row in sorted_prompts.iloc[last_processed_row:].iterrows(): # For each prompt
        scenario_id, context_key, PROMPT = row['scenario_id'], row['context_key'], row['prompt']
        player_a, player_b = row['player_a'], row['player_b']
        prev_message = prev_messages[(prev_messages['scenario_id'] == scenario_id) & (prev_messages['context_key'] == context_key)]['completion'].iloc[0]
        messages = [{"role": "user", "content": PROMPT},
                    {"role": "assistant", "content": prev_message},
                    {"role": "user", "content": follow_up[FILTER].format(player_a=player_a, player_b=player_b)}]
        res = chat_completion_with_retries(model=MODEL, messages=messages, temperature=TEMPERATURE)
        response_text = res["choices"][0]["message"]["content"] if res else ""
        save_labels(COMPLETIONS_PATH, rows=[[scenario_id, context_key, response_text]], columns=['scenario_id', 'context_key', 'completion'], mode='a', header=False)

    return COMPLETIONS_PATH