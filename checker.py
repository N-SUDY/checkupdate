from helper_fns.helper import savewebsite
from aiohttp import ClientSession
from datetime import datetime
from pytz import timezone
from time import time
from asyncio import sleep
from helper_fns.helper import USER_DATA, GET_TIME, save_update
from config import Config
from bs4 import BeautifulSoup
from pyrogram.errors import FloodWait

session = ClientSession()
IST = timezone('Asia/Kolkata')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
punc = ['!', '(', ')', '[', ']', '|', '{', '}', ';', ':', "'", '=', '"', '\\', ',', '<', '>', '.', '/', '?', '@', '#', '$', '%', '^', '&', '*', '~', "  ", "\t", "+", "b'", "'"]


async def process_html(string):
    soup = BeautifulSoup(string, features="lxml")
    soup.prettify()
    for s in soup.select('script'):
        s.extract()
    for s in soup.select('meta'):
        s.extract()
    return str(soup).replace('\r', '')



async def record_error(error, url, timex):
    try:
            filehandle = open("All_Errors.txt", 'a', encoding="utf-8")
            filehandle.write(f"❗{str(url)} :  {str(timex)}   -   {str(error)}\n############\n\n\n\n\n\n\n\n")
            filehandle.close()
    except Exception as e:
        print(e)
    return


async def websitechecker(client, user_id, url, new_task):
        if new_task:
                await savewebsite(user_id, url, "🔷Starting Notifier")
        previous_response_html = []
        file_name = url
        for ele in punc:
            if ele in file_name:
                    file_name = file_name.replace(ele, '')
        file_name = f"{str(user_id)}_{str(file_name)}.html"
        url_name = url.replace("https://", '').replace("http://", '').replace('/', '')
        print(url_name)
        while True:
            datetime_ist1 = datetime.now(IST)
            timex = datetime_ist1.strftime('%I:%M:%S %p, %d-%m-%Y')
            Caption_Found = False
            try:
                    if url not in USER_DATA()[user_id]['URLS']:
                                await client.send_message(user_id, f"🔶Notifier Has Been Deleted.\n\n📎Website: {str(url)}", disable_web_page_preview=True)
                                break
                    start_time = time()
                    async with session.get(url=url, headers=headers, timeout=20) as raw_response:
                            response = await raw_response.text()
                            processed_response_html = await process_html(response)
                            processed_response_html = processed_response_html.split("</div>")
                            comp_timex = round(time() - start_time)
                            comp_time = f"{str(comp_timex)} Seconds"
                            changes = ""
                            if url_name=="haryanajobs.in":
                                    new_value = False
                                    try:
                                            for x in processed_response_html:
                                                if "All Latest Govt Job Update" in x:
                                                    soup = BeautifulSoup(x, features="lxml")
                                                    zz = soup.findAll('li')
                                                    if not len(zz)==0:
                                                        new_value = [str(zz[0]).split('</a>')[0]]
                                                        try:
                                                            Caption_Found = str(zz[0].get_text())
                                                            await save_update(url, Caption_Found)
                                                        except Exception as e:
                                                            print(e)
                                                            await record_error(e, url, timex)
                                                        break
                                            if new_value:
                                                if len(previous_response_html)==0:
                                                                previous_response_html = new_value
                                                if previous_response_html != new_value:
                                                            changes = str(new_value[0])
                                            else:
                                                await record_error('[All Latest Govt Job Update] string not found', url, timex)
                                    except Exception as e:
                                                print(e)
                                                await record_error(e, url, timex)
                            elif url_name=="vacancyjobalert.com":
                                Found = False
                                new_value = False
                                for x in processed_response_html:
                                    if "Updates 🥇" in x:
                                        Found = True
                                    if Found:
                                        if "ago" in x:
                                            break
                                if Found:
                                    try:
                                        soup = BeautifulSoup(x, features="lxml")
                                        zz = soup.findAll('a')
                                        if not len(zz)==0:
                                            new_value = [str(zz[-1])]
                                            try:
                                                Caption_Found = str(zz[-1].get_text())
                                                await save_update(url, Caption_Found)
                                            except Exception as e:
                                                print(e)
                                                await record_error(e, url, timex)
                                    except Exception as e:
                                                print(e)
                                                await record_error(e, url, timex)
                                if new_value:
                                        if len(previous_response_html)==0:
                                                        previous_response_html = new_value
                                        if previous_response_html != new_value:
                                                    changes = str(new_value[0])
                                else:
                                        await record_error('[Updates 🥇] string not found', url, timex)
                            else:
                                    if len(previous_response_html)==0:
                                        previous_response_html = processed_response_html
                                    for x in processed_response_html:
                                        if x not in previous_response_html and "data-cf-modified" not in x and "data-cfemail" not in x and "<!DOCTYPE html>" not in x:
                                            try:
                                                x = str(x.strip())
                                            except Exception as e:
                                                print(e)
                                            if len(x)>5:
                                                    changes+= x
                                                    try:
                                                            soup = BeautifulSoup(x, features="lxml")
                                                            zz = soup.findAll('a')
                                                            if not len(zz)==0:
                                                                try:
                                                                    Value_Found = str(zz[0].get_text())
                                                                    if Caption_Found:
                                                                        Caption_Found += "\n\n" + Value_Found
                                                                        await save_update(url, Caption_Found)
                                                                    else:
                                                                        Caption_Found = Value_Found
                                                                        await save_update(url, Caption_Found)
                                                                except Exception as e:
                                                                    print(e)
                                                                    await record_error(e, url, timex)
                                                    except Exception as e:
                                                                print(e)
                                                                await record_error(e, url, timex)
                            if len(changes)!=0:
                                if Caption_Found:
                                    UPDATEX = f"🔷Updates: {str(Caption_Found)}"
                                else:
                                    UPDATEX = f"🔶Updates: Look html file to check what is updated on this website\n`Unable to phrase update response, this can happen on false update response or this website is unsupported by the Phraser`"
                                try:
                                    await client.send_message(user_id, f"🔔New Update Found\n\n🔗Website: {str(url)}\n\n⏳Checked: {str(timex)}\n\n⛔Delete: `/delete {str(url)}`\n\n\n{str(UPDATEX)}", disable_web_page_preview=True)
                                except FloodWait as e:
                                    await sleep(e.value)
                                except Exception as e:
                                    print(e)
                                    await record_error(e, url, timex)
                                await sleep(2)
                                if "🔶" in UPDATEX:
                                        caption = f"🔗Website: `{str(url)}`\n\n⏳Checked: {str(timex)}\n\n\n🔵Bot By Sahil"
                                else:
                                        caption = f"🔗Website: `{str(url)}`\n\n⏳Checked: {str(timex)}\n\n\n{str(UPDATEX)}\n\n\n🔵Bot By Sahil"
                                try:
                                    try:
                                            changes_html = BeautifulSoup(changes, features="lxml")
                                    except Exception as e:
                                            print(e)
                                            await record_error(e, url, timex)
                                            changes_html = changes
                                    filehandle = open(file_name, 'w', encoding="utf-8")
                                    filehandle.write(str(changes_html))
                                    filehandle.close()
                                    await client.send_document(chat_id=Config.Status_Chat, document=file_name, caption=caption)
                                except FloodWait as e:
                                    await sleep(e.value)
                                except Exception as e:
                                    print(e)
                                    await record_error(e, url, timex)
                                text = f"🔵Status: Update Found\n⏳Checked: {str(timex)}\n⚡Ping: {str(comp_time)}\n\n🔶Staus_Code: {str(raw_response.status)}\n🔗Website: {str(url)}\n⏰Notifier Time: {str(GET_TIME())} Secs"
                                await savewebsite(user_id, url, text)
                                if url_name in ["haryanajobs.in", "vacancyjobalert.com"]:
                                    previous_response_html = new_value
                                else:
                                    previous_response_html = processed_response_html
                            else:
                                text = f"🟢Status: Notifier Running\n⏳Checked: {str(timex)}\n⚡Ping: {str(comp_time)}\n\n🔶Staus_Code: {str(raw_response.status)}\n🔗Website: {str(url)}\n⏰Notifier Time: {str(GET_TIME())} Secs"
                                await savewebsite(user_id, url, text)
            except Exception as e:
                                comp_timex = round(time() - start_time)
                                comp_time = f"{str(comp_timex)} Seconds"
                                text = f"❌Status: Website Down\n⏳Checked: {str(timex)}\n💠Connection Time: {str(comp_time)}\n\n🔶Staus_Code: Not Connected\n🔗Website: {str(url)}\n⏰Notifier Time: {str(GET_TIME())} Secs\n\n❗Connect_Error: {str(e)}"
                                await savewebsite(user_id, url, text)
                                try:
                                    await record_error(text, url, timex)
                                except Exception as e:
                                    print(text)
                                    print(e)
            await sleep(GET_TIME())
        return