import re
import pandas as pd
from pathlib import Path
import os
import openpyxl
import glob


def hw_get_uptime(filelist):
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
            for i in range(len(data_ver)):
                data_ver[i] = re.findall(r'[0-9]{1,9}\s[a-zA-Z]{1,5},\s[0-9]{1,9}\s[a-zA-Z]{1,4},\s[0-9]{1,9}\s[a-zA-Z]{1,5},\s[0-9]{1,9}\s[a-zA-Z]{1,7}', data_ver[i])
                if len(data_ver[i]) == 0:
                    pass
                else:
                    uptime = data_ver[i]
            dict1 = {'设备名': device, '运行时间': uptime}
            df1 = pd.DataFrame(dict1, index=[n])
            df_uptime = pd.concat([df_uptime, df1], join="outer", axis=0, copy=False, ignore_index=True)
    df_uptime.to_excel('ver.xlsx', sheet_name='hw_version', index=False)


def hw_get_mem(filelist):
    df_mem = pd.DataFrame(columns=['设备名', '内存使用率'])
    n = 1
    for file_list in filelist:
        with open(file_list) as f:
            device = re.findall(r"\b10.*/", str(f))[0][0:-1]
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            lines = [i.strip('-') for i in lines]
            data = list(filter(None, lines))
            data_mem = data[0:100]
            for i in range(len(data_mem)):
                data_mem[i] = re.findall(r'Memory Using.*', data_mem[i])
                if len(data_mem[i]) == 0:
                    pass
                else:
                    mem_data = data_mem[i]
                    mem_data = re.findall(r'\b[0-9]{1,2}%', str(mem_data))
            dict1_mem = {'设备名': device, '内存使用率': mem_data}
            df1_mem = pd.DataFrame(dict1_mem, index=[n])
            n = n + 1
            df_mem = pd.concat([df_mem, df1_mem], join="outer", axis=0, copy=False, ignore_index=True)
    df_write_mem = pd.ExcelWriter('ver.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new')
    df_mem.to_excel(df_write_mem, sheet_name='hw_mem', index=False)
    df_write_mem.close()


def hw_get_cpu(filelist):
    df_cpu = pd.DataFrame(columns=['设备名', 'CPU利用率'])
    n = 1
    for file_list in filelist:
        with open(file_list) as f:
            device = re.findall(r"\b10.*/", str(f))[0][0:-1]
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            lines = [i.strip('-') for i in lines]
            data = list(filter(None, lines))
            data_cpu = data[0:100]
            for i in range(len(data_cpu)):
                data_cpu[i] = re.findall(r'CPU utilization.*', data_cpu[i])
                if len(data_cpu[i]) == 0:
                    pass
                else:
                    cpu_data = data_cpu[i]
            dict1_cpu = {'设备名': device, 'CPU利用率': cpu_data}
            df1_cpu = pd.DataFrame(dict1_cpu, index=[n])
            n = n + 1
            df_cpu = pd.concat([df_cpu, df1_cpu], join="outer", axis=0, copy=False, ignore_index=True)
    df_write_cpu = pd.ExcelWriter('ver.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new')
    df_cpu.to_excel(df_write_cpu, sheet_name='hw_cpu', index=False)
    df_write_cpu.close()


def cisco_get_cpu(filelist):
    df_cpu_cisco = pd.DataFrame(columns=['设备名', 'CPU利用率'])
    n = 1
    for file_list in filelist:
        with open(file_list) as f:
            device = re.findall(r"\b10.*/", str(f))[0][0:-1]
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            lines = [i.strip('-') for i in lines]
            data = list(filter(None, lines))
            data_cpu = data[0:100]

            for i in range(len(data_cpu)):
                data_cpu[i] = re.findall(r'CPU utilization.*', data_cpu[i])
                if len(data_cpu[i]) == 0:
                    pass
                else:
                    cpu_data = data_cpu[i]
            dict1_cpu = {'设备名': device, 'CPU利用率': cpu_data}
            df1_cpu = pd.DataFrame(dict1_cpu, index=[n])
            n = n + 1
            df_cpu_cisco = pd.concat([df_cpu_cisco, df1_cpu], join="outer", axis=0, copy=False, ignore_index=True)
    df_write_cpu = pd.ExcelWriter('ver.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new')
    df_cpu_cisco.to_excel(df_write_cpu, sheet_name='cisco_cpu', index=False)
    df_write_cpu.close()


def cisco_get_mem(filelist):
    df_mem_cisco = pd.DataFrame(columns=['设备名', '内存利用率'])
    n = 1
    for file_list in filelist:
        with open(file_list) as f:
            device = re.findall(r"\b10.*/", str(f))[0][0:-1]
            lines = f.readlines()
            lines = [i.strip() for i in lines]
            lines = [i.strip('-') for i in lines]
            data = list(filter(None, lines))
            data_mem = data[0:100]
            for i in range(len(data_mem)):
                data_mem[i] = re.findall(r'Processor Pool Total.*', data_mem[i])
                if len(data_mem[i]) == 0:
                    pass
                else:
                    mem_data = data_mem[i]
                    total_mem = list(map(int, re.findall(r'Total:(.+?)Used', mem_data[0])))
                    used_mem = list(map(int, re.findall(r'Used:(.+?)Free', mem_data[0])))
                    for total in total_mem:
                        for used in used_mem:
                            mem_utilization = used/total
                    mem_data_cisco = '{:.2f}%'.format(mem_utilization * 100)
                    dict1_mem = {'设备名': device, '内存利用率': mem_data_cisco}
                    df1_mem = pd.DataFrame(dict1_mem, index=[n])
                    n = n + 1
                    df_mem_cisco = pd.concat([df_mem_cisco, df1_mem], join="outer", axis=0, copy=False, ignore_index=True)
    df_write_mem = pd.ExcelWriter('ver.xlsx', mode='a', engine='openpyxl', if_sheet_exists='new')
    df_mem_cisco.to_excel(df_write_mem, sheet_name='cisco_mem', index=False)
    df_write_mem.close()


if __name__ == '__main__':
    p = os.path.dirname(os.path.abspath(__file__))
    p = Path(p)
    # verList = list(p.glob("**/display version.txt"))
    # hw_get_uptime(verList)
    # memList = list(p.glob("**/display memory.txt"))
    # hw_get_mem(memList)
    # cpuList = list(p.glob("**/display cpu-usage.txt"))
    # hw_get_cpu(cpuList)
    # cpuList_cisco = list(p.glob("**/show process cpu.txt"))
    # cisco_get_cpu(cpuList_cisco)
    memList_cisco = list(p.glob("**/show process memory.txt"))
    cisco_get_mem(memList_cisco)
