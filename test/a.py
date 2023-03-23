# import json
# food = open("/home/doan/Desktop/DA/WebServer/Aquarium-Smart/my_data/food_setting.json" , 'r')
# data = json.load(food)

# for value in data : 

#   time_setting = value["time"]
#   amount_food = value["amount_food"]

#   print( "amount food : "+ str(amount_food))

#   controlMotor =  "M" + str((float(amount_food)*1000)) + "E"
#   print( "motor control : "+ str(controlMotor))
a = "1000"
print(int(float(a) * 1000))