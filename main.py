from config import Config
from pyromod import listen
from pyrogram import Client, idle
from checker import websitechecker
from asyncio import get_event_loop

User_Data = Config.User_Data

app = Client(
    "Notifier_Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TOKEN,
    plugins=dict(root="bot"),
)

async def create_backgroud_task(app, user_id, url, new_task):
    get_event_loop().create_task(websitechecker(app, user_id, url, new_task))
    return




if __name__ == "__main__":
    app.start()
    user_ids = User_Data.keys()
    data = "🔶Checker Restarted.\n\n\n"
    for user_id in user_ids:
        if len(User_Data[user_id])!=0:
            if len(User_Data[user_id]['URLS'])!=0:
                    for url in User_Data[user_id]['URLS']:
                        app.run(create_backgroud_task(app, user_id, url, False))
                        print(f"Checker added for {str(url)}.")
                        data += f"🔗URL: {str(url)}\n\n"
    if data != "🔶Checker Restarted.\n\n\n":
            app.send_message(Config.Status_Chat, data, disable_web_page_preview=True)
    uname = app.get_me().username
    print(f'✅@{uname} Started Successfully!✅')
    print(f"⚡Bot By Sahil Nolia⚡")
    idle()
    app.stop()
    print("💀Bot Stopped💀")
