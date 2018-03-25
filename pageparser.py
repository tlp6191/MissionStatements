import re
import copy

categories= {'c3':[],'c4':[],'c6':[]}
pages= {'c3':{},'c4':{},'c6':{}}

with open('501c3') as f:
    for line in f:
        m = re.match('.*a href="/wiki/(.*?)"',line)
        if m:
            categories['c3'].append(m.group(1))
with open('501c4') as f:
    for line in f:
        m = re.match('.*a href="/wiki/(.*?)"',line)
        if m:
            categories['c4'].append(m.group(1))
with open('501c6') as f:
    for line in f:
        m = re.match('.*a href="/wiki/(.*?)"',line)
        if m:
            categories['c6'].append(m.group(1))

with open('enwiki-20180301-pages-articles-multistream.xml') as f:
    page=[]
    pagetype=None
    title = ""
    for line in f:
        if '<page>' in line:
            page=[]
            pagetype=None
        elif '</page>' in line:
            if pagetype is not None:
                pages[pagetype][title]=copy.deepcopy(page)
        elif '<title>' in line:
            m = re.match('.*<title>(.*)</title>.*',line)
            if not m:
                continue
            title = m.group(1).replace(" ","_")
            
       #     print t
            for c in categories.keys():
                if title in categories[c]:
                    pagetype=c

        else:
            page.append(line)
import pickle
pickle.dump(pages,open("501c.p","wb"))
print categories
print pages['c3'].keys()
print "Unknown"
print set(pages['c3'].keys())-set(categories['c3'])
