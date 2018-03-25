import pickle
found=set()
pages = pickle.load(open("501c.p","rb"))
for cat in pages.keys():
    for key in pages[cat].keys():
        for line in pages[cat][key]:
            if 'mission' in line.lower():
                print cat+"|"+key+":"+line.strip()
                found.add(key)
print found
print len(found)


