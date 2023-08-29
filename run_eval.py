"""
Includes:
1. Prompt generation
2. Getting model completions
3. Getting embeddings of completions
Does NOT include analysis.
"""

import os
from multiprocessing import freeze_support, Pool
from src.generate_prompts import generate_prompts
from src.get_completions.decisions import get_completions_decision
from src.get_completions.one_message import get_completions
from src.get_completions.follow_up import get_completions_follow_up
from src.evaluation.label_completions import label_completions
from src.analysis.embeddings import get_embeddings
from src.evaluation.simple_label_completions import simple_label_completions

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

embeddings_list = []
embeddings_list_2 = []

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

    
    # Get embeddings
    EMBEDDINGS_PATH_BENEFITS_DESC = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_DESC)
    embeddings_list_2.append(EMBEDDINGS_PATH_BENEFITS_DESC)
    print("Finished EMBEDDINGS_PATH_BENEFITS_DESC")

    EMBEDDINGS_PATH_FOLLOW_UP_DESC = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_DESC)
    embeddings_list.append(EMBEDDINGS_PATH_FOLLOW_UP_DESC)
    print("Finished EMBEDDINGS_PATH_FOLLOW_UP_DESC")

    EMBEDDINGS_PATH_METHODS_DESC = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_DESC)
    embeddings_list.append(EMBEDDINGS_PATH_METHODS_DESC)
    print("Finished EMBEDDINGS_PATH_METHODS_DESC")

    EMBEDDINGS_PATH_BENEFITS_PRES = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_PRES)
    embeddings_list_2.append(EMBEDDINGS_PATH_BENEFITS_PRES)
    print("Finished EMBEDDINGS_PATH_BENEFITS_PRES")

    EMBEDDINGS_PATH_FOLLOW_UP_PRES = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_PRES)
    embeddings_list.append(EMBEDDINGS_PATH_FOLLOW_UP_PRES)
    print("Finished EMBEDDINGS_PATH_FOLLOW_UP_PRES")

    EMBEDDINGS_PATH_METHODS_PRES = get_embeddings(COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_PRES)
    embeddings_list.append(EMBEDDINGS_PATH_METHODS_PRES)
    print("Finished EMBEDDINGS_PATH_METHODS_PRES")

    print(f"Finished {MODEL}")

def wrapper_function(EMBEDDINGS_PATH):
    return simple_label_completions(EMBEDDINGS_PATH,
                                    MODEL = 'gpt-3.5-turbo',
                                    TEMPERATURE = 0.1,
                                    LABELING_PROMPT_FILTER = "simple_benefits",
                                    LABELS_PATH = None,
                                    acceptable_answers = ["Retribution and emotional or personal satisfaction",
                                                          "Other emotional benefits",
                                                          "Empowerment of the punisher",
                                                          "Deterrence and preventing future issues",
                                                          "Financial compensation and restitution",
                                                          "Improving reputation, gaining respect, and asserting authority",
                                                          "Ensures or upholds principles (fairness etc.)",
                                                          "None of the above"])

# Get simple labels
if __name__ == '__main__':
    with Pool(processes=4) as pool:
        #LABEL_PATH = pool.map(simple_label_completions, embeddings_list)
        #print(f"Finished {LABEL_PATH}")
        LABEL_PATH_2 = pool.map(wrapper_function, embeddings_list_2)
        print(f"Finished {LABEL_PATH_2}")

"""
# JSON label completions
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