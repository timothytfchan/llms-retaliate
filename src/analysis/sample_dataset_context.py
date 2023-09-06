import os
import pandas as pd
from typing import Dict, List, Mapping, Optional

def sample_dataset_context(PROMPTS_PATH: str, ITEMS_PATH: str, LABELS_PATH: str, OUTPUT_PATH: str, question_key: str, contexts: List):
    # Read CSV files
    df_prompts = pd.read_csv(PROMPTS_PATH)
    if 'player_a' in df_prompts.columns:
        df_prompts.drop('player_a', axis=1, inplace=True)
    if 'player_b' in df_prompts.columns:
        df_prompts.drop('player_b', axis=1, inplace=True)

    df_items = pd.read_csv(ITEMS_PATH)
    if 'embedding' in df_items.columns:
        df_items.drop('embedding', axis=1, inplace=True)
    
    df_labels = pd.read_csv(LABELS_PATH)
    if 'response_text' in df_labels.columns:
        df_labels.drop('response_text', axis=1, inplace=True)

    # Process labels df
    df_labels['question_key'] = question_key

    # Process items df
    df_items['question_key'] = question_key

    # Merge dataframes to include items and original prompts
    df = pd.merge(df_items, df_labels, how='right', on=['scenario_id', 'context_key', 'question_key', 'split_index'])
    df = pd.merge(df_prompts, df, how='right', on=['scenario_id', 'context_key', 'question_key'])

    # Subset df to only include rows where context_key values are in the contexts list
    df_samples = df[df['context_key'].isin(contexts)]

    """
    # Sample for each class
    df_samples = pd.DataFrame(columns=df.columns)

    acceptable_answers = ["Retribution and emotional or personal satisfaction",
                        "Other emotional benefits",
                        "Empowerment of the punisher",
                        "Deterrence and preventing future issues",
                        "Financial compensation and restitution",
                        "Improving reputation, gaining respect, and asserting authority",
                        "Ensures or upholds principles (fairness etc.)",
                        "None of the above"]

    for answer in acceptable_answers:
        sample = df[df['labels'] == answer]
        if len(sample) >= 30:
            sample = sample.sample(n=30, random_state=30)
        else:
            sample = sample.sample(n=len(sample), random_state=30)
        
        df_samples = pd.concat([df_samples, sample]).reset_index(drop=True)
    """
    # Randomize order
    df_samples = df_samples.sample(frac=1, random_state=30).reset_index(drop=True)
    
    # Save to CSV
    df_samples.to_csv(OUTPUT_PATH, index=False)