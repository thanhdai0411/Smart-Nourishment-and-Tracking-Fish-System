
import time 

year, month, day = time.strftime(
                    '%Y'), time.strftime('%m'), time.strftime('%d')

date_start =  str(day) + "-" + str(month) + "-" + str(year) 

print(date_start)