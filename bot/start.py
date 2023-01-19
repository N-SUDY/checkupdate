from pyrogram import Client,  filters
from time import time
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper_fns.helper import get_readable_time, USER_DATA, deletewebsite, SET_TIME, GET_TIME
from checker import websitechecker
from asyncio import get_event_loop
from os import execl
from sys import argv, executable
from os.path import exists
from os import remove





############Variables##############
botStartTime = time()
sudo_users = eval(Config.SUDO_USERS)



async def create_backgroud_task(app, user_id, url, new_task):
    get_event_loop().create_task(websitechecker(app, user_id, url, new_task))
    return



################Start####################
@Client.on_message(filters.command('start'))
async def startmsg(client, message):
    user_id = message.chat.id
    text = f"Hi {message.from_user.mention(style='md')}, I Am A Website Update Notifier Bot, Send Me Any Website Link And I Will Notify You When The Website Have Some Update."
    await client.send_message(chat_id=user_id,
                                text=text,reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        f'⭐ Bot By 𝚂𝚊𝚑𝚒𝚕 ⭐',
                                        url='https://t.me/nik66')
                                ], [
                                    InlineKeyboardButton(
                                        f'❤ Join Channel ❤',
                                        url='https://t.me/nik66x')
                                ]]
                        ))
    return



################Time####################
@Client.on_message(filters.command(["time"]))
async def timecmd(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        currentTime = get_readable_time(time() - botStartTime)
        await client.send_message(chat_id=message.chat.id,
                                text=f'♻Bot Is Alive For {currentTime}')
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


@Client.on_message(filters.command(["errors"]))
async def geterrors(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if exists('All_Errors.txt'):
            await client.send_document(chat_id=user_id, document=f"All_Errors.txt", caption=f"Bot By Sahil")
        else:
            await client.send_message(chat_id=user_id,
                                text=f"🔶Currently There Is No Error File.")
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


@Client.on_message(filters.command(["deleteerrors"]))
async def deleteerrors(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if exists('All_Errors.txt'):
            try:
                remove('All_Errors.txt')
            except Exception as e:
                await client.send_message(chat_id=user_id,
                                text=str(e))
                return
            await client.send_message(chat_id=user_id,
                                text=f"✅Successfully Deleted Error File.")
        else:
            await client.send_message(chat_id=user_id,
                                text=f"🔶Currently There Is No Error File.")
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return

################Clear####################
@Client.on_message(filters.command(["clear"]))
async def clear(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        users = USER_DATA().keys()
        if len(users)==0:
            await client.send_message(chat_id=user_id,
                                text=f"❗No User Found")
            return
        
        Names = []
        for user in users:
            datam = f"{str(user)}"
            keyboard = [InlineKeyboardButton(datam, callback_data=f"clear-{str(user)}")]
            Names.append(keyboard)
        await client.send_message(chat_id=user_id,
                                        text=f'⏺️Choose Account', reply_markup=InlineKeyboardMarkup(Names))
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


################Check_Update####################
@Client.on_message(filters.command(["checkupdate"]))
async def check_update_message(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        users = USER_DATA().keys()
        if len(users)==0:
            await client.send_message(chat_id=user_id,
                                text=f"❗No User Found")
            return
        
        Names = []
        for user in users:
            datam = f"{str(user)}"
            keyboard = [InlineKeyboardButton(datam, callback_data=f"checkupdate-{str(user)}")]
            Names.append(keyboard)
        await client.send_message(chat_id=user_id,
                                        text=f'⏺️Choose Account', reply_markup=InlineKeyboardMarkup(Names))
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


################Check_Status####################
@Client.on_message(filters.command(["checkstatus"]))
async def check_status(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        users = USER_DATA().keys()
        if len(users)==0:
            await client.send_message(chat_id=user_id,
                                text=f"❗No User Found")
            return
        
        Names = []
        for user in users:
            datam = f"{str(user)}"
            keyboard = [InlineKeyboardButton(datam, callback_data=f"checkstatus-{str(user)}")]
            Names.append(keyboard)
        await client.send_message(chat_id=user_id,
                                        text=f'⏺️Choose Account', reply_markup=InlineKeyboardMarkup(Names))
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


################Delete####################
@Client.on_message(filters.command(["delete"]))
async def delete(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if len(message.command)==2:
            url = message.command[1]
            respomse = await deletewebsite(user_id, url)
            if respomse:
                await client.send_message(chat_id=user_id,
                                            text=f'✅URL Deleted Successfully')
                await client.send_message(Config.Status_Chat, f"🛠Checker Deleted.\n\n🔗URL: {str(url)}", disable_web_page_preview=True)
            else:
                await client.send_message(chat_id=user_id,
                                            text=f'❌Failed To Delete URL')
            return
        else:
                if user_id in USER_DATA():
                    urls = USER_DATA()[user_id]['URLS']
                    if len(urls)==0:
                        await client.send_message(chat_id=user_id,
                                        text=f"You Have Not Added Any URL Yet.")
                        return
                    Names = []
                    a = 0
                    for url in urls:
                        url = url.replace("https://", "").replace("http://", "").split("/")[0]
                        datam = f"{str(url)}"
                        keyboard = [InlineKeyboardButton(datam, callback_data=f"delete-{str(a)}")]
                        Names.append(keyboard)
                        a += 1
                    await client.send_message(chat_id=user_id,
                                                    text=f'⏺️Choose URL To Delete', reply_markup=InlineKeyboardMarkup(Names))
                    return
                else:
                    await client.send_message(chat_id=user_id,
                                        text=f"You Have Not Added Any URL Yet.")
                    return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return



################Allurls####################
@Client.on_message(filters.command(["allurls"]))
async def checkallurls(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if user_id in USER_DATA():
            urls = USER_DATA()[user_id]['URLS']
            if len(urls)==0:
                await client.send_message(chat_id=user_id,
                                text=f"You Have Not Added Any URL Yet.")
                return
            text = "♻You Have Added Following URLS:\n\n"
            url_data = ''
            for url in urls:
                url_data +=  f"⛓URL: {str(url)}\n⛔Delete: `/delete {str(url)}`\n\n\n"
            text = text + url_data
            await client.send_message(chat_id=user_id,
                                text=text, disable_web_page_preview=True)
            return
        else:
            await client.send_message(chat_id=user_id,
                                text=f"You Have Not Added Any URL Yet.")
            return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return
    

################AllStatus####################
@Client.on_message(filters.command(["allstatus"]))
async def checkalllstatus(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if user_id in USER_DATA():
            urls = USER_DATA()[user_id]['URLS']
            if len(urls)==0:
                await client.send_message(chat_id=user_id,
                                text=f"You Have Not Added Any URL Yet.")
                return
            text = "♻All URLS Status:\n\n"
            url_data = ''
            for url in urls:
                try:
                        url_data +=  f"{str(USER_DATA()[user_id][url])}\n\n\n"
                except Exception as e:
                        await client.send_message(chat_id=user_id,
                                text=f"❗Failed To Get Status Of {str(url)}\n\nError: {str(e)}", disable_web_page_preview=True)
            text = text + url_data
            await client.send_message(chat_id=user_id,
                                text=text, disable_web_page_preview=True)
            return
        else:
            await client.send_message(chat_id=user_id,
                                text=f"You Have Not Added Any URL Yet.")
            return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


################AllChecker####################
@Client.on_message(filters.command(["allchecker"]))
async def allchecker(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        users = USER_DATA().keys()
        if len(users)==0:
            await client.send_message(chat_id=user_id,
                                text=f"❗No User Found")
            return
        data = ''
        for user in users:
            urls = USER_DATA()[user]['URLS']
            total_urls = len(urls)
            if total_urls==0:
                continue
            data += f"🔸{str(user)} [{str(total_urls)}]\n"
        if len(data)!=0:
            await client.send_message(chat_id=user_id,
                                text=data)
        else:
            await client.send_message(chat_id=user_id,
                                text="❗No  Account Found")
        return
            
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return



################deleteall####################
@Client.on_message(filters.command(["deleteall"]))
async def deleteall(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        users = USER_DATA().keys()
        if len(users)==0:
            await client.send_message(chat_id=user_id,
                                text=f"❗No User Found")
            return
        proc = await client.send_message(user_id, "⏳Deleting, Please Wait........")
        tt = 0
        failed = 0
        for user in users:
            urls = USER_DATA()[user]['URLS']
            total_urls = len(urls)
            if total_urls==0:
                continue
            for url in urls:
                respomse = await deletewebsite(user, url)
                if respomse:
                    tt += 1
                else:
                    failed += 1
        await proc.delete()
        data = f"🔶Deleted: {str(tt)}\n❗Failed: {str(failed)}"
        await client.send_message(chat_id=user_id,
                                text=data)
        return
            
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return



################Add####################
@Client.on_message(filters.command(["add"]))
async def addwebsite(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if len(message.command)==2:
            url = message.command[1]
        else:
            try:
                    ask = await client.ask(user_id, f'*️⃣Send Me --URL-- Of The Website.', timeout=60, filters=filters.text)
                    url  = ask.text
            except:
                    await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                    return
            await ask.request.delete()
        if not url.startswith("http"):
                    await client.send_message(chat_id=user_id,
                                        text=f"❌Invalid URL.")
                    return
        if user_id in USER_DATA():
            # if len(USER_DATA()[user_id]['URLS'])==2 and user_id not in sudo_users:
            #             await client.send_message(chat_id=user_id,
            #                             text=f"❗Sorry, You Can Only Add 2 URLs At A Time.")
            #             return
            if url in USER_DATA()[user_id]['URLS']:
                await client.send_message(user_id, "❗Website Is Already Added.")
                return
        await client.send_message(user_id, f"🔷New Notifier Started.\n\n🔗URL: {str(url)}", disable_web_page_preview=True)
        await create_backgroud_task(client, user_id, url, True)
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


################Restart####################
@Client.on_message(filters.command("restart"))
async def restart(_, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        await message.reply_text("♻Restarting...", True)
        execl(executable, executable, *argv)
    else:
        await message.reply_text(f"❌Only Authorized Users Can Use This Command")
        return



##########CheckerTime##############
@Client.on_message(filters.command(["settime"]))
async def addcheckertime(client, message):
    user_id = message.chat.id
    if user_id in sudo_users:
        if len(message.command)==2:
            ctime = message.command[1]
        else:
            try:
                    ask = await client.ask(user_id, f'*️⃣Send Me Notifier Time In Seconds.\n\nCurrent Time: {str(GET_TIME())} Seconds', timeout=60, filters=filters.text)
                    ctime  = ask.text
            except:
                    await client.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                    return
            await ask.request.delete()
            try:
                ctime = int(ctime)
            except:
                await client.send_message(chat_id=user_id,
                                text=f"❌Invalid Time")
                return
            SET_TIME(int(ctime))
            await client.send_message(chat_id=user_id,
                                text=f"✅Successfully Updated Notifier Time To {str(GET_TIME())} Seconds.")
            return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return