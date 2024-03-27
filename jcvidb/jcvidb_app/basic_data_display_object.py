class file_data_display_object():
    def __init__(self):
        self.f_id = ""
        self.file_ = ""
        self.display_data = []

class basic_data_display_object():

    def __init__(self):
        self.id = ""
        self.details = ""
        self.references = ""
        self.funding = ""
        self.createdBy = 0
        self.type = 0
        self.approved = 0
        self.creationDate = ""
        self.file_array = []


    def add_file(self, _file):
        if isinstance(_file, file_data_display_object):  # Check if the object is of Child type
            self.file_array.append(_file)
        else:
            print("Invalid child object:", _file)


class col_data_display_object():
    def __init__(self):
        self.file_data_id = ""
        self.col_index = 0
        self.sheet_index = 0
        self.column_names = ""
