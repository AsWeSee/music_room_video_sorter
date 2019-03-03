

class Paths:

    path_income = ""
    path_full = ""
    path_empty = ""
    path_dark_motion = ""

    def __init__(self, folder):
        self.path_income = "D:\\" + folder + "\\1 from camera\\"
        self.path_full = "D:\\" + folder + "\\2 full\\"
        self.path_empty = "D:\\" + folder + "\\3 empty\\"
        self.path_dark_motion = "D:\\" + folder + "\\3_1 dark motion\\"
        self.path_corrects = "D:\\" + folder + "\\4 corrects\\"
        self.path_errors = "D:\\" + folder + "\\4_1 errors\\"
