import re
import os
file_dir=os.path.join(os.getcwd(),'word.csv')
out_dir=os.path.join(os.getcwd())
entity=[]
produce=[]
r=open(out_dir+'produce.txt','a')
with open(file_dir,encoding='utf-8') as f:
    for line in f:
        line=re.split(r',',line)
        if line[0]=='':
            entity.append(line[1].strip('""'))
            produce.append(' ')
        else:
            entity.append((re.split('\n',line[1])[0]).strip('"'))
            produce.append(line[0].strip('"'))
r=open(file_dir+'produce.txt','a')
for en,pr in zip(entity,produce):
    r.write(en+' '+pr+'\n')
r.close()
