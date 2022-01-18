
# Used in MeasEngineManager class to check if files list was loaded
# and user actions will not cause an error with uninitialized data:
# Note: do not use it for getters methods
def check_initialization(method):
    def wrapper(self, *args, **kwargs):
        if self.get_files_format():
            method(self, *args, **kwargs)
        else:
            # means that the files were not loaded
            return
    return wrapper