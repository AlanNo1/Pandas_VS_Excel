#改进版-先合并再匹配
import os
import pandas as pd
import time
# 获取目标文件夹中的需匹配号码文件列表
start_time=time.time()
def renameexcel(mydir):
	# 重命名xlsx文件
	file_list = os.listdir(mydir)
	print(f'总共有{len(file_list)}个文件：')
	old_book_name = '.xlsx'
	new_book_name = ''
	for i in file_list:
		if i.startswith('~$'):	
			continue
		new_file = i.replace(old_book_name, new_book_name)
		old_file_path = os.path.join(mydir, i)
		new_file_path = os.path.join(mydir, new_file)
		os.rename(old_file_path, new_file_path+'.xlsx')

def finddir(mydir):
    filelist = os.listdir(mydir)
    print(f"号码列表:{filelist}\n{time.strftime('%Y年%m月%d日 %X 秒',time.localtime())}开始读取：")
    dfs = []
    i = 0
    for filename in filelist:
        i = i+1
        filepath = os.path.join(mydir,filename)
        df = pd.read_excel(filepath).rename(columns={'id':'ID'})
        print(f"第{i}个文件：{time.strftime('%Y年%m月%d日 %X 秒',time.localtime())}:{filename}读取完毕！-----------------------------")
        dfs.append(df)
    return dfs    

def concatdata(mydir,needNO): 
    dfList = finddir(mydir)
    # 合并所有班级、课程数据
    result = pd.concat(dfList,ignore_index=True)
    # 输出合并数据到csv文件
    #result.to_csv(f'C:/Users/Administrator/Desktop/mydir.csv',index=False)
    end_time=time.time()
    costtime = end_time-start_time
    print(f"合并完成，耗时{time.strftime('%M分%S秒',time.localtime(costtime))}")
    print(f'{result.shape[0]}行,{result.shape[1]}列')
    print(f'平均速度：{result.shape[0]//costtime}行/秒')
    #需要匹配的号码
    for No in needNO:
        dfno = pd.read_excel(f"{prpjiectName}.xlsx",sheet_name=No)
        new = pd.merge(dfno,result,on = "ID").dropna(axis=1,how='all')#根据老王ID这列匹配班级和课程，并删除空列
        # 将合并结果保存到excel文件
        new.to_excel(f"{prpjiectName}__{No}匹配后.xlsx",index=False) 
    print("已完成表格匹配!")
    
#执行   
if __name__ == "__main__":
    prpjiectName ="老王"  #存放号码列表文件夹名称（同时也是需匹配号码的Excel名）
    renameexcel(prpjiectName)
    concatdata(prpjiectName,['班级','课程']) #”老王.xlsx”中的sheet名字列表！
