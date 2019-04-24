import re
temp="\ninstalledcapacityofelectricpowersystem\nd一an}1xltongrong}.ong电力系统容且(installedcapaeityofeleetriepowersystem)电力系统中各类发电厂机组额定容t的总和，也称系统装机容量、系统发电设备容t.电力系统规划设计中还要考虑工作出力、负荷备用容t、事故备用容盘、检修备用容量、系统总备用容量、受阻容t、空闲容量、重复容量、系统可调容量及预想出力等。&apikey=96d16cb944abac391be5f799e01ef336"
p=re.compile(r'http://shuyantech.com/api/cndbpedia/avpair\?q=(.*)&apikey=96d16cb944abac391be5f799e01ef336')        
#res=p.match(temp)
#print(res.group(1))
#for a in temp:
#    if a=='\\':
#        a=r'\\'
print(temp[1])