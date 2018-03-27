import re
import string
from collections import defaultdict
import pickle
org_type={}
mission={}

org_def={
"1":"Corporations Organized Under Act of Congress (including Federal Credit Unions)",
"2" : "Title-holding Corporations for Exempt Organizations[3]",
"3" : "Religious, Educational, Charitable, Scientific, Literary, Testing for Public Safety, to Foster National or International Amateur Sports Competition, or Prevention of Cruelty to Children or Animals Organizations",
"4" : "Civic Leagues, Social Welfare Organizations, and Local Associations of Employees",
"5" : "Labor, Agricultural and Horticultural Organizations",
"6" : "Business Leagues, Chambers of Commerce, Real Estate Boards, etc.",
"7" : "Social and Recreational Clubs",
"8" : "Fraternal Beneficiary Societies and Associations",
"9" : "Voluntary Employee Beneficiary Associations",
"10" : "Domestic Fraternal Societies and Associations",
"11" : "Teachers' Retirement Fund Associations",
"12" : "Benevolent Life Insurance Associations, Mutual Ditch or Irrigation Companies, Mutual or Cooperative Telephone Companies, etc.",
"13" : "Cemetery Companies",
"14" : "State-Chartered Credit Unions, Mutual Reserve Funds",
"15" : "Mutual Insurance Companies or Associations",
"16" : "Cooperative Organizations to Finance Crop Operations",
"17" : "Supplemental Unemployment Benefit Trusts",
"18" : "Employee Funded Pension Trust (created before June 25, 1959)",
"19" : "Post or Organization of Past or Present Members of the Armed Forces",
"20" : "Group Legal Services Plan Organizations[b]",
"21" : "Black Lung Benefit Trusts",
"22" : "Withdrawal Liability Payment Fund",
"23" : "Veterans Organization[c]",
"24" : "Section 4049 ERISA Trusts[d]",
"25" : "Title Holding Corporations or Trusts with Multiple Parents",
"26" : "State-Sponsored Organization Providing Health Coverage for High-Risk Individuals",
"27" : "State-Sponsored Workers' Compensation Reinsurance Organization",
"28" : "National Railroad Retirement Investment Trust",
"29" : "Qualified Nonprofit Health Insurance Issuers[e]",
}
def extract():
    with open('mixed') as f:
        for line in f:
            m = re.match(".//(.*).xml.*organization501cTypeTxt=\"(\d*)\"",line)
            if m:
                org_type[m.group(1)]=m.group(2)
            m = re.match(".//(.*).xml.*Organization501c3Ind.*X*",line)
            if m:
                org_type[m.group(1)]="3"
            m = re.match(".//(.*).xml.*ActivityOrMissionDesc>(.*)</ActivityOrMissionDesc>",line)
            if m:
                mission[m.group(1)]=m.group(2)
            m = re.match(".//(.*).xml.*PrimaryExemptPurposeTxt(.*)PrimaryExemptPurposeTxt",line)
            if m:
                mission[m.group(1)]=m.group(2)
    pickle.dump(mission,open("mission.p","wb"))
    pickle.dump(org_type,open("org.p","wb"))
def load():
    global org_type
    global mission
    org_type = pickle.load(open("org.p","rb"))
    mission = pickle.load(open("mission.p","rb"))
#extract()
load()

#print mission
#print org_type

combined = set(mission.keys()) & set(org_type.keys())
inverted_org_type = defaultdict(list)
for key in org_type.keys():
#    if key in mission:
        inverted_org_type[org_type[key]].append(key)
#print inverted_org_type
for key in sorted(inverted_org_type.keys()):
    print "Number of "+key+"="+str(len(inverted_org_type[key]))
word_count={}
ratio = {}
for k in org_type.keys():
    word_count[org_type[k]] = defaultdict(int)
    ratio[org_type[k]] = defaultdict(float)
word_count["0"] = defaultdict(int)
#print len(mission)
for key in combined:
    arr = mission[key].split()
    words = []
    for a in arr:
        words.extend(a.split(",/"))
    for w in words:
        word = w.strip().upper()
        word = word.translate(None, string.punctuation)
        word_count["0"][word]+=1
#        word_count["0"]["phebus"]+=1
        word_count[org_type[key]][word]+=1
#        word_count[org_type[key]]["phebus"]+=1

for w in word_count["0"].keys():
    if word_count["0"][w] < 10:
        continue
    for type in set(org_type.values()):
        ratio[type][w] = (0.0+word_count[type][w])/word_count["0"][w]
   
for t in sorted(inverted_org_type.keys()):
    print "Top for 501c"+t+", "+org_def[t]
    i = 0
    for w in reversed(sorted(ratio[t].keys(), key=lambda x: (ratio[t][x],word_count["0"][x]))):
        i=i+1
        print w+":"+str(word_count[t][w])+"/"+str(word_count["0"][w])
        if (t != "3" and i>100) or (i>10000):
            break
    print ""
