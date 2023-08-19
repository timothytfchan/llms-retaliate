import os
import pandas as pd
import json

def generate_prompts(SCENARIOS_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'raw', 'scenarios.csv'), 
                     CONTEXT_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'raw', 'additional_context.json'), 
                     QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'raw', 'questions.json')):
    try:
        scenarios = pd.read_csv(SCENARIOS_PATH)
    except (FileNotFoundError, pd.errors.ParserError):
        print(f"Error: {SCENARIOS_PATH} not found or invalid CSV.")
        return

    try:
        with open(CONTEXT_PATH) as f: context_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: {CONTEXT_PATH} not found or invalid JSON.")
        return

    try:
        with open(QUESTIONS_PATH) as f: questions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: {QUESTIONS_PATH} not found or invalid JSON.")
        return

    generated_prompts = []

    for idx, row in scenarios.iterrows():
        scenario = row['scenario']
        player_a = row['player_a']
        player_b = row['player_b']
        scenario_id = row['ID']
        
        # Loop over each entry in the additional_context JSON data and replace placeholders
        for context_key, context_value in context_data.items():
            context_filled = context_value.format(player_a=player_a, player_b=player_b)
            
            # Loop over each entry in the questions JSON data and replace placeholders
            for question_key, question_value in questions.items():
                question_filled = question_value.format(player_a=player_a, player_b=player_b)
                
                # Form the final prompt
                if context_key != "no_context":
                    prompt = f"{scenario} We know for certain that {context_filled} {question_filled}"
                else:
                    prompt = f"{scenario} {question_filled}"

                # Append the ID, context key, question key, and prompt to the list
                generated_prompts.append([scenario_id, context_key, question_key, player_a, player_b, prompt])

    # Convert the list to a DataFrame and write the DataFrame to a CSV file
    prompts_df = pd.DataFrame(generated_prompts, columns=['scenario_id', 'context_key', 'question_key', 'player_a', 'player_b', 'prompt'])
    PROMPTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'processed', 'generated_prompts.csv')
    prompts_df.to_csv(PROMPTS_PATH, index=False)

    return PROMPTS_PATH