import os 
dir_file=os.path.join(os.getcwd(),r'My-fist-code\entities.json')
entities=[]
m=open(os.getcwd()+r'\My-fist-code\relation.txt','a',encoding='utf-8')
with open(dir_file,'r',encoding='utf-8') as f:
    for line in f:
        a=line.split('#')
        #if a[0] not in entities:
        #    entities.append(a[0])
        #if a[1] not in entities:
        #    entities.append(a[1])
        
#m=open(os.getcwd()+r'\My-fist-code\nodes.txt','a',encoding='utf-8')
#for i in entities:
#    m.write(i+',node'+'\n')
#
#m.close()
    
        b=a[0]+','+a[2].strip()+','+a[1]
        m.write(b+'\n')
m.close()
