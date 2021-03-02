# CSV creation and writing
import os
from pathlib import Path
import csv
# REGEX for formatting/clean-up
import re

# Third party libraries
# MARC processing/extraction
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode

# CSV creation and writing
import os
from pathlib import Path
import csv

# Third party libraries
# MARC processing/extraction
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode

# Custom local libraries
import cleanup_functions as cleanup
from class_ui import App
from class_map import Mappp


LS_MAPPING_OPTIONS = [
        ("Dissertation", "dissertation"),
        ("Map", "map")
        ]


class Mapper():

    def __init__(self):
        # Default None, will get input from user via UI.
        self.ui = None
        self.source_file_path = None
        self.output_name = None
        self.mapping_to_use = None
        self.mapping_recipe = {}
        
        # Run the UI to collect user input.
        self.start_ui()
        self.get_user_selected_options()

        # Based on selected mapping, grab the recipe.
        self.mapping_recipe = self.generate_mapping_recipe()

        self.process_marc(self.source_file_path, self.output_name)
    
    # TODO
    # Gather start up and or validate input recieved.
    # ? Possible to have a function to restore values to UI after destroy? That could then allow for validation in the mapper class instead of handling in UI class.
    # If no name given, auto generate generic file timestamped for when started. Use time.strftime().
    # Current thinking - the FOR LOOP is going to be challenging to allow for multiple input.
    # # Might be able to set up the instructions to be the "mapping" file send to the "mapper" kick off that has a dict - key for the column heading, then value is the dict of instructions to get to be handled by "process field".
    # # # If possible, then the "mapper" could run the FOR LOOP and not have to worry about loading up ALL of the records into memory to then call methods from the class.


    def start_ui(self):
        # Start up the UI via the App Class.
        self.ui = App(LS_MAPPING_OPTIONS)

    
    def get_user_selected_options(self):
        # Get mapping decision from UI.
        # self.source_file_path = self.ui.entry_source_path.get()
        self.source_file_path = self.ui.input_path
        print("Source file path: " + self.source_file_path)

        self.output_name = self.ui.output_path
        print("Output name: " + self.output_name)

        # self.mapping_to_use = self.ui.print_option()
        self.mapping_to_use = self.ui.mapping
        print("using mapping: " + self.mapping_to_use)
    

    def generate_mapping_recipe(self):
        mapping_option = self.mapping_to_use
        Recipe = None
        dict_recipe = {}

        if mapping_option == "map":
            Recipe = Mappp()
        
        dict_recipe = Recipe.get_recipe()

        return dict_recipe

    def process_marc(self, extract_from=None, save_name=None):
        if save_name is None or save_name == "":
            save_name = "output_mapping_maps.csv"

        # Check if the path is surrounded by quotes (default in Windows "Copy Path" option)
        if extract_from:
            if extract_from[0]=='"' and extract_from[-1]=='"':
                # remove first and last quote
                extract_from = extract_from[1:-1]
            # Convert the string to a Path
            extract_from = Path(extract_from)

        # Open File
        with open(extract_from, 'rb') as mf:
            reader = pymarc.MARCReader(mf, to_unicode=True, force_utf8=True)
            
            # Loop through file
            for record in reader:
                dict_csv_fields = {}

                # dict_csv_fields = extract_fields(record)
                # dict_csv_fields = self.process_field(record, *self.mapping_recipe.keys())
                for key in self.mapping_recipe.keys():
                    dict_csv_fields[key] = self.process_field(record, *self.mapping_recipe.fromkeys(key))

                dictionary_to_csv(dict_data=dict_csv_fields, output_name=save_name)
    

    def unpack_recipe(self, dict_recipe={}):
        pass


    # Write contents to CSV file
    def dictionary_to_csv(self, dict_data=None, output_name=None):
        # Assign CSV output name
        if output_name is None:
        # if not output_name:
            csv_file = 'csv_export.csv'
        else:
            # Ensure '.csv' is appended to the filename
            if not output_name[-4:] == '.csv':
                csv_file = output_name + '.csv'
            else:
                csv_file = output_name
        
        # Check if the file already exists, if no, add in HEADERS
        if not os.path.isfile(csv_file):
            with open(csv_file, mode='w', encoding='utf-8', newline='') as csvfile:
                field_names = dict_data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

                # Write to csv file HEADERS
                writer.writeheader()

        # Append/add new row of data to file
        with open(csv_file, mode='a', encoding='utf-8', newline='') as csvfile:
            field_names = dict_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            writer.writerow(dict_data)
    
    
    def process_field(self,
        record=None,
        dict_fields_subs={},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={},
        subfield_delimiter=' ',
        field_delimiter='||',
        ):
        
        # Default output variable.
        return_str = ''
        # Get fields based on field passed as keys in dict.
        ls_fields = []
        # ls_results
        ls_results = []

        for k in dict_fields_subs.keys():

            # Check if field is present.
            if record.get_fields(k):
                print("list is not empty")
                ls_fields.extend(record.get_fields(k))
        
        print("fields list is: " + str(ls_fields))
        
        # Get and process subfield data.
        for f in ls_fields:
            
            # Determine if requested field is a data field. Will be processed differently.
            field_data = ''
            try:
                field_data = f.data
            except:
                pass
            
            if field_data != '':
                print("There is a data field.")
                
                # Assign the return string to be the field's data string.
                return_str = field_data
                
                # Data field is finished processing. Return value and don't continue.
                return return_str

            # If not a data field, continue process.

            ls_subfields = []

            # Filter on indicator.
            # Default for inidicators.
            indicator1 = ''
            indicator2 = ''

            # If indicator is blank or missing, standardize to "none".
            try:
                indicator1 = f.indicator1

                if indicator1 is None or indicator1 == ' ':
                    print(str(f.tag) + " ind1 is NONE.")
                    indicator1 = 'none'
                else:
                    indicator1 = f.indicator1
            except:
                indicator1 = 'none'
            
            try:
                indicator2 = f.indicator2

                if indicator2 is None or indicator2 == ' ':
                    print(str(f.tag) + " ind2 is NONE.")
                    indicator2 = 'none'
                else:
                    indicator2 = f.indicator2
            except:
                indicator2 = 'none'
            
            if indicator1 not in dict_field_first_indicators.get(f.tag) or indicator2 not in dict_field_second_indicators.get(f.tag):
                # Stop processing this field, Skip and continue to next.
                continue
            
            # Continue working on field, assuming it has approved indicators.
            ls_sub_letters = dict_fields_subs.get(f.tag)
            print("sub letters are: " + str(ls_sub_letters))

            # Get subfields.
            ls_subfields = f.get_subfields(*ls_sub_letters)

            # Cleanup -- for each subfield.
            for index, subfield in enumerate(ls_subfields):
                str_subfield = ''

                # Default cleanup, converting to string and trimming white space.
                str_subfield = cleanup.str_convert_trimmed(subfield)

                # Run requested cleanup operations.
                for c in dict_subfield_cleanup.get(f.tag):
                    # Run the cleanup operations:
                    if c == "remove trailing period":
                        str_subfield = cleanup.remove_trailing_period(str_subfield)
                
                # Update the value in the list.
                ls_subfields[index] = str_subfield
            
            # Cleanup -- remove duplicates and remove any empty.
            ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
            ls_subfields = cleanup.list_remove_empty(ls_subfields)

            # Add if results left:
            # Tie together subfields with subfield delimiter.
            if len(ls_subfields) > 0:
                ls_results.append(str(subfield_delimiter).join(ls_subfields))

        # Cleanup -- remove duplicates and remove empty.
        ls_results = cleanup.list_remove_duplicates(ls_results)
        ls_results = cleanup.list_remove_empty(ls_results)

        # Tie together with field delimiter.
        if len(ls_results) > 0:
            return_str = str(field_delimiter).join(ls_results)

        return return_str


if __name__ == "__main__":
    m = Mapper()