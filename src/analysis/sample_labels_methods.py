import os
import pandas as pd

# Read CSV files
df1_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'benefits_desc_follow_up_gpt-3.5-turbo-0301.csv'))
df2_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'benefits_pres_follow_up_gpt-3.5-turbo-0301.csv'))
df3_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'benefits_desc_follow_up_gpt-4-0314.csv'))
df4_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'benefits_pres_follow_up_gpt-4-0314.csv'))

df5_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'methods_desc_gpt-3.5-turbo-0301.csv'))
df6_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'methods_pres_gpt-3.5-turbo-0301.csv'))
df7_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'methods_desc_gpt-4-0314.csv'))
df8_labels = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'methods_pres_gpt-4-0314.csv'))

df1_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'benefits_desc_follow_up_gpt-3.5-turbo-0301.csv'))
df2_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'benefits_pres_follow_up_gpt-3.5-turbo-0301.csv'))
df3_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'benefits_desc_follow_up_gpt-4-0314.csv'))
df4_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'benefits_pres_follow_up_gpt-4-0314.csv'))

df5_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'methods_desc_gpt-3.5-turbo-0301.csv'))
df6_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'methods_pres_gpt-3.5-turbo-0301.csv'))
df7_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'methods_desc_gpt-4-0314.csv'))
df8_embeddings = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'methods_pres_gpt-4-0314.csv'))

# Process prompts df
df_prompts = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'processed', 'generated_prompts.csv'))
df_prompts.drop('player_a', axis=1, inplace=True)
df_prompts.drop('player_b', axis=1, inplace=True)

# Process labels dfs
df1_labels['question_key'] = 'methods_desc'
df2_labels['question_key'] = 'methods_pres'
df3_labels['question_key'] = 'methods_desc'
df4_labels['question_key'] = 'methods_pres'

df5_labels['question_key'] = 'methods_desc'
df6_labels['question_key'] = 'methods_pres'
df7_labels['question_key'] = 'methods_desc'
df8_labels['question_key'] = 'methods_pres'

labels_df = pd.concat([df1_labels, df2_labels, df3_labels, df4_labels, df5_labels, df6_labels, df7_labels, df8_labels], ignore_index=True)
labels_df.drop('response_text', axis=1, inplace=True)

# Process embeddings dfs
# strictly there is no question_key for the follow-up, but method_desc and method_pres matches to the same sort of question
df1_embeddings['question_key'] = 'methods_desc' 
df2_embeddings['question_key'] = 'methods_pres'
df3_embeddings['question_key'] = 'methods_desc'
df4_embeddings['question_key'] = 'methods_pres'

df5_embeddings['question_key'] = 'methods_desc'
df6_embeddings['question_key'] = 'methods_pres'
df7_embeddings['question_key'] = 'methods_desc'
df8_embeddings['question_key'] = 'methods_pres'

df1_embeddings.drop('embedding', axis=1, inplace=True)
df2_embeddings.drop('embedding', axis=1, inplace=True)
df3_embeddings.drop('embedding', axis=1, inplace=True)
df4_embeddings.drop('embedding', axis=1, inplace=True)

df5_embeddings.drop('embedding', axis=1, inplace=True)
df6_embeddings.drop('embedding', axis=1, inplace=True)
df7_embeddings.drop('embedding', axis=1, inplace=True)
df8_embeddings.drop('embedding', axis=1, inplace=True)

embeddings_df = pd.concat([df1_embeddings, df2_embeddings, df3_embeddings, df4_embeddings, df5_embeddings, df6_embeddings, df7_embeddings, df8_embeddings], ignore_index=True)

# Merge dataframes to include embeddings and original prompts
merged_df_2 = pd.merge(embeddings_df, labels_df, how='right', on=['scenario_id', 'context_key', 'question_key', 'split_index'])
df = pd.merge(df_prompts, merged_df_2, how='right', on=['scenario_id', 'context_key', 'question_key'])

# Sample for each class
df_samples = pd.DataFrame(columns=df.columns)

acceptable_answers = ["Use the legal system or law enforcement", "Involve other authorities outside legal system", "Public shaming or damage reputation",
                      "Other social or interpersonal consequences", "Communicate, confront, or seek apology", "Physical violence or revenge",
                      "Financial or professional consequences", "Mediation or arbitration", "Education or community service",
                      "Forgiveness or restorative justice", "None of the above"]

for answer in acceptable_answers:
    sample = df[df['labels'] == answer]
    if len(sample) >= 30:
        sample = sample.sample(n=30, random_state=30)
    else:
        sample = sample.sample(n=len(sample), random_state=30)
    
    df_samples = pd.concat([df_samples, sample]).reset_index(drop=True)

# Randomize order
df_samples = df_samples.sample(frac=1, random_state=30).reset_index(drop=True)

# Save to CSV
df_samples.to_csv(os.path.join(os.path.dirname(__file__), '..', '..', 'labels', 'methods_samples.csv'), index=False)