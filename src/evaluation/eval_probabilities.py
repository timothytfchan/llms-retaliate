import os
import pandas as pd

def eval_probabilities():
    COMPLETIONS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'completions', 'completions_decision.csv')
    PROBABILITIES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'probabilities_decision.csv')
    completions = pd.read_csv(COMPLETIONS_PATH)
    sorted_data = completions.sort_values(by=['scenario_id', 'context_key'])

    def save_probabilities(rows):
        df = pd.DataFrame(rows, columns=['scenario_id', 'context_key', 'probability'])
        df.to_csv(PROBABILITIES_PATH, mode='a', header=False, index=False)

    def get_last_processed_row():
        try:
            df = pd.read_csv(PROBABILITIES_PATH)
            return len(df)
        except FileNotFoundError:
            with open(PROBABILITIES_PATH, 'w') as f:
                f.write('scenario_id,context_key,probability\n')
            return 0

    start_row = get_last_processed_row()
    print(f'Starting from row {start_row}')
    
    for i in range(start_row, len(sorted_data)):
        row = sorted_data.iloc[i]
        scenario_id, context_key = row['scenario_id'], row['context_key']
        numerator, denominator = 0, 0

        for column in sorted_data.columns[2:]: # Skip scenario_id and context_key columns
            if row[column].lower() == 'yes':
                numerator += 1
                denominator += 1
            elif row[column].lower() == 'no':
                denominator += 1
            else:
                raise ValueError(f'Unexpected answer: {row[column]}')
        
        if denominator == 0:
            raise ValueError(f'Denominator is 0 for scenario {scenario_id} and context {context_key}')
        else:
            probability = numerator / denominator
            save_probabilities([(scenario_id, context_key, probability)])
    
    return PROBABILITIES_PATH