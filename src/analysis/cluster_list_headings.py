import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from ..utils.helper_functions import extract_pattern, get_embedding_with_retries

"""
Function imported from other file
-------------------------
def extract_pattern(text):
    expressions = re.findall(r'(\d+)\.\s([^:]+):', text)
    if not expressions:
        return [("N/A", "N/A")]
    return expressions
-------------------------
"""

def cluster_list_headings(COMPLETIONS_PATH, EMBEDDINGS_PATH, PLOT_PATH):
    # Load the data
    df = pd.read_csv(COMPLETIONS_PATH)
    
    # Extract number and list headings from tuples from completions, and with those, also include keys in new CSV file
    if not os.path.exists(EMBEDDINGS_PATH):
        df['extracted_tuples'] = df['completion'].apply(extract_pattern)
        flattened_data = []
        for _, row in df.iterrows():
            for tup in row['extracted_tuples']:
                flattened_data.append((row['scenario_id'], row['context_key'], tup[0], tup[1]))
        
        columns = ['scenario_id', 'context_key', 'number', 'text']
        df_embeddings = pd.DataFrame(flattened_data, columns=columns)        
        df_embeddings.to_csv(EMBEDDINGS_PATH, index=False)
    else:
        df_embeddings = pd.read_csv(EMBEDDINGS_PATH)
    
    # Get text embeddings for each list heading and save to the same CSV file
    df_embeddings['embedding'] = df_embeddings.text.apply(lambda x: get_embedding_with_retries(x, model='text-embedding-ada-002'))
    df_embeddings.to_csv(EMBEDDINGS_PATH, index=False)

    # Cluster using tSNE and color by context_key
    matrix = np.vstack(df_embeddings.embedding.values)
    n_clusters = 8

    kmeans = KMeans(n_clusters = n_clusters, init='k-means++', random_state=42)
    kmeans.fit(matrix)
    df['Cluster'] = kmeans.labels_
    
    # Save the plot to a PNG file
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='scenario_id', y='Cluster', hue='context_key', palette='tab10')
    plt.savefig(PLOT_PATH)

    return EMBEDDINGS_PATH, PLOT_PATH