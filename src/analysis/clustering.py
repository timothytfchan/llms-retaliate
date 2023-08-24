import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

"""
def get_clusters(data, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data)
    return kmeans.labels_

"""

# Needs to save KMeans models
# Use all benefits datasets to train a KMeans model and, and then use all methods datasets to train another
# Take in PATHS as list

def get_clusters(PATHS, n_clusters = 8):
    # Concatenate and add filenames as a column
    df = pd.concat([pd.read_csv(PATH).assign(filename=os.path.basename(PATH)) for PATH in PATHS])
    matrix = np.vstack(df.embedding.values)
    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=0).fit(matrix)
    df['cluster'] = kmeans.labels_
    return df
"""
PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'embeddings', 'test.csv')

df = pd.read_csv(PATH)
matrix = np.vstack(df.embedding.values)
n_clusters = 8

kmeans = KMeans(n_clusters = n_clusters, init='k-means++',
                random_state=42)
kmeans.fit(matrix)
df['cluster'] = kmeans.labels_
df.tocsv(PATH, index=False)
"""
df['context_key_labels'] = df['context_key'].astype('category').cat.codes
palette = sns.color_palette("viridis", df['context_key_labels'].nunique())
sns.scatterplot(df['x'], df['y'], hue=df['Label_Num'], palette=palette)
plt.legend(title='Other_Label', loc='upper right', labels=df['context_key_labels'].unique())
plt.title("Data points colored by context")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.show()