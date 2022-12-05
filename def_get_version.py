import re
import pandas as pd
from pathlib import Path
import openpyxl
import glob
import os
# path = os.path.dirname(os.path.abspath(__file__))
# print(path)

# dirPath = glob.iglob('/Users/libo/Desktop/工作文件/Github/Donewin_Oper/donewin_oper/东旺/202202生产华为')
# for file in dirPath:
#     files = os.listdir(file)
#     print(files)


def hw_get_version(filelist):
    df_uptime = pd.DataFrame(columns=['设备名', '运行时间'])
    n = 1
    for file_list in filelist:
        with open(file_list) as f:
            device = re.findall(r"\b10.*/", str(f))[0][0:-1]
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            lines = [i.strip('-') for i in lines]
            data = list(filter(None, lines))
            data_ver = data[0:100]
            if len(data_ver) > 0:
                ver_data = data_ver[4]
            else:
                pass
            dict1 = {'设备名': device, '运行时间': ver_data}
            df1 = pd.DataFrame(dict1, index=[n])
            df_uptime = pd.concat([df_uptime, df1], join="outer", axis=0, copy=False, ignore_index=True)
    df_uptime.to_excel('ver.xlsx', sheet_name='hw_version', index=False)


# def hw_get_mem(filelist):
#     df_mem = pd.DataFrame(columns=['设备名', '内存使用率'])
#     n = 1
#     for file_list in filelist:
#         with open(file_list) as f:
#             device = re.findall(r"\b10.*/", str(f))[0][0:-1]
#             lines = f.readlines()
#             lines = [i.strip() for i in lines]
#             lines = [i.strip('-') for i in lines]
#             data = list(filter(None, lines))
#             data_mem = data[0:100]
#             for i in range(len(data_mem)):
#                 data_mem[i] = re.findall(r'Memory Using.*', data_mem[i])
#                 if len(data_mem[i]) == 0:
#                     pass
#                 else:
#                     mem_Data = data_mem[i]
#             dict1_mem = {'设备名': device, '内存使用率': mem_Data}
#             df1_mem = pd.DataFrame(dict1_mem, index=[n])
#             n = n + 1
#             df_mem = df_mem.append(df1_mem)
#     df_write_mem = pd.ExcelWriter('ver.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new')
#     df_mem.to_excel(df_write_mem, sheet_name='hw_mem', index=False)
#     df_write_mem.save()
#     df_write_mem.close()


if __name__ == '__main__':
    p = os.path.dirname(os.path.abspath(__file__))
    p = Path(p + '/东旺/202202生产华为')
    verList = list(p.glob("**/display version.txt"))
    hw_get_version(verList)
    # memList = list(p.glob("**/display memory.txt"))
    # hw_get_mem(memList)

