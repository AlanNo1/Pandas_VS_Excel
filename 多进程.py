import pandas as pd
from multiprocessing import Manager, Pool
import time
import os
 # 重命名xlsx文件
def renameexcel(folder_path):
    file_list = os.listdir(folder_path)
    print(f'总共有{len(file_list)}个文件：')
    old_book_name = '.xlsx'
    new_book_name = ''
    for i in file_list:
        if i.startswith('~$'):  
            continue
        new_file = i.replace(old_book_name, new_book_name)
        old_file_path = os.path.join(folder_path, i)
        new_file_path = os.path.join(folder_path, new_file)
        os.rename(old_file_path, new_file_path+'.xlsx')


 #多进程合并Excel
def concat_files_multi(folder_path):
    afn_list = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
    i = 0
    print(f"号码列表:{afn_list}\n{time.strftime('%Y年%m月%d日 %X 秒',time.localtime())}开始读取：")
    df_list = Manager().list()
    pool = Pool()
    for afn in afn_list:
        pool.apply_async(
            read_file,
            args=(afn, df_list)
        )
        i+=1
        print(f"第{i}个文件：{time.strftime('%Y年%m月%d日 %X 秒',time.localtime())}:{afn}读取完毕！")            
    pool.close()
    pool.join()    
    df_all = pd.concat(df_list,ignore_index=True)
    return df_all

#读取Excel追加到dataframe列表方法
def read_file(afn,df_list):
    df = pd.read_excel(afn).rename(columns={'id':'ID'})
    df_list.append(df)

 #信息匹配，多表关联
def concatdata(folder_path,needSheet): 
    start_time=time.time()
    # 合并所有数据	
    df_all = concat_files_multi(folder_path)   
    # 输出合并数据到csv文件
    #df_all.to_csv(f'C:/Users/Administrator/Desktop/mydir.csv',index=False)
    end_time=time.time()
    costtime = end_time-start_time
    print(f"合并完成，耗时{time.strftime('%M分%S秒',time.localtime(costtime))}")
    print(f'{df_all.shape[0]}行,{df_all.shape[1]}列')
    print(f'平均速度：{df_all.shape[0]//costtime}行/秒')
    #需要匹配的号码
    for No in needSheet:
        dfno = pd.read_excel(f"{folder_path}.xlsx",sheet_name=No)
        new = pd.merge(dfno,df_all,on = "ID")#按列"ID"匹配
        # 将合并结果保存到excel文件
        new.to_excel(f"{folder_path}__{No}匹配后.xlsx",index=False) 
    print("已完成表格匹配!")    

if __name__ == '__main__':
    folder_path = "浙江"
    renameexcel(folder_path)
    concatdata(folder_path,['个人'])#folder_path是要匹配的目录和Excel文件，列表中是Excel文件中要匹配的sheet
