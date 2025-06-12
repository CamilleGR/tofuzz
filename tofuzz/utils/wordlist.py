import csv, os, sys, math

def load_wordlist(filepath,splitted=1) :
    lists = [] 

    with open(filepath, newline='', mode="r") as f : 
        lines = [w.strip() for w in f.readlines()]

        splitted = min(splitted, len(lines))

        filePerSplit= math.ceil(len(lines)/splitted)
        
        for i in range(0,splitted) : 
            lists.append(lines[filePerSplit*i:min(len(lines),filePerSplit*(i+1))])
    return lists 



def normalize_payload(p,n): 
    if len(p) < n : 
        return f"{p}{(n-len(p))*" "}"
    else :
        return f"{p[0:len(p)-3]}..."