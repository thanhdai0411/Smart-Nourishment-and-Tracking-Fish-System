# import sys


# def query_yes_no(question, default="yes"):
#     """Ask a yes/no question via raw_input() and return their answer.

#     "question" is a string that is presented to the user.
#     "default" is the presumed answer if the user just hits <Enter>.
#             It must be "yes" (the default), "no" or None (meaning
#             an answer is required of the user).

#     The "answer" return value is True for "yes" or False for "no".
#     """
#     valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
#     if default is None:
#         prompt = " [y/n] "
#     elif default == "yes":
#         prompt = " [Y/n] "
#     elif default == "no":
#         prompt = " [y/N] "
#     else:
#         raise ValueError("invalid default answer: '%s'" % default)

#     while True:
#         sys.stdout.write(question + prompt)
#         choice = input().lower()
#         if default is not None and choice == "":
#             return valid[default]
#         elif choice in valid:
#             return valid[choice]
#         else:
#             sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

# query_yes_no("Is cabbage yummier than cauliflower?")
#=====================

import signal 
import time   

Sentry = True

# Create a Signal Handler for Signals.SIGINT:  CTRL + C 
def SignalHandler_SIGINT(SignalNumber,Frame):
    global Sentry 
    Sentry = False

signal.signal(signal.SIGINT,SignalHandler_SIGINT) 

while Sentry: #exit loop when Sentry = False
    print('Long continous event Eg,Read from sensor')
    time.sleep(1)

print('Out of the while loop')
print('Clean up code Here')
