import math
import os
import pandas as pd

def convert_pattern(input_file, saveloc, filename):
    headerline = 4
    no_of_line_in_section=201
    i=1
    header_array=[]
    kk_header_list=[]
    data_array=[]
    temp_data_array=[]
    with open(input_file) as my_file:
        for line in my_file:
            if i <= headerline:
                header_array.append(line)
            elif i >headerline:
                #formular_number = math.ceil((i-headerline)/no_of_line_in_section)
                #attribute_number = (i-headerline)%no_of_line_in_section
                temp_data_array.append(line.replace("\t","").replace("\n",""))
                if (i-headerline)%no_of_line_in_section == 0:
                    data_array.append(temp_data_array)
                    temp_data_array=[]

            i += 1

    #print(data_array)
    #print(i)
    #print(temp_data_array)

    with open('temp\\kk_header.txt') as kk_header_file:
        for line in kk_header_file:
            kk_header_list.append(line)

    #print(kk_header_list)

    print(saveloc+filename[:-4]+"_Covereted.txt")
    with open(saveloc+"\\"+filename[:-4]+"_Covereted.txt", 'w') as file_converted:
        # for line in header_array:
        #     file_converted.write(line)
        for line in kk_header_list:
            file_converted.write(line)
        file_converted.write("\n")
        for line in data_array:
            for cell in line:
                file_converted.write(cell + '\t')
            file_converted.write('\n')
        # for line in temp_data_array:
        #     file_converted.write(line)

    with open('temp\\header.txt', 'w') as header_file:
        for line in header_array:
            header_file.write(line)
    #print(header_array)
    
    with open('temp\\last_line.txt', 'w') as last_line_file:
        for line in temp_data_array:
            last_line_file.write(line)
    #print(temp_data_array)

def reverse_pattern(input_file, saveloc, filename):
    i=1
    data_array=[]
    header_list=[]
    last_line_list=[]
    with open(input_file) as my_file:
        for line in my_file:
            if i == 1:
                pass
            elif i >1:
                line = line.split("\t",1)[0].strip('"') + "\t" + line.split("\t",1)[1]
                if line[-2] != "\t":
                    # print("k1"+line[-1]+"l1")
                    # print("k2"+line[-2]+"l2")
                    line = line + "\n"
                data_array.append(line.replace("\t","\n"))

            i += 1

    with open('temp\\header.txt') as header_file:
        for line in header_file:
            header_list.append(line)
    with open('temp\\last_line.txt') as last_line_file:
        for line in last_line_file:
            last_line_list.append(line)

    with open(saveloc+"\\"+filename.replace("_Covereted","")[:-4]+"_Reversed.txt", 'w') as reversed_file:
        for line in header_list:
            reversed_file.write(line)        
        for line in data_array:
            reversed_file.write(line[:-1])
        for line in last_line_list:
            reversed_file.write(line)
        reversed_file.write("\n")

def reverse_pattern_from_excel(input_file, saveloc, filename):
    i=1
    sheet=1
    data_array=[]
    header_list=[]
    last_line_list=[]

    Excel_df_dict =pd.read_excel(input_file,sheet_name=None,dtype=str)

    for key in Excel_df_dict.keys():
        temp=Excel_df_dict[key]
        if sheet != 1:
            temp=temp[1:]
        temp_str = temp.to_csv(header=False, index=False, line_terminator='\n', sep='\n')
        data_array.append(temp_str+'\n')

        sheet += 1

    with open('temp\\header.txt') as header_file:
        for line in header_file:
            header_list.append(line)
    with open('temp\\last_line.txt') as last_line_file:
        for line in last_line_file:
            last_line_list.append(line)

    with open(saveloc+"\\"+filename.replace("_Covereted","")[:-5]+".txt", 'w') as reversed_file:
        for line in header_list:
            reversed_file.write(line)        
        for line in data_array:
            reversed_file.write(line[:-1])
        for line in last_line_list:
            reversed_file.write(line)
        reversed_file.write("\n")


if __name__ == "__main__":
    Method="0"
    while Method != "C" and Method != "R" and Method != "X" and Method != "c" and Method != "r" and Method != "x":
        Method=input("Convert/Revert/Excel(C/R/X):")
        if Method != "C" and Method != "R" and Method != "X" and Method != "c" and Method != "r" and Method != "x":
            print("Input C or R or X")
            print("You input "+Method)

    fullpathxlsx=input("TXT:")
    if "\"" in fullpathxlsx:
        fullpathxlsx=fullpathxlsx[1:-1]
    saveloc, filename= os.path.split(fullpathxlsx)

    if Method == "C" or Method == "c":
        convert_pattern(fullpathxlsx, saveloc, filename)
    elif Method == "R" or Method == "r":
        reverse_pattern(fullpathxlsx, saveloc, filename)
    elif Method == "X" or Method == "x":
        reverse_pattern_from_excel(fullpathxlsx, saveloc, filename)
    else:
        pass
