
# Used in ReconEngineManager class to check if files list was loaded
# and user actions will not cause an error with uninitialized data:
# Note: do not use it for getters methods
def check_initialization(method):
    def wrapper(self, *args, **kwargs):
        if self.get_data_dict():
            method(self, *args, **kwargs)
        else:
            # means that the files were not loaded
            return

    return wrapper