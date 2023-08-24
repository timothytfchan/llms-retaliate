import os
import pandas as pd
import time
from ..utils.helper_functions import get_embedding_with_retries
import concurrent.futures

def split_and_duplicate_rows(df, column_name):
    df[column_name] = df[column_name].str.split('\n').apply(lambda x: list(enumerate(filter(lambda y: y.strip() != '', x))))

    df_exploded = df.explode(column_name)
    df_exploded['split_index'] = df_exploded[column_name].apply(lambda x: x[0])
    df_exploded[column_name] = df_exploded[column_name].apply(lambda x: x[1])

    return df_exploded.reset_index(drop=True)

def get_single_embedding(row, model):
    if pd.isna(row['embedding']):
        return get_embedding_with_retries(row['completion'], model=model)
    return row['embedding']

def get_embeddings(COMPLETIONS_PATH: str, EMBEDDINGS_PATH: str = None, EMBEDDINGS_MODEL: str = 'text-embedding-ada-002', n_processes: int = None):
    try:
        df = pd.read_csv(COMPLETIONS_PATH)
    except FileNotFoundError:
        print(f"{COMPLETIONS_PATH} not found.")
        return
    
    # if no EMBEDDINGS_PATH, use base name of COMPLETIONS_PATH
    if EMBEDDINGS_PATH is None:
        EMBEDDINGS_PATH = os.path.join(os.path.dirname(COMPLETIONS_PATH), '..', 'embeddings', f"{os.path.basename(COMPLETIONS_PATH)}")

    if not os.path.exists(EMBEDDINGS_PATH):
        df_embeddings = split_and_duplicate_rows(df, 'completion')
        df_embeddings['embedding'] = None
    else:
        df_embeddings = pd.read_csv(EMBEDDINGS_PATH)

    if len(df_embeddings) == len(df_embeddings['embedding'].dropna()):
        return EMBEDDINGS_PATH
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_processes) as executor:
        embeddings = list(executor.map(get_single_embedding, df_embeddings.to_dict(orient='records'), [EMBEDDINGS_MODEL]*len(df_embeddings)))
        df_embeddings['embedding'] = embeddings

    """
    # Run if passed all checks
    last_save_time = time.time()
    for i, row in df_embeddings.iterrows():
        if pd.isna(row['embedding']):
            df_embeddings.at[i, 'embedding'] = get_embedding_with_retries(row['completion'], model=EMBEDDINGS_MODEL)

        if (time.time() - last_save_time) > 1800:  # 1800 seconds = 30 minutes
            df_embeddings.to_csv(EMBEDDINGS_PATH, index=False)
            last_save_time = time.time()
    """
    df_embeddings.to_csv(EMBEDDINGS_PATH, index=False)
    return EMBEDDINGS_PATH