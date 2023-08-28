import os
import numpy as np
import pandas as pd
import ast
from sklearn.cluster import KMeans
import joblib

def read_and_concatenate_csvs(PATHS):
    """Reads multiple CSV files, concatenates them, and keeps track of the source of each row."""
    dataframes = []
    for idx, PATH in enumerate(PATHS):
        df = pd.read_csv(PATH, converters= {'embedding': ast.literal_eval})
        df['source'] = idx  # add a column to track the original file
        dataframes.append(df)
        print("Finished reading", PATH)
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

def apply_kmeans_on_combined(df, n_clusters_list, random_state):
    """Applies KMeans clustering on the combined dataframe's 'embedding' column for multiple n_clusters values
    and returns the corresponding models."""
    
    matrix = np.vstack(df.embedding.values)
    kmeans_models = []
    
    for n_clusters in n_clusters_list:
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init = 20, random_state=random_state)
        cluster_col_name = f'{n_clusters}_clusters'
        kmeans.fit(matrix)
        df[cluster_col_name] = kmeans.labels_
        kmeans_models.append(kmeans)
    
    return df, kmeans_models

def split_and_write(df, CLUSTER_DIR, original_paths, kmeans_models_list, n_clusters_list, CLUSTER_MODELS_DIR=None):
    """Splits the dataframe based on the source column and writes to separate CSV files."""
    output_paths = []
    model_paths = []
    for source, group in df.groupby('source'):
        # Remove the source column and write to CSV
        del group['source']
        output_path = os.path.join(CLUSTER_DIR, f"{os.path.basename(original_paths[int(source)])}")
        group.to_csv(output_path, index=False)
        output_paths.append(output_path)

        if CLUSTER_MODELS_DIR:
            for n_clusters, kmeans_model in zip(n_clusters_list, kmeans_models_list):
                # Get the filename without the extension and use it for the model filename
                filename_without_ext = os.path.splitext(os.path.basename(output_path))[0]
                model_path = os.path.join(CLUSTER_MODELS_DIR, f"{filename_without_ext}_kmeans_{n_clusters}_clusters.pkl")
                joblib.dump(kmeans_model, model_path)
                model_paths.append(model_path)

    return output_paths, model_paths

def get_clusters(EMBEDDINGS_PATHS, n_clusters_list, CLUSTER_DIR, CLUSTER_MODELS_DIR=None, random_state=0):
    """Main function to handle clustering, writing results, and saving the models."""
    combined_df = read_and_concatenate_csvs(EMBEDDINGS_PATHS)
    print("Finished reading CSV files and concatenating dataframes")
    clustered_df, kmeans_models_list = apply_kmeans_on_combined(combined_df, n_clusters_list, random_state)
    print("Finished applying KMeans")    
    output_paths, model_paths = split_and_write(clustered_df, CLUSTER_DIR, EMBEDDINGS_PATHS, kmeans_models_list, n_clusters_list, CLUSTER_MODELS_DIR)
    print("Finished writing CSV and model files")
    return output_paths, model_paths