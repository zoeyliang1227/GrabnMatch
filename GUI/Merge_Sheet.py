import warnings
import pandas as pd

from datetime import datetime

warnings.filterwarnings("ignore", message="Title is more than 31 characters.*")
time_string = datetime.now().strftime('%Y-%m-%d')

def merge(get_excel):
    print(get_excel)
    with pd.ExcelWriter(f'{time_string}_merge.xlsx') as writer:
        for i in range(len(get_excel)):
            file = pd.ExcelFile(get_excel[i])
            sheets = file.sheet_names
            
            for sheet_name in sheets:                                 
                df = file.parse(sheet_name)
                if len(sheet_name)>31:
                    sheet_name=sheet_name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
if __name__ == "__main__":
    get_excel = []
    while True:
        excel = input('Please input the Excel files you want to merge. Press Enter when finished adding: ')
        if excel != '':
            get_excel.append(excel)
        else:
            break
    merge(get_excel)