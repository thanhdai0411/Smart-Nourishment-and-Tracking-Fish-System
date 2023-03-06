import json

def write_file_json(path_file_json, data_write) : 
    with open(path_file_json, "w") as open_file:
        open_file.write(json.dumps(data_write))

def read_file_json(path_file_json) : 
    with open(path_file_json, 'r') as open_file:
        json_object = json.load(open_file)
    return json_object   

