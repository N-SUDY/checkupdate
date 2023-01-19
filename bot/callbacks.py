from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper_fns.helper import USER_DATA, deletewebsite, get_update


############Variables##############
sudo_users = eval(Config.SUDO_USERS)



############CallBack##############
@Client.on_callback_query()
async def newbt(client, callback_query):
        txt = callback_query.data
        print(txt)
        user_id = callback_query.message.chat.id
        
        
        if txt.startswith("clear"):
            await callback_query.message.delete()
            DATA = txt.split("-")
            if len(DATA)==2:
                user = int(DATA[1])
            elif len(DATA)==3:
                user = -int(DATA[2])
            try:
                    URLS = USER_DATA()[user]['URLS']
                    if len(URLS)==0:
                            await client.send_message(chat_id=user_id,
                                                text=f"❗No URL Found")
                            return
                    Names = []
                    a = 0
                    for url in URLS:
                        url = url.replace("https://", "").replace("http://", "").split("/")[0]
                        datam = f"{str(url)}"
                        keyboard = [InlineKeyboardButton(datam, callback_data=f"delete-{str(a)}")]
                        Names.append(keyboard)
                        a += 1
                    await client.send_message(chat_id=user_id,
                                                    text=f'⏺️Choose URL To Clear', reply_markup=InlineKeyboardMarkup(Names))
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                                    text=str(e), disable_web_page_preview=True)
            return
        
        
        elif txt.startswith("delete"):
            await callback_query.message.delete()
            DATA = txt.split("-")
            if len(DATA)==2:
                deleteid = int(DATA[1])
            elif len(DATA)==3:
                deleteid = -int(DATA[2])
            try:
                    url = USER_DATA()[user_id]['URLS'][deleteid]
                    respomse = await deletewebsite(user_id, url)
                    if respomse:
                        await client.send_message(chat_id=user_id,
                                                    text=f'✅URL Deleted Successfully')
                        await client.send_message(Config.Status_Chat, f"🛠Checker Deleted.\n\n🔗URL: {str(url)}", disable_web_page_preview=True)
                    else:
                        await client.send_message(chat_id=user_id,
                                                    text=f'❌Failed To Delete URL')
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                                    text=str(e), disable_web_page_preview=True)
            return


        elif txt.startswith("checkstatus"):
            await callback_query.message.delete()
            DATA = txt.split("-")
            if len(DATA)==2:
                user = int(DATA[1])
            elif len(DATA)==3:
                user = -int(DATA[2])
            try:
                    URLS = USER_DATA()[user]['URLS']
                    if len(URLS)==0:
                            await client.send_message(chat_id=user_id,
                                                text=f"❗No URL Found")
                            return
                    Names = []
                    a = 0
                    for url in URLS:
                        url = url.replace("https://", "").replace("http://", "").split("/")[0]
                        datam = f"{str(url)}"
                        keyboard = [InlineKeyboardButton(datam, callback_data=f"getstatus-{str(a)}")]
                        Names.append(keyboard)
                        a += 1
                    await client.send_message(chat_id=user_id,
                                                    text=f'⏺️Choose URL To Get Status', reply_markup=InlineKeyboardMarkup(Names))
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                                    text=str(e), disable_web_page_preview=True)
            return
        
        
        elif txt.startswith("getstatus"):
            DATA = txt.split("-")
            if len(DATA)==2:
                sid = int(DATA[1])
            elif len(DATA)==3:
                sid = -int(DATA[2])
            try:
                    url = USER_DATA()[user_id]['URLS'][sid]
                    status = str(USER_DATA()[user_id][url])
                    try:
                        await callback_query.answer(
                        str(status),
                        show_alert=True)
                    except:
                            await client.send_message(chat_id=user_id,
                                                    text=str(status), disable_web_page_preview=True)
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                                    text=str(e), disable_web_page_preview=True)
            return


        elif txt.startswith("checkupdate"):
            await callback_query.message.delete()
            DATA = txt.split("-")
            if len(DATA)==2:
                user = int(DATA[1])
            elif len(DATA)==3:
                user = -int(DATA[2])
            try:
                    URLS = USER_DATA()[user]['URLS']
                    if len(URLS)==0:
                            await client.send_message(chat_id=user_id,
                                                text=f"❗No URL Found")
                            return
                    Names = []
                    a = 0
                    for url in URLS:
                        url = url.replace("https://", "").replace("http://", "").split("/")[0]
                        datam = f"{str(url)}"
                        keyboard = [InlineKeyboardButton(datam, callback_data=f"getupdate-{str(a)}")]
                        Names.append(keyboard)
                        a += 1
                    await client.send_message(chat_id=user_id,
                                                    text=f'⏺️Choose URL To Get Update Message', reply_markup=InlineKeyboardMarkup(Names))
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                                    text=str(e), disable_web_page_preview=True)
            return
        
        
        elif txt.startswith("getupdate"):
            DATA = txt.split("-")
            if len(DATA)==2:
                sid = int(DATA[1])
            elif len(DATA)==3:
                sid = -int(DATA[2])
            try:
                    url = USER_DATA()[user_id]['URLS'][sid]
                    update_message = await get_update(url)
                    stext = f"🔗URL: {str(url)}\n🔶Updates: {str(update_message)}"
                    try:
                        await callback_query.answer(
                        str(stext),
                        show_alert=True)
                    except:
                            await client.send_message(chat_id=user_id,
                                                    text=str(stext), disable_web_page_preview=True)
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                                    text=str(e), disable_web_page_preview=True)
            return
        
        return

