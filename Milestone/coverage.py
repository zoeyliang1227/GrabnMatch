import pandas as pd
import os
import re

from openpyxl import load_workbook

dict1={}
dict2={}

mapping_excel = 'DG4278_Test Coverage.xlsx'
# concat_excel = 'concat.xlsx'
concat_excel = 'Book11.xlsx'

def main():
    # concat()
    # containing_line() 
    wb1 = load_workbook(mapping_excel, read_only = False)
    wb2 = load_workbook(concat_excel, read_only = False)
    
    make_dict(wb1, wb2)
    di()
    #     compare(work1, work2)   
        
    #     # for key, value in dict1.items():
    #     #     print(wb1.sheetnames[sheet], key, len([item for item in value if item]))
        
    #     print(len(dict1[list(dict1.keys())[0]]))
    #     print(len(dict1[list(dict1.keys())[1]]))
    #     print(len(dict1[list(dict1.keys())[2]]))  
    #     print(len(dict1[list(dict1.keys())[3]]))  
    #     print(len(dict1[list(dict1.keys())[4]]))
    #     print(len(dict1[list(dict1.keys())[5]]))  
    #     print(len(dict1[list(dict1.keys())[6]]))  
    #     print(len(dict1[list(dict1.keys())[7]]))
    #     print(len(dict1[list(dict1.keys())[8]]))  
    #     print(len(dict1[list(dict1.keys())[9]]))  
    #     print(len(dict1[list(dict1.keys())[10]]))  
    #     print(len(dict1[list(dict1.keys())[11]])) 
        
    #     df = pd.DataFrame(dict1)
    #     file_path = 'Done.xlsx'
    #     if not os.path.exists(file_path):
    #         with pd.ExcelWriter(file_path, mode="w", engine="openpyxl") as writer:
    #             df.to_excel(writer, index=False, sheet_name=wb1.sheetnames[sheet])
    #     else:
    #         with pd.ExcelWriter(file_path, mode="a", engine="openpyxl", if_sheet_exists='overlay') as writer:
    #             df.to_excel(writer, index=False, sheet_name=wb1.sheetnames[sheet])

def concat():
    excel_files = ['Book1.xlsx', 'Book2.xlsx', 'Book3.xlsx', 'Book4.xlsx', 'Book5.xlsx']
    dfs = [pd.read_excel(file) for file in excel_files]

    result = pd.concat(dfs)
    result.to_excel(concat_excel, index=False)
    
#處理單元格中含有換行符號
def containing_line():
    wb = load_workbook('Book11.xlsx')
    ws = wb.active
    
    for row in ws.iter_rows():
        for cell in row:
            # print(f'第 {cell.row} 列，第 {c} 行，{str(cell.value)}')
            if '\n' in str(cell.value):                    
                print(f"第 {cell.row} 列，第 {cell.column} 行，儲存格 {cell.coordinate} 中的字串包含換行符號")
                num_newlines = cell.value.count('\n')
                                                
                cell_value = ws[f'{cell.coordinate}'].value
                lines = cell_value.split('\n')
                print(cell.row)
                ws.insert_rows(cell.row+1, amount=num_newlines)
                print(cell.row)
                
                for i, line in enumerate(lines, start=1):
                    ws.cell(row=cell.row+i, column=cell.column, value=line)
                    
    
    print(wb[wb.sheetnames[0]].max_row)
    wb.save('BBook11.xlsx')
    
def make_dict(wb1, wb2):
    for sheet in range(1, len(wb1.sheetnames)):
        work1 = wb1[wb1.sheetnames[sheet]]
        for r in range(1, work1.max_column+1):
            key = work1.cell(1, r).value
            dict1[key] = []
            for c in range(2, work1.max_row+1):
                value = work1.cell(c, r).value
                dict1[key].append(value)

    # print(dict1)
    
    work2 = wb2[wb2.sheetnames[0]]
    for r in range(1, work2.max_column+1):
        key = work2.cell(1, r).value
        dict2[key] = []
        for c in range(2, work2.max_row+1):
            value = work2.cell(c, r).value
            dict2[key].append(value)
            
    # print(dict2)
    
def di():
    print(dict2.values())
    # for value in dict2.values():
    #     print(value, '000')
    #     break
        # if '\n' in value:
        #     print(f"值 '{value}' 包含换行符")
        #     split_values = value.split('\n')
        #     print(split_values)
        #     for key, v in dict2.items():
        #         if v == value:
        #             dict2[key] = split_values
        # else:
        #     continue
            # print(f"值 '{value}' 不包含换行符") 

    # print(len(dict2[list(dict1.keys())[0]]))
    # print(len(dict2[list(dict1.keys())[1]]))
    # print(len(dict2[list(dict1.keys())[2]]))  
    # print(len(dict2[list(dict1.keys())[3]]))  
    # print(len(dict2[list(dict1.keys())[4]]))
    # print(len(dict2[list(dict1.keys())[5]]))  
    # print(len(dict2[list(dict1.keys())[6]]))  
    # print(len(dict2[list(dict1.keys())[7]]))
    # print(len(dict2[list(dict1.keys())[8]]))  
    # print(len(dict2[list(dict1.keys())[9]]))  
    # print(len(dict2[list(dict1.keys())[10]]))  
    # print(len(dict2[list(dict1.keys())[11]])) 
    # print(len(dict2[list(dict1.keys())[12]]))  
    # print(len(dict2[list(dict1.keys())[13]])) 
    
def compare(work1, work2):
    dict1['T']=[]
    count_list=[]
    k=1
    for key in dict1:
        for i in range(1, work1.max_row):
            if key == 'Key':
                # print(i, key, dict1[key][i-1])
                count_list.clear()
                for b, CPEGR in enumerate(dict2.get('CPEGR ID')):
                    if is_blank_or_none(CPEGR) == False and is_blank_or_none(dict1[key][i-1]) == False:
                        print(dict1[key][i-1], '111', CPEGR, CPEGR.find('\n') != -1, re.search(dict1[key][i-1], CPEGR))
                        if re.search(dict1[key][i-1], CPEGR):
                            print(f'查看 {concat_excel} 中 第 {b+2} 列有相似的 {dict1[key][i-1]}') #第一個excel 從1開始，第二個excel從0開始，整體少2，故+2   
                            # print(work2.cell(i, 4).value) 
                            
                            if work2.cell(i+1, 4).value not in count_list:
                                count_list.append(work2.cell(i+1, 4).value)
                            
                            # print(len(count_list))
                            # if len(count_list) != 0:
                            #     dict1[list(dict1.keys())[1]].insert(i, '')    
                            #     dict1[list(dict1.keys())[2]].insert(i, '')      
                            #     dict1[list(dict1.keys())[3]].insert(i, '')      
                            #     dict1[list(dict1.keys())[4]].insert(i, '')    
                            #     dict1[list(dict1.keys())[5]].insert(i, '')      
                            #     dict1[list(dict1.keys())[6]].insert(i, '')      
                            #     dict1[list(dict1.keys())[7]].insert(i, '')    
                            #     dict1[list(dict1.keys())[8]].insert(i, '')      
                            #     dict1[list(dict1.keys())[9]].insert(i, '')      
                            #     dict1[list(dict1.keys())[10]].insert(i, '')      
                            #     dict1[list(dict1.keys())[11]].insert(i, '')      

                if len(count_list) == 0:
                    dict1['T'].append('')
                else:
                    dict1['T'].append(count_list[-1:])
                    
        k+=1
                    
def is_blank_or_none(s):
    return s is None or len(s.strip()) == 0

    
    
    
if __name__ == "__main__":
    main()