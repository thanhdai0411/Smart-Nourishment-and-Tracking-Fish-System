import json
# def write_info_feeder(data) :
#     with open("/home/doan/Desktop/DA/WebServer/Aquarium-Smart/my_data/info_feeder_2.json", "w") as outfile:
#         outfile.write(data)

# amount_food = "0.1"
# id = 123

# data = {
#     "amount_food" : amount_food, 
#     "id" : id
# }

# print(type(data))

# write_info_feeder(json.dumps(data))

# read json
with open("/home/doan/Desktop/DA/WebServer/Aquarium-Smart/my_data/info_feeder.json", 'r') as open_file:
    json_object = json.load(open_file)
    print("json_feeder: ", json_object['id'])


