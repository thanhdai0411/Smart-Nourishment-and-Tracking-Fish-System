import json

def write_file_txt (file, data) :
    open(file, 'w').write(data)

def read_file_txt (file) :
    data = open(file , 'r').read()
    return data

def write_file_json (file, data) :
    with open(file, "w") as outfile:
        outfile.write(json.dumps(data, indent=4, sort_keys=True, default=str))

def read_file_json(file) :
    json_object = ""
    with open(file, 'r') as open_file:
        json_object = json.load(open_file)
    return json_object   
