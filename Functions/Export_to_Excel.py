
import xlwt
import os

style_head = xlwt.easyxf('font: bold 1,height 300;')  
style_body = xlwt.easyxf('font: height 260;')  

def write_header(sheet):
    sheet.write(0, 0, 'Title', style_head) 
    sheet.write(0, 1, 'Company', style_head) 
    sheet.write(0, 2, 'Location', style_head) 
    sheet.write(0, 3, 'Duration', style_head) 
    sheet.write(0, 4, 'Stipend', style_head) 
    sheet.write(0, 5, 'Apply By', style_head) 
    sheet.write(0, 6, 'Applicants', style_head) 
    sheet.write(0, 7, 'Skills Required', style_head) 
    sheet.write(0, 8, 'Perks', style_head) 
    sheet.write(0, 9, 'Details', style_head) 
    sheet.write(0, 10, 'Link', style_head) 

def write_body(params,sheet):
    params = list(params.values())
    max_val = [0]*len(params)
    for excel_row in range(1,len(params[0])+1):
        for excel_col in range(len(params)):
            sheet.write(excel_row,excel_col,params[excel_col][excel_row-1],style_body)
            col_width = len(str(params[excel_col][excel_row-1])) + 3
            max_val[excel_col] = col_width if 160 > col_width > max_val[excel_col] else max_val[excel_col]
            sheet.col(excel_col).width = 256 * max_val[excel_col]

def save_and_export(workbook):
    err = True
    while err:
        err = False
        choice = int(input("\n1: Save and Download the file\n2: Discard file and Exit\n"))
        try:
            if choice == 1:
                name = "webscrap"
                workbook.save('./' + name + '.csv')
                print(f"Data saved to '{name}.csv'")
                exit()
            elif choice == 2:
                exit()
            else:
                raise ValueError
        except PermissionError:
            print("Don't have appropriate permissions to perform the operation. Try changing the name of the file to something unique or run terminal as admin...Choose again")
            err = True
        except ValueError:
            print("Invalid Input, Loading choices again.............")
            err = True
    