import pandas as pd

def string_matching(df, column, patterns, case=False):
    context_dict = {}
    
    # Prepare the patterns based on case sensitivity
    prepared_patterns = [pattern if case else pattern.lower() for pattern in patterns]
    
    # Prepare the list to hold matching rows
    matching_rows_list = []
    
    for row in df.itertuples(index=False):
        # Prepare the cell content based on case sensitivity
        cell_content = getattr(row, column) if case else getattr(row, column).lower()
        
        context_key = getattr(row, 'context_key')
        
        for prepared_pattern in prepared_patterns:
            if prepared_pattern in cell_content:
                matching_rows_list.append(row)
                
                # Update the count for this context_key
                context_dict[context_key] = context_dict.get(context_key, 0) + 1
                
                # Break the loop as the row matched one of the patterns
                break
            
    # Create DataFrame from list of matching rows
    matching_rows = pd.DataFrame(matching_rows_list, columns=df.columns).reset_index(drop=True)
    
    # Sort the context_dict by value
    context_dict = {k: v for k, v in sorted(context_dict.items(), key=lambda item: item[1], reverse=True)}
    
    return matching_rows, context_dict
