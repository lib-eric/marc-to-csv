# from class_mapper import Mapper

class Mappp():

    def __init__(self):
        self.recipe = {}

        self.recipe = self.gather_ingredients()

    def gather_ingredients(self):
        dict_map_fields = {}

        dict_map_fields['dc.identifier'] = self.get_dc_identifier_str()
        dict_map_fields['dc.subject'] = self.get_dc_subject_str()

        return dict_map_fields
    
    def get_recipe(self):
        dict_recipe = {}

        dict_recipe = dict(self.recipe)

        return dict_recipe
    
    # def extract_fields(record):
    #     dict_map_fields = {}

    #     dict_map_fields['dc.identifier'] = get_dc_identifier_str(record)
    #     dict_map_fields['dc.subject'] = get_dc_subject_str(record)

    #     return dict_map_fields


    # def get_dc_subject_str(record):
    def get_dc_subject_str(self):
        # str_results = ""

        # dict_fields_subs = {'600':['a','b','v','x','y','z'], '610':['a','b','v','x','y','z'], '650':['a','b','v','x','y','z']}
        # dict_field_first_indicators = {'600': ['none','0','1','3'], '610': ['none','0','1','2'],'650': ['none','0','1','2']}
        # dict_field_second_indicators = {'600': ['0','1'], '610': ['0','1'], '650': ['0','1']}
        # dict_subfield_cleanup = {'600': ['remove trailing period'], '610': ['remove trailing period'], '650': ['remove trailing period']}
        # subfield_delimiter = '--'
        # field_delimiter = '||'

        # str_results = process_field(record=record,
        #     dict_fields_subs=dict_fields_subs,
        #     dict_field_first_indicators=dict_field_first_indicators,
        #     dict_field_second_indicators=dict_field_second_indicators,
        #     dict_subfield_cleanup=dict_subfield_cleanup,
        #     subfield_delimiter=subfield_delimiter,
        #     field_delimiter=field_delimiter)


        # # print(str_results)
        # return str_results
        dict_instructions = {
            'dict_fields_subs': {'600':['a','b','v','x','y','z'], '610':['a','b','v','x','y','z'], '650':['a','b','v','x','y','z']},
            'dict_field_first_indicators': {'600': ['none','0','1','3'], '610': ['none','0','1','2'],'650': ['none','0','1','2']},
            'dict_field_second_indicators': {'600': ['0','1'], '610': ['0','1'], '650': ['0','1']},
            'dict_subfield_cleanup': {'600': ['remove trailing period'], '610': ['remove trailing period'], '650': ['remove trailing period']},
            'subfield_delimiter': '--',
            'field_delimiter': '||'
        }

        return dict_instructions


    # def get_dc_identifier_str(record):
    def get_dc_identifier_str(self):
        # str_results = ""

        # dict_fields_subs = {'001':[]}
        # dict_field_first_indicators = {'001': ['none']}
        # dict_field_second_indicators = {'001': ['none']}
        # dict_subfield_cleanup = {'001': []}
        # subfield_delimiter = ' '
        # field_delimiter = '||'

        # str_results = process_field(record=record,
        #     dict_fields_subs=dict_fields_subs,
        #     dict_field_first_indicators=dict_field_first_indicators,
        #     dict_field_second_indicators=dict_field_second_indicators,
        #     dict_subfield_cleanup=dict_subfield_cleanup,
        #     subfield_delimiter=subfield_delimiter,
        #     field_delimiter=field_delimiter)

        # # print(str_results)
        # return str_results
        dict_instructions = {
            'dict_fields_subs': {'001':[]},
            'dict_field_first_indicators': {'001': ['none']},
            'dict_field_second_indicators': {'001': ['none']},
            'dict_subfield_cleanup': {'001': []},
            'subfield_delimiter': ' ',
            'field_delimiter': '||'
        }

        return dict_instructions


if __name__ == "__main__":
    m = Mapper(Map)