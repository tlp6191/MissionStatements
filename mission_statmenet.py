import pickle
import re
found=set()
pages = pickle.load(open("501c.p","rb"))
for cat in pages.keys():
    for key in pages[cat].keys():
        lines_left = 0
        for line in pages[cat][key]:
            
            if re.match('.*\Wmission\W.*',line.lower()):
                lines_left = 6
                if key not in found:
                    print ""
                found.add(key)
            if lines_left >0:
                print cat+"|"+key+":"+line.strip()
                lines_left-=1
print found
print len(found)


