import os
import pandas as pd
import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Load the CSV file into a dataframe
df = pd.read_csv('/path_to_your_file/benefits_desc_gpt-3.5-turbo-0301.csv')

# Extract the expressions from the 'completion' column
df['extracted_patterns'] = df['completion'].apply(lambda x: re.findall(r'\d+\.\s[^:]+:', x))

# Filter only the rows where the regular expression extraction worked
rows_with_patterns_df = df[df['extracted_patterns'].str.len() > 0]

# Preprocess the extracted patterns
def preprocess_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text).strip().lower()

rows_with_patterns_df['cleaned_patterns'] = rows_with_patterns_df['extracted_patterns'].apply(lambda patterns: ' '.join([preprocess_text(pattern) for pattern in patterns]))

# Remove stop words from the cleaned patterns
rows_with_patterns_df['cleaned_patterns_without_stopwords'] = rows_with_patterns_df['cleaned_patterns'].apply(lambda text: ' '.join([word for word in text.split() if word not in ENGLISH_STOP_WORDS]))

# Calculate word frequencies by context_key for these rows after removing stop words
word_freq_by_context_without_stopwords = rows_with_patterns_df.groupby('context_key')['cleaned_patterns_without_stopwords'].apply(' '.join).apply(lambda x: Counter(x.split()))

# Get the top 10 most common words for each context_key after removing stop words
top_10_words_by_context_without_stopwords = word_freq_by_context_without_stopwords.apply(lambda counter: [word for word, _ in sorted(counter.items(), key=lambda x: x[1], reverse=True)[:10]])

# Convert the Series to DataFrame for export to CSV
export_df_without_stopwords = top_10_words_by_context_without_stopwords.reset_index()
export_df_without_stopwords.columns = ['context_key', 'top_10_words']
export_df_without_stopwords['top_10_words'] = export_df_without_stopwords['top_10_words'].apply(', '.join)

# Save the dataframe to a CSV file
export_df_without_stopwords.to_csv('/path_where_you_want_to_save/top_10_words_by_context_without_stopwords.csv', index=False)
