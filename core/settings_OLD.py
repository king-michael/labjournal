#!/usr/bin/env
"""
Settings of the system:
 Handles current settings
 imports default and custom settings
"""
# ToDo: import of custom settings
from default_settings import default_settings

class Settings(dict):
    def __init__(self):
        """Settings"""
        try:
            self.defaults = default_settings
        except:
            raise StandardError("No default settings found\n"
                                "Should be here in this folder")
        self.restore_defaults()  # set Settings to default values

    def read_custom(self):
        """Not implemented yet
        Function to read in custom settings and update"""
        pass

    def restore_defaults(self):
        """set Settings to default values"""
        # Create a dict with the current settings
        self.update(self.defaults)


settings = Settings()

if __name__ == '__main__':
    print(settings)
    print(settings['Database'])
