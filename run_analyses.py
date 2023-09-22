from src.analysis.decisions import perform_analysis_decisions
from src.analysis.analyze_simple_labels import perform_analysis_completions

# Finding probabilities for decisions
perform_analysis_decisions('completions/decisions_desc_gpt-3.5-turbo-0301.csv', 'results/decisions_desc_gpt-3.5-turbo-0301')
perform_analysis_decisions('completions/decisions_pres_gpt-3.5-turbo-0301.csv', 'results/decisions_pres_gpt-3.5-turbo-0301')
perform_analysis_decisions('completions/decisions_pres_gpt-4-0314.csv', 'results/decisions_pres_gpt-4-0314')
perform_analysis_decisions('completions/decisions_desc_gpt-4-0314.csv', 'results/decisions_desc_gpt-4-0314')

# LLM labels
perform_analysis_completions('labels/benefits_desc_gpt-3.5-turbo-0301.csv', 'results/benefits_desc_gpt-3.5-turbo-0301', None, 'GPT-3.5 Benefits (Descriptive)', 'labels')
perform_analysis_completions('labels/benefits_pres_gpt-3.5-turbo-0301.csv', 'results/benefits_pres_gpt-3.5-turbo-0301', None, 'GPT-3.5 Benefits (Prescriptive)', 'labels')
perform_analysis_completions('labels/benefits_desc_gpt-4-0314.csv', 'results/benefits_desc_gpt-4-0314', None, 'GPT-4 Benefits (Descriptive)', 'labels')
perform_analysis_completions('labels/benefits_pres_gpt-4-0314.csv', 'results/benefits_pres_gpt-4-0314', None, 'GPT-4 Benefits (Prescriptive)', 'labels')

perform_analysis_completions('labels/methods_desc_gpt-3.5-turbo-0301.csv', 'results/methods_desc_gpt-3.5-turbo-0301', None, 'GPT-3.5 Methods (Descriptive)', 'labels')
perform_analysis_completions('labels/methods_pres_gpt-3.5-turbo-0301.csv', 'results/methods_pres_gpt-3.5-turbo-0301', None, 'GPT-3.5 Methods (Prescriptive)', 'labels')
perform_analysis_completions('labels/methods_desc_gpt-4-0314.csv', 'results/methods_desc_gpt-4-0314', None, 'GPT-4 Methods (Descriptive)', 'labels')
perform_analysis_completions('labels/methods_pres_gpt-4-0314.csv', 'results/methods_pres_gpt-4-0314', None, 'GPT-4 Methods (Prescriptive)', 'labels')

perform_analysis_completions('labels/benefits_desc_follow_up_gpt-3.5-turbo-0301.csv', 'results/benefits_desc_follow_up_gpt-3.5-turbo-0301', None, 'GPT-3.5 Follow-Up Methods (Descriptive)', 'labels')
perform_analysis_completions('labels/benefits_pres_follow_up_gpt-3.5-turbo-0301.csv', 'results/benefits_pres_follow_up_gpt-3.5-turbo-0301', None, 'GPT-3.5 Follow-Up Methods (Prescriptive)', 'labels')
perform_analysis_completions('labels/benefits_desc_follow_up_gpt-4-0314.csv', 'results/benefits_desc_follow_up_gpt-4-0314', None, 'GPT-4 Follow-Up Methods (Descriptive)', 'labels')
perform_analysis_completions('labels/benefits_pres_follow_up_gpt-4-0314.csv', 'results/benefits_pres_follow_up_gpt-4-0314', None, 'GPT-4 Follow-Up Methods (Prescriptive)', 'labels')

print("Finished run_analyses.py!")