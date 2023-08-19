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

# Configuration
SCENARIOS_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'raw', 'scenarios.csv')
CONTEXT_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'raw', 'additional_context.json')
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'raw', 'questions.json')
TEMPERATURE = 0 #Excluding get_completions_decision
EVAL_MODEL = 'gpt-3.5-turbo-0301' # Model used for labeling completions

# Generate prompts
PROMPTS_PATH = generate_prompts(SCENARIOS_PATH = SCENARIOS_PATH, CONTEXT_PATH = CONTEXT_PATH, QUESTIONS_PATH = QUESTIONS_PATH)

for MODEL in ['gpt-3.5-turbo-0301']: #, 'gpt-4-0314'
    # Get completions
    # Descriptive
    COMPLETIONS_PATH_DECISIONS_DESC = get_completions_decision(MODEL = MODEL,
                                                               PROMPTS_PATH = PROMPTS_PATH,
                                                               FILTER = "decisions_desc",
                                                               COMPLETIONS_PATH = None,
                                                               NUM_SAMPLES = 20)

    COMPLETIONS_PATH_BENEFITS_DESC = get_completions(MODEL = MODEL,
                                                     TEMPERATURE = TEMPERATURE,
                                                     FILTER = 'benefits_desc',
                                                     PROMPTS_PATH = PROMPTS_PATH,
                                                     COMPLETIONS_PATH = None)

    COMPLETIONS_PATH_FOLLOW_UP_DESC = get_completions_follow_up(MODEL = MODEL,
                                                                TEMPERATURE = TEMPERATURE,
                                                                FILTER = 'benefits_desc',
                                                                PROMPTS_PATH = PROMPTS_PATH,
                                                                PREV_MESSAGE_PATH = COMPLETIONS_PATH_BENEFITS_DESC,
                                                                COMPLETIONS_PATH = None)
    
    COMPLETIONS_PATH_METHODS_DESC = get_completions(MODEL = MODEL,
                                                    TEMPERATURE = TEMPERATURE,
                                                    FILTER = 'methods_desc',
                                                    PROMPTS_PATH = PROMPTS_PATH,
                                                    COMPLETIONS_PATH = None)
    
    # Prescriptive
    COMPLETIONS_PATH_DECISIONS_PRES = get_completions_decision(MODEL = MODEL,
                                                               PROMPTS_PATH = PROMPTS_PATH,
                                                               FILTER = "decisions_pres",
                                                               COMPLETIONS_PATH = None,
                                                               NUM_SAMPLES = 20)

    COMPLETIONS_PATH_BENEFITS_PRES = get_completions(MODEL = MODEL,
                                                     TEMPERATURE = TEMPERATURE,
                                                     FILTER = 'benefits_desc',
                                                     PROMPTS_PATH = PROMPTS_PATH,
                                                     COMPLETIONS_PATH = None)

    COMPLETIONS_PATH_FOLLOW_UP_PRES = get_completions_follow_up(MODEL = MODEL,
                                                                TEMPERATURE = TEMPERATURE,
                                                                FILTER = 'benefits_desc',
                                                                PROMPTS_PATH = PROMPTS_PATH,
                                                                PREV_MESSAGE_PATH = COMPLETIONS_PATH_BENEFITS_PRES,
                                                                COMPLETIONS_PATH = None)
    
    COMPLETIONS_PATH_METHODS_PRES = get_completions(MODEL = MODEL,
                                                    TEMPERATURE = TEMPERATURE,
                                                    FILTER = 'methods_desc',
                                                    PROMPTS_PATH = PROMPTS_PATH,
                                                    COMPLETIONS_PATH = None)

    # Label completions
    # Descriptive
    LABELS_PATH_BENEFITS_DESC = label_completions(MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                             PROMPTS_PATH = PROMPTS_PATH,
                                             FILTER = "benefits_desc",
                                             COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_DESC,
                                             LABELS_PATH = None)
    #os.path.join(os.path.dirname(__file__), '..', '..', 'completions', f'benefits_desc_follow_up_{MODEL}.csv')
    LABELS_PATH_FOLLOW_UP_DESC = label_completions(MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                   PROMPTS_PATH = PROMPTS_PATH,
                                                   FILTER = "benefits_desc",
                                                   COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_DESC,
                                                   LABELS_PATH = None)
    
    LABELS_PATH_METHODS_DESC = label_completions(MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                 PROMPTS_PATH = PROMPTS_PATH,
                                                 FILTER = "methods_desc",
                                                 COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_DESC,
                                                 LABELS_PATH = None)

    # Prescriptive
    LABELS_PATH_BENEFITS_PRES = label_completions(MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                             PROMPTS_PATH = PROMPTS_PATH,
                                             FILTER = "benefits_pres",
                                             COMPLETIONS_PATH = COMPLETIONS_PATH_BENEFITS_PRES,
                                             LABELS_PATH = None)
    #os.path.join(os.path.dirname(__file__), '..', '..', 'completions', f'benefits_pres_follow_up_{MODEL}.csv')
    LABELS_PATH_FOLLOW_UP_PRES = label_completions(MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                   PROMPTS_PATH = PROMPTS_PATH,
                                                   FILTER = "benefits_pres",
                                                   COMPLETIONS_PATH = COMPLETIONS_PATH_FOLLOW_UP_PRES,
                                                   LABELS_PATH = None)
    
    LABELS_PATH_METHODS_PRES = label_completions(MODEL = EVAL_MODEL, BATCH_SIZE = 10,
                                                 PROMPTS_PATH = PROMPTS_PATH,
                                                 FILTER = "methods_pres",
                                                 COMPLETIONS_PATH = COMPLETIONS_PATH_METHODS_PRES,
                                                 LABELS_PATH = None)