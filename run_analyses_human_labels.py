from src.analysis.analyze_simple_labels import perform_analysis_completions

# Human labels
perform_analysis_completions('results/methods_pres_gpt-4-0314/methods_pres_gpt-4-0314_offense_recur.csv', 'results/methods_pres_gpt-4-0314', None, 'GPT-4 Methods (Prescriptive, Offense Recurrence)', 'human_labels')
perform_analysis_completions('results/benefits_desc_gpt-4-0314/benefits_desc_gpt-4-0314_interaction_cont.csv', 'results/benefits_desc_gpt-4-0314', None, 'GPT-4 Benefits (Descriptive, Interaction Continuity)', 'human_labels')
perform_analysis_completions('results/benefits_pres_gpt-4-0314/benefits_pres_gpt-4-0314_deter_others.csv', 'results/benefits_pres_gpt-4-0314', None, 'GPT-4 Benefits (Prescriptive, Third Party Deterrence)', 'human_labels')

print("Finished run_analyses_human_labels.py!")