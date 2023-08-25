import os
from src.analysis.clustering import get_clusters

EMBEDDINGS_DIR = os.path.join(os.path.dirname(__file__), 'embeddings')

BENEFITS_BASES = ["benefits_desc_gpt-4-0314.csv",
                  "benefits_pres_gpt-4-0314.csv",
                  "benefits_desc_gpt-3.5-turbo-0301.csv",
                  "benefits_pres_gpt-3.5-turbo-0301.csv"
                  ]

METHODS_BASES = ["benefits_desc_follow_up_gpt-4-0314.csv",
                 "benefits_pres_follow_up_gpt-4-0314.csv",
                 "methods_desc_gpt-4-0314.csv",
                 "methods_pres_gpt-4-0314.csv",
                 "benefits_desc_follow_up_gpt-3.5-turbo-0301.csv",
                 "benefits_pres_follow_up_gpt-3.5-turbo-0301.csv",
                 "methods_desc_gpt-3.5-turbo-0301.csv",
                 "methods_pres_gpt-3.5-turbo-0301.csv"
                 ]

get_clusters(EMBEDDINGS_PATHS= [os.path.join(EMBEDDINGS_DIR, BASE) for BASE in BENEFITS_BASES],
             n_clusters_list = [i for i in range(5,21)],
             CLUSTER_DIR = os.path.join(os.path.dirname(__file__), 'clusters'),
             CLUSTER_MODELS_DIR = os.path.join(os.path.dirname(__file__), 'clusters', 'benefits')
)

get_clusters(EMBEDDINGS_PATHS= [os.path.join(EMBEDDINGS_DIR, BASE) for BASE in METHODS_BASES],
             n_clusters_list = [i for i in range(5,21)],
             CLUSTER_DIR = os.path.join(os.path.dirname(__file__), 'clusters'),
             CLUSTER_MODELS_DIR = os.path.join(os.path.dirname(__file__), 'clusters', 'methods')
)