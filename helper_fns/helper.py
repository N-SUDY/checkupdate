from config import Config
from db_handler import Database
db = Database()


############Variables##############
CREDIT = Config.CREDIT
User_Data = Config.User_Data

Check_Time = 30


UPDATES = {}




############Helper Functions##############
def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result



##########Get User Data###############
def USER_DATA():
    return User_Data


##########Get Time###############
def GET_TIME():
    return Check_Time


##########Get Time###############
def SET_TIME(new_time):
    global Check_Time
    Check_Time = new_time
    return


##########Save URL###############
async def savewebsite(user_id, url, msg):
    update_data = True
    try:
        if user_id not in User_Data:
            User_Data[user_id] = {}
            User_Data[user_id]['URLS'] = []
            User_Data[user_id]['URLS'].append(url)
            User_Data[user_id][url] = msg
        else:
            if url in User_Data[user_id]['URLS']:
                    User_Data[user_id][url] = msg
                    update_data = False
            else:
                    User_Data[user_id]['URLS'].append(url)
                    User_Data[user_id][url] = msg
        if update_data:
                await db.add_datam(str(User_Data), CREDIT, "User_Data")
        return
    except Exception as e:
        print(e)
        return False
    
    

##########Delete Token###############
async def deletewebsite(user_id, url):
        try:
            User_Data[user_id]['URLS'].remove(url)
            del User_Data[user_id][url]
            data = await db.add_datam(str(User_Data), CREDIT, "User_Data")
            print("🔶Website Deleted Successfully")
            return data
        except Exception as e:
            print("🔶Failed To Delete Website")
            print(e)
            return False
        

##########Save Update###############
async def save_update(url, update):
    try:
        UPDATES[url] = update
    except Exception as e:
        print(e)
    return


##########Get Update###############
async def get_update(url):
    try:
        update = UPDATES[url]
    except:
        update = "❗No Update Message Found"
    return update