
def process():
    inputFilePath = 'D:\gowrishankar.p\Python Script\py_input\cobol_layout.txt'
    global prev_lvl,arr_lvl,cnt,dic_,tab
    tab = '\t'
    arr = []
    arr_lvl = []
    dic_ = {}
    cnt = 0
    prev_lvl = ''
    prev_var = ''
    
    
    arr.append("{")
    
    with open(inputFilePath, "r") as fIn:
         for line in fIn:
             trim = line.strip()[6:72]
             if trim != '':
                split_ = trim.split()
                lvl = split_[0]
                var_ = split_[1].replace(".","")
                # var_ = trim(var_)
    
                if lvl > prev_lvl:
                    if prev_var != '':
                       List_load()
                       Dict_load()
                       arr.append(dic_[prev_lvl]+prev_var+": {")
                           
                           
                if lvl < prev_lvl:
                    List_load()
                    Dict_load()
                    arr.append(dic_[prev_lvl]+prev_var+ ": ''")
                    
                    
                    Len = len(arr_lvl)
                    idx = arr_lvl.index(lvl)
                    
                    for rev in reversed(range(idx,len(arr_lvl))):
                        key = arr_lvl[rev]
                        if lvl == key:
                            braces = dic_[key] + "},"
                        else:
                            braces = dic_[key] + "}"
                        arr.append(braces)
                       
                        
                if lvl == prev_lvl:
                    List_load()
                    if lvl not in dic_:
                        cnt += 1
                        dic_[lvl] = tab*cnt
                        
                    arr.append(dic_[lvl]+prev_var+ ": ''")
    
                prev_lvl = lvl
                prev_var = var_
    
    #To Handle the last record
    idx = arr_lvl.index(prev_lvl)
    arr.append(dic_[lvl]+prev_var+ ": ''")
    
    #Final closing braces
    for rev in reversed(range(idx-1)):
        key = arr_lvl[rev]
        braces = dic_[key] + "}"
        arr.append(braces)
    arr.append("}")
    
    return(arr)

def List_load():
    if prev_lvl not in arr_lvl:
        arr_lvl.append(prev_lvl)
        
def Dict_load():
    global cnt    
    if prev_lvl not in dic_:
        cnt += 1
        dic_[prev_lvl] = tab*cnt
    
def out(arr):    
    json_output_path = 'D:\gowrishankar.p\Python Script\py_output\json.txt'
    
    with open(json_output_path, "w") as txt_file:
        for line in arr:
            txt_file.write(" ".join(line) + "\n") 

if __name__ == '__main__':
    arr = process()
    out(arr)
    