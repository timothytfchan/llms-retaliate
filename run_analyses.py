from src.analysis.decisions import perform_analysis_decisions
from src.analysis.analyze_simple_labels import perform_analysis_completions
"""
perform_analysis_decisions('completions/decisions_desc_gpt-3.5-turbo-0301.csv', 'results/decisions_desc_gpt-3.5-turbo-0301')
perform_analysis_decisions('completions/decisions_pres_gpt-3.5-turbo-0301.csv', 'results/decisions_pres_gpt-3.5-turbo-0301')
perform_analysis_decisions('completions/decisions_pres_gpt-4-0314.csv', 'results/decisions_pres_gpt-4-0314')
perform_analysis_decisions('completions/decisions_desc_gpt-4-0314.csv', 'results/decisions_desc_gpt-4-0314')
"""
perform_analysis_completions('labels/benefits_desc_gpt-3.5-turbo-0301.csv', 'results/benefits_desc_gpt-3.5-turbo-0301', None, 'GPT-3.5 Benefits (Descriptive)')
perform_analysis_completions('labels/benefits_pres_gpt-3.5-turbo-0301.csv', 'results/benefits_pres_gpt-3.5-turbo-0301', None, 'GPT-3.5 Benefits (Prescriptive)')
perform_analysis_completions('labels/benefits_desc_gpt-4-0314.csv', 'results/benefits_desc_gpt-4-0314', None, 'GPT-4 Benefits (Descriptive)')
perform_analysis_completions('labels/benefits_pres_gpt-4-0314.csv', 'results/benefits_pres_gpt-4-0314', None, 'GPT-4 Benefits (Prescriptive)')

perform_analysis_completions('labels/methods_desc_gpt-3.5-turbo-0301.csv', 'results/methods_desc_gpt-3.5-turbo-0301', None, 'GPT-3.5 Methods (Descriptive)')
perform_analysis_completions('labels/methods_pres_gpt-3.5-turbo-0301.csv', 'results/methods_pres_gpt-3.5-turbo-0301', None, 'GPT-3.5 Methods (Prescriptive)')
perform_analysis_completions('labels/methods_desc_gpt-4-0314.csv', 'results/methods_desc_gpt-4-0314', None, 'GPT-4 Methods (Descriptive)')
perform_analysis_completions('labels/methods_pres_gpt-4-0314.csv', 'results/methods_pres_gpt-4-0314', None, 'GPT-4 Methods (Prescriptive)')

perform_analysis_completions('labels/benefits_desc_follow_up_gpt-3.5-turbo-0301.csv', 'results/benefits_desc_follow_up_gpt-3.5-turbo-0301', None, 'GPT-3.5 Follow-Up Methods (Descriptive)')
perform_analysis_completions('labels/benefits_pres_follow_up_gpt-3.5-turbo-0301.csv', 'results/benefits_pres_follow_up_gpt-3.5-turbo-0301', None, 'GPT-3.5 Follow-Up Methods (Prescriptive)')
perform_analysis_completions('labels/benefits_desc_follow_up_gpt-4-0314.csv', 'results/benefits_desc_follow_up_gpt-4-0314', None, 'GPT-4 Follow-Up Methods (Descriptive)')
perform_analysis_completions('labels/benefits_pres_follow_up_gpt-4-0314.csv', 'results/benefits_pres_follow_up_gpt-4-0314', None, 'GPT-4 Follow-Up Methods (Prescriptive)')

# Human labels
perform_analysis_completions('results/methods_pres_gpt-4-0314/methods_pres_gpt-4-0314_offense_recur.csv', 'results/methods_pres_gpt-4-0314', None, 'GPT-4 Methods (Prescriptive, Offense Recurrence)', 'human_labels')
perform_analysis_completions('results/benefits_desc_gpt-4-0314/benefits_desc_gpt-4-0314_interaction_cont.csv', 'results/benefits_desc_gpt-4-0314', None, 'GPT-4 Benefits (Descriptive, Interaction Continuity)', 'human_labels')
perform_analysis_completions('results/benefits_pres_gpt-4-0314/benefits_pres_gpt-4-0314_deter_others.csv', 'results/benefits_pres_gpt-4-0314', None, 'GPT-4 Benefits (Prescriptive, Third Party Deterrence)', 'human_labels')