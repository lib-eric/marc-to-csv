# REGEX for formatting/clean-up
import re


# Cleanup
# Input: Str
# Return: Str -- with trailing period removed
def remove_trailing_period(passed_input, keep_dotted_inital=True):
    passed_input = str(passed_input).strip()
    cleaned_output = passed_input

    
    if keep_dotted_inital == True:
        
        # Regular Expression for checking if last LETTER and PERIOD are an initial
        re_pattern = r'(\s[A-Z]\.)$'

        # If an ending intial is not found, remove
        if re.match(re_pattern, passed_input) is None:
            
            # Check if passed_input has trailing period
            if passed_input[-1] == '.':
                cleaned_output = str(passed_input[0:-1]).strip()
    
    return cleaned_output


# Cleanup
# Input: Str
# Return: Str -- with trailing common subfield punctuation removed
def remove_trailing_punctuation(passed_input, keep_dotted_inital=True):

    passed_input = str(passed_input).strip()
    cleaned_output = passed_input

    if keep_dotted_inital == True:
        
        # Regular Expression for checking if last LETTER and PERIOD are an initial
        re_pattern = r'(\s[A-Z]\.)$'

        # If an ending intial is not found, remove
        if re.match(re_pattern, passed_input) is None:
            
            # Check if passed_input has trailing period
            if passed_input[-1] in ['.',',','/',':',';']:
                cleaned_output = str(passed_input[0:-1]).strip()
    
    return cleaned_output


# Cleanup
# Input: Str -- with numbers
# Return: Str -- with only numbers/digits
def only_numbers(passed_input):
    cleaned_output = str(passed_input).strip()
    
    re_pattern = r'[^\d]'

    cleaned_output = re.sub(re_pattern,"",cleaned_output)

    return cleaned_output


# Cleanup
# Input: ls
# Return: ls -- with duplicates removed
def list_remove_duplicates(passed_list):
    ls_deduped = passed_list

    ls_deduped = list(dict.fromkeys(ls_deduped))

    return ls_deduped


# Cleanup
# Input: ls
# Return: ls -- with empty results removed
def list_remove_empty(passed_list):
    ls_slimmed = passed_list

    ls_slimmed = list(filter(None,ls_slimmed))

    return ls_slimmed



