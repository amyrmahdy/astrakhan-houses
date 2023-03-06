import json

def to_json(dictionary,file_name):
    f = open(file_name,'w')
    json.dump(dictionary,f)
    f.close()
    
