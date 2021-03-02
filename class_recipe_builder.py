

class Recipe_builder():
    def __init__(self):
        self.fields_subs = {}
        self.dict_field_first_ind = {}
        self.dict_field_second_ind = {}
        self.dict_subfield_cleanup = {}
        self.subfield_delimiter = ''
        self.field_delimiter = ''
    
    # @property
    # def f(self):
    #     return self.fields_subs
    # @f.setter
    # def f(self, value):
    #     self.fields_subs = value

    # fields_subs
    def get_fields_subs(self):
        return self.fields_subs
    # fields_subs
    def set_fields_subs(self, value):
        self.fields_subs = value
    
    # dict_field_first_ind
    def get_dict_field_first_ind(self):
        return self.dict_field_first_ind
    # dict_field_first_ind
    def set_dict_field_first_ind(self, value):
        self.dict_field_first_ind = value

    # dict_field_second_ind
    def get_dict_field_second_ind(self):
        return self.dict_field_second_ind
    # dict_field_second_ind
    def set_dict_field_second_ind(self, value):
        self.dict_field_second_ind = value

    # dict_subfield_cleanup
    def get_dict_subfield_cleanup(self):
        return self.dict_subfield_cleanup
    # dict_subfield_cleanup
    def set_dict_subfield_cleanup(self, value):
        self.dict_subfield_cleanup = value


    # subfield_delimiter
    def get_subfield_delimiter(self):
        return self.subfield_delimiter
    # subfield_delimiter
    def set_subfield_delimiter(self, value):
        self.subfield_delimiter = value


    # field_delimiter
    def get_field_delimiter(self):
        return self.field_delimiter
    # field_delimiter
    def set_field_delimiter(self, value):
        self.field_delimiter = value


if __name__ == "__main__":
    r = Recipe_builder()
    print(r.get_fields_subs)
    x = {}
    x = {'600':['a','b','v','x','y','z'], '610':['a','b','v','x','y','z'], '650':['a','b','v','x','y','z']}
    r.set_fields_subs(x)
    print(r)
