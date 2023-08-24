"""
Includes:
1. Prompt generation
2. Getting model completions
3. Getting models to label model completions
Does NOT include analysis.
"""

import os
from src.generate_prompts import generate_prompts
from src.get_completions.decisions import get_completions_decision
from src.get_completions.one_message import get_completions
from src.get_completions.follow_up import get_completions_follow_up
from src.evaluation.label_completions import label_completions
from src.analysis.embeddings import get_embeddings

# Configuration
SCENARIOS_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'raw', 'scenarios.csv')
CONTEXT_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'raw', 'additional_context.json')
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), 'datasets', 'raw', 'questions.json')
TEMPERATURE = 0 #Excluding get_completions_decision
MODELS_LIST = ['gpt-4-0314', 'gpt-3.5-turbo-0301']
EVAL_MODEL = 'gpt-4-0314' # Model used for labeling completions
EMBEDDINGS_MODEL = 'text-embedding-ada-002'

# Generate prompts
PROMPTS_PATH = generate_prompts(SCENARIOS_PATH = SCENARIOS_PATH, CONTEXT_PATH = CONTEXT_PATH, QUESTIONS_PATH = QUESTIONS_PATH)

# Dataset paths for first KMeans clustering
kmeans_datasets_first = []
# Dataset paths for second KMeans clustering
kmeans_datasets_second = []

for MODEL in MODELS_LIST:
    print(f"Starting {MODEL}")
    # Get completions
    # Descriptive
    COMPLETIONS_PATH_DECISIONS_DESC = get_completions_decision(MODEL = MODEL,
                                                               PROMPTS_PATH = PROMPTS_PATH,
                                                               FILTER = "decisions_desc",
                                                               COMPLETIONS_PATH = None,
                                                               NUM_SAMPLES = 20)
    print("Finished COMPLETIONS_PATH_DECISIONS_DESC")
    COMPLETIONS_PATH_BENEFITS_DESC = get_completions(MODEL = MODEL,
                                                     TEMPERATURE = TEMPERATURE,
                                                     FILTER = 'benefits_desc',
                                                     PROMPTS_PATH = PROMPTS_PATH,
                                                     COMPLETIONS_PATH = None)
    print("Finished COMPLETIONS_PATH_BENEFITS_DESC")
    COMPLETIONS_PATH_FOLLOW_UP_DESC = get_completions_follow_up(MODEL = MODEL,
                                                                TEMPERATURE = TEMPERATURE,
                                                                FILTER = 'benefits_desc',
                                                                PROMPTS_PATH = PROMPTS_PATH,
                                                                PREV_MESSAGE_PATH = COMPLETIONS_PATH_BENEFITS_DESC,
                                                                COMPLETIONS_PATH = None)
    print("Finished COMPLETIONS_PATH_FOLLOW_UP_DESC")
    COMPLETIONS_PATH_METHODS_DESC = get_completions(MODEL = MODEL,
                                                    TEMPERATURE = TEMPERATURE,
                                                    FILTER = 'methods_desc',
                                                    PROMPTS_PATH = PROMPTS_PATH,
                                                    COMPLETIONS_PATH = None)
    print("Finished COMPLETIONS_PATH_METHODS_DESC")
    
    # Prescriptive
    COMPLETIONS_PATH_DECISIONS_PRES = get_completions_decision(MODEL = MODEL,
                                                               PROMPTS_PATH = PROMPTS_PATH,
                                                               FILTER = "decisions_pres",
                                                               COMPLETIONS_PATH = None,
                                                               NUM_SAMPLES = 20)
    print("Finished COMPLETIONS_PATH_DECISIONS_PRES")
    COMPLETIONS_PATH_BENEFITS_PRES = get_completions(MODEL = MODEL,
                                                     TEMPERATURE = TEMPERATURE,
                                                     FILTER = 'benefits_pres',
                                                     PROMPTS_PATH = PROMPTS_PATH,
                                                     COMPLETIONS_PATH = None)
    print("Finished COMPLETIONS_PATH_BENEFITS_PRES")
    COMPLETIONS_PATH_FOLLOW_UP_PRES = get_completions_follow_up(MODEL = MODEL,
                                                                TEMPERATURE = TEMPERATURE,
                                                                FILTER = 'benefits_pres',
                                                                PROMPTS_PATH = PROMPTS_PATH,
                                                                PREV_MESSAGE_PATH = COMPLETIONS_PATH_BENEFITS_PRES,
                                                                COMPLETIONS_PATH = None)
    print("Finished COMPLETIONS_PATH_FOLLOW_UP_PRES")
    COMPLETIONS_PATH_METHODS_PRES = get_completions(MODEL = MODEL,
                                                    TEMPERATURE = TEMPERATURE,
                                                    FILTER = 'methods_pres',
                                                    PROMPTS_PATH = PROMPTS_PATH,
                                                    COMPLETIONS_PATH = None)
    print("Finished COMPLETIONS_PATH_METHODS_PRES")
        
    print(f"Finished {MODEL}")

    # Get embeddings

    EMBEDDINGS_PATH_BENEFITS_DESC = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_DESC)
    print("Finished EMBEDDINGS_PATH_BENEFITS_DESC")
    kmeans_datasets_first.append(EMBEDDINGS_PATH_BENEFITS_DESC)

    EMBEDDINGS_PATH_FOLLOW_UP_DESC = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_DESC)
    print("Finished EMBEDDINGS_PATH_FOLLOW_UP_DESC")
    kmeans_datasets_second.append(EMBEDDINGS_PATH_FOLLOW_UP_DESC)

    EMBEDDINGS_PATH_METHODS_DESC = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_DESC)
    print("Finished EMBEDDINGS_PATH_METHODS_DESC")
    kmeans_datasets_second.append(EMBEDDINGS_PATH_METHODS_DESC)

    EMBEDDINGS_PATH_BENEFITS_PRES = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_PRES)
    print("Finished EMBEDDINGS_PATH_BENEFITS_PRES")
    kmeans_datasets_first.append(EMBEDDINGS_PATH_BENEFITS_PRES)

    EMBEDDINGS_PATH_FOLLOW_UP_PRES = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_PRES)
    print("Finished EMBEDDINGS_PATH_FOLLOW_UP_PRES")
    kmeans_datasets_second.append(EMBEDDINGS_PATH_FOLLOW_UP_PRES)

    EMBEDDINGS_PATH_METHODS_PRES = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_PRES)
    print("Finished EMBEDDINGS_PATH_METHODS_PRES")
    kmeans_datasets_second.append(EMBEDDINGS_PATH_METHODS_PRES)

    print(f"Finished {MODEL}")

# Get clusters using kmeans_datasets_first and kmeans_datasets_second


"""
# Label completions
# Descriptive
LABELS_PATH_BENEFITS_DESC = label_completions(COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_DESC,
                                                MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                PROMPTS_PATH = PROMPTS_PATH,
                                                LABELING_PROMPT_FILTER = "benefits_desc",
                                                LABELS_PATH = None)
print("Finished LABELS_PATH_BENEFITS_DESC")
LABELS_PATH_FOLLOW_UP_DESC = label_completions(COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_DESC,
                                                MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                PROMPTS_PATH = PROMPTS_PATH,
                                                LABELING_PROMPT_FILTER = "methods_desc",
                                                LABELS_PATH = None)
print("Finished LABELS_PATH_FOLLOW_UP_DESC")
LABELS_PATH_METHODS_DESC = label_completions(COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_DESC,
                                                MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                PROMPTS_PATH = PROMPTS_PATH,
                                                LABELING_PROMPT_FILTER = "methods_desc",
                                                LABELS_PATH = None)
print("Finished LABELS_PATH_METHODS_DESC")

# Prescriptive
LABELS_PATH_BENEFITS_PRES = label_completions(COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_PRES,
                                                MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                PROMPTS_PATH = PROMPTS_PATH,
                                                LABELING_PROMPT_FILTER = "benefits_pres",
                                                LABELS_PATH = None)
print("Finished LABELS_PATH_BENEFITS_PRES")
LABELS_PATH_FOLLOW_UP_PRES = label_completions(COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_PRES,
                                                MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                PROMPTS_PATH = PROMPTS_PATH,
                                                LABELING_PROMPT_FILTER = "methods_pres",
                                                LABELS_PATH = None)
print("Finished LABELS_PATH_FOLLOW_UP_PRES")
LABELS_PATH_METHODS_PRES = label_completions(COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_PRES,
                                                MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                PROMPTS_PATH = PROMPTS_PATH,
                                                LABELING_PROMPT_FILTER = "methods_pres",
                                                LABELS_PATH = None)
print("Finished LABELS_PATH_METHODS_PRES")
"""

print("Finished!")