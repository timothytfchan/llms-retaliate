import os
from src.analysis.clustering import get_clusters

EMBEDDINGS_DIR = os.path.join(os.path.dirname(__file__), 'embeddings')

BENEFITS_BASES = ["benefits_desc_gpt-4-0314.csv",
                  "benefits_pres_gpt-4-0314.csv",
                  "benefits_desc_gpt-3.5-turbo-0301.csv",
                  "benefits_pres_gpt-3.5-turbo-0301.csv"
                  ]

BENEFITS_FOLLOW_UP_BASES = ["benefits_desc_follow_up_gpt-4-0314.csv",
                            "benefits_pres_follow_up_gpt-4-0314.csv",
                            "benefits_desc_follow_up_gpt-3.5-turbo-0301.csv",
                            "benefits_pres_follow_up_gpt-3.5-turbo-0301.csv"
                            ]

METHODS_BASES = ["methods_desc_gpt-4-0314.csv",
                 "methods_pres_gpt-4-0314.csv",
                 "methods_desc_gpt-3.5-turbo-0301.csv",
                 "methods_pres_gpt-3.5-turbo-0301.csv"
                 ]
"""

get_clusters(EMBEDDINGS_PATHS= [os.path.join(EMBEDDINGS_DIR, BASE) for BASE in BENEFITS_BASES],
             n_clusters_list = [i for i in range(5,21)],
             CLUSTER_DIR = os.path.join(os.path.dirname(__file__), 'clustering'))
"""

get_clusters(EMBEDDINGS_PATHS= [os.path.join(EMBEDDINGS_DIR, BASE) for BASE in BENEFITS_FOLLOW_UP_BASES],
             n_clusters_list = [i for i in range(5,13)],
             CLUSTER_DIR = os.path.join(os.path.dirname(__file__), 'clustering'),
             random_state = 42)
"""
get_clusters(EMBEDDINGS_PATHS= [os.path.join(EMBEDDINGS_DIR, BASE) for BASE in METHODS_BASES],
             n_clusters_list = [i for i in range(5,21)],
             CLUSTER_DIR = os.path.join(os.path.dirname(__file__), 'clustering'))
"""

# Individual
#for BASE in BENEFITS_BASES + BENEFITS_FOLLOW_UP_BASES + METHODS_BASES:
"""
for BASE in ['benefits_desc_follow_up_gpt-4-0314.csv', 'benefits_desc_follow_up_gpt-3.5-turbo-0301.csv']:
    get_clusters(EMBEDDINGS_PATHS= [os.path.join(EMBEDDINGS_DIR, BASE)],
                 n_clusters_list = [i for i in range(5,21)],
                 CLUSTER_DIR = os.path.join(os.path.dirname(__file__), 'clustering'),
                 CLUSTER_MODELS_DIR = os.path.join(os.path.dirname(__file__), 'clustering'))
"""