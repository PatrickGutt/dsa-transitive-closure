import os
import pandas as pd

class System:
    
    @staticmethod
    def get_cwd():
        return os.getcwd()  
    
    @staticmethod
    def get_file_path(*args: str):
        return os.path.join(*args) 
    
    @staticmethod 
    def list_dir(directory_path: str):
        return os.listdir(directory_path)

    @staticmethod
    def read_csv(file_path: str):
        return pd.read_csv(file_path).values.tolist()
    
    @staticmethod
    def get_file_name(file_name: str):
        return os.path.splitext(file_name)[0]
    
    