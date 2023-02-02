# Quine McCluskey algorithm
# by
# Muhammad Asharib Rehan
# Hafsa Waheed 

def multiply_minterms(x,y):
    res = []
    for i in x:
        if i+"'" in y or (len(i)==2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res

def multiply_exp(x,y):
    res = []
    for i in x:
        for j in y:
            tmp = multiply_minterms(i,j)
            res.append(tmp) if len(tmp) != 0 else None
    return res

def remv_dontcare(my_list,dc_list): # Removes don't care terms from the list
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res

def fEPI(x): # Function to find essential prime implicants from chart
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res

def findVar(x): # Function to find variables in a meanterm
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
            var_list.append(chr(i+65))
    return var_list

def flatten(x): # Flattens a list
    flattened_items = []
    for i in x:
        flattened_items.extend(x[i])
    return flattened_items

def findmin(a): #Function for finding out which minterms are grouped
    gaps = a.count('_')
    if gaps == 0:
        return [str(int(a,2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
    temp = []
    for i in range(pow(2,gaps)):
        temp2,ind = a[:],-1
        for j in x[0]:
            if ind != -1:
                ind = ind+temp2[ind+1:].find('_')+1
            else:
                ind = temp2[ind+1:].find('_')
            temp2 = temp2[:ind]+j+temp2[ind+1:]
        temp.append(str(int(temp2,2)))
        x.pop(0)
    return temp

def compare(a,b): # Function for checking if 2 minterms differ by 1 bit only
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c>1:
                return (False,None)
    return (True,mismatch_index)

def removeTerms(_chart,terms): # Removes minterms which are already covered from chart
    for i in terms:
        for j in findmin(i):
            try:
                del _chart[j]
            except KeyError:
                pass

mint = [int(i) for i in input("Enter the minterms: ").strip().split()]
dontc = [int(i) for i in input("Enter the don't cares: ").strip().split()]
mint.sort()
minterms = mint+dontc
minterms.sort()
size = len(bin(minterms[-1]))-2
groups,all_pi = {},set()

for minterm in minterms:
    try:
        groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
    except KeyError:
        groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]

print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s"%('='*50))
for i in sorted(groups.keys()):
    print("%5d:"%i)
    for j in groups[i]:
        print("\t\t    %-20d%s"%(int(j,2),j)) 
    print('_'*50)

while True:
    tmp = groups.copy()
    groups,m,marked,should_stop = {},0,set(),True
    l = sorted(list(tmp.keys()))
    for i in range(len(l)-1):
        for j in tmp[l[i]]: 
            for k in tmp[l[i+1]]: 
                res = compare(j,k)
                if res[0]:
                    try:
                        groups[m].append(j[:res[1]]+'_'+j[res[1]+1:]) if j[:res[1]]+'_'+j[res[1]+1:] not in groups[m] else None
                    except KeyError:
                        groups[m] = [j[:res[1]]+'_'+j[res[1]+1:]] 
                    should_stop = False
                    marked.add(j)
                    marked.add(k)
        m += 1
    local_unmarked = set(flatten(tmp)).difference(marked)
    all_pi = all_pi.union(local_unmarked)
    print("Unmarked elements(Prime Implicants) of this table:",None if len(local_unmarked)==0 else ', '.join(local_unmarked))
    if should_stop:
        print("\n\nAll Prime Implicants: ",None if len(all_pi)==0 else ', '.join(all_pi))
        break
    print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s"%('='*50))
    for i in sorted(groups.keys()):
        print("%5d:"%i)
        for j in groups[i]:
            print("\t\t%-24s%s"%(','.join(findmin(j)),j))
        print('_'*50)

sz = len(str(mint[-1]))
chart = {}
print('\n\n\nPrime Implicants chart:\n\n    Minterms    |%s\n%s'%(' '.join((' '*(sz-len(str(i))))+str(i) for i in mint),'='*(len(mint)*(sz+1)+16)))
for i in all_pi:
    merged_minterms,y = findmin(i),0
    print("%-16s|"%','.join(merged_minterms),end='')
    for j in remv_dontcare(merged_minterms,dontc):
        x = mint.index(int(j))*(sz+1)
        print(' '*abs(x-y)+' '*(sz-1)+'X',end='')
        y = x+sz
        try:
            chart[j].append(i) if i not in chart[j] else None
        except KeyError:
            chart[j] = [i]
    print('\n'+'_'*(len(mint)*(sz+1)+16))

EPI = fEPI(chart)
print("\nEssential Prime Implicants: "+', '.join(str(i) for i in EPI))
removeTerms(chart,EPI)

if(len(chart) == 0):
    final_result = [findVar(i) for i in EPI]
else:
    P = [[findVar(j) for j in chart[i]] for i in chart]
    while len(P)>1:
        P[1] = multiply_exp(P[0],P[1])
        P.pop(0)
    final_result = [min(P[0],key=len)] 
    final_result.extend(findVar(i) for i in EPI)
print('\n\nFinal Result: F = '+' + '.join(''.join(i) for i in final_result))
