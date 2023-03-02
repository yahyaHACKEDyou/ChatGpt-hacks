import time
import requests

results_per_page = 10

api_keys=[]

try:
    with open("api_keys.txt" , "r") as f:
        api_keys +=f.readlines()
        except FileNotFoundError:
            print("api_keys is not found")
            exit()
            except PermissionError
            print("Permission denied when opening api_keys.txt. Exiting")
            exit()
            try:
                with open ("queries.txt", "r", encoding = "utf-8") as f:
                    except FileNotFoundError:
                        print ("queries.txt file not found. Exiting.")
                        exit()
                        except PermissionError
                        print("Permission denied when opening queries.txt. Exiting.")