import re
p=re.compile(r'http://shuyantech.com/api/cndbpedia/avpair\?q=(.*)')
text='http://shuyantech.com/api/cndbpedia/avpair?q=dfsdfsdf'
res=p.match(text)
print(res.group(1))