from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
from os.path import exists

if exists('config.env'):
  load_dotenv('config.env')


        
        
def get_mongo_data(MONGODB_URI, BOT_USERNAME, id, colz):
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[BOT_USERNAME]
        col = mongo_db[colz]
        print("🔶Getting Data From Database")
        item_details = col.find({"id" : id})
        data = False
        for item in item_details:
                        data = item.get('data')
        if data:
            print("🟢Data Found In Database")
            return data
        else:
            print("🟡Data Not Found In Database")
            return "{}"


class Config:
    API_ID = int(getenv("API_ID",""))
    API_HASH = getenv("API_HASH","")
    TOKEN = getenv("TOKEN","")
    SUDO_USERS = getenv("SUDO_USERS","")
    MONGODB_URI = getenv("MONGODB_URI","")
    CREDIT = "NIK66BOTS"
    BOT_USERNAME = "Notifier66Bot"
    User_Data = eval(get_mongo_data(MONGODB_URI, BOT_USERNAME, CREDIT, "User_Data"))
    Status_Chat = int(getenv("Status_Chat",""))

