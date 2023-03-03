import json
import asyncio
from python_ghost_cursor import path
from python_ghost_cursor.playwright_sync import create_cursor
from proxyChecking import proxyChecking
from database import database
import os.path
from location import loc
import concurrent.futures
from playwright.sync_api import sync_playwright
import os
from getJSON import getJson
from getMysqlData import getSQLDATA
from location import loc
from playwright_stealth import stealth_sync
from proxyChecking import proxyChecking
import requests
import time
from coreConfig import CoreConfig
from seedLogin import seedLogin
from playwright.sync_api import expect
import re

#filePath=os.path.dirname(os.path.abspath(__file__))
SessionFilePath=f"C:\production\\SessionData\\"

def xpathAction(page,ElementSelector):
    try:
        page.wait_for_selector(ElementSelector)
        page.click(ElementSelector)
    except Exception as e:
        print("Exception in xpathAction")
        print(ElementSelector)
        pass


def timeout(page,duration):
    page.wait_for_timeout(duration)

def handlePopup(page,pop,popupLen):
    for i in range(len(popupLen)):
        try:
            print(pop)
            page.click(pop,timeout=2000)
        except Exception as e:
            pass
        # try:
        #     page.wait_for_selector(i,timeout=5000)
        #     page.click(i,timeout=5000)     
        # except Exception as e:
        #     print(f"\n [ Error ]  >>  {type(e).__name_} at line {e.__traceback__.tb_lineno} of {_file__}: {e}")
        #     print("Exceptions in popup")
        #     pass

    # try:
    #     page.wait_for_selector("//button[tabindex='-1' and title='Maybe later']",timeout=5000)
    #     page.click("//button[tabindex='-1' and title='Maybe later']")     
    # except Exception as e:
    #     print(f"\n [ Error ]  >>  {type(e).__name_} at line {e.__traceback__.tb_lineno} of {_file__}: {e}")
    #     print("Exceptions in popup")


def scroll(page):
    for i in range(2):
        page.mouse.wheel(0, 100)
        page.mouse.wheel(100, 300)
        time.sleep(2)


def actionsNS(page,data,profileid):
    email=str(data[2]).strip()
    cursor = create_cursor(page)
    # print(len(list(popup["popUp"]["allPopUp"].split('|'))))
    
    #handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
    page.wait_for_selector(action["Action"]["Composed"])
    xpathAction(page,action["Action"]["spam"])
    try:
        spamSubject=str(data[8].strip())
        print("spamSubject",spamSubject)
        SpamSubjectSelector=str(action["Action"]["SpamSubjectSelector"])
        print("SpamSubjectSelector",SpamSubjectSelector)
        Sub=SpamSubjectSelector.replace('__Subject',str(spamSubject))
        a=page.locator(Sub)
        page.wait_for_timeout(4000)
        if config["config"]["spam_percentage"]:     #10/100 * 80 = X
            percentangeEmailCount=int((int(config["config"]["spam_percentage"])/100*a.count()))
        else:
            percentangeEmailCount=a.count()
        for i in range(0,percentangeEmailCount):
            xpathAction(page,Sub)
            scroll(page)
            xpathAction(page,action["Action"]["notSpam"])
            timeout(page,5000)
        query1=f'''update job_email set status  = "1" and remark = "{percentangeEmailCount} Mails are marked as Notspam"  where jobid = "{profileid}" and Email="{email}";'''
        print(query1)
        database.updateDb(query1)
    except Exception as e:
        print("Exception in actionNS")

def actionIB(page,data,profileid):
    email=str(data[2]).strip()
    try:
        spamSubject=str(data[8].strip())
        SpamSubjectSelector=str(action["Action"]["SpamSubjectSelector"])
        Sub=SpamSubjectSelector.replace('__Subject',str(spamSubject))
        page.wait_for_selector(action["Action"]["inbox"])
        cursor = create_cursor(page)
        cursor.click(action["Action"]["inbox"])
        a=page.locator(Sub)
        if config["config"]["inbox_percentage"]:     #10/100 * 80 = X
            percentangeEmailCount=int((int(config["config"]["inbox_percentage"])/100*a.count()))
        else:
            percentangeEmailCount=a.count()
        for i in range(0,percentangeEmailCount):
            xpathAction(page,Sub)
            cursor.click(action["Action"]["star"])
            cursor.click(action["Action"]["archive"])
        query2=f'''update job_email set status  = "1", remark = "{percentangeEmailCount} Emails are Proceed Sucessfully!"  where jobid = "{profileid}" and Email="{email}";''' 
        print(query2)
        database.updateDb(query2)
    except Exception as e:
        print('passing excepting in inbox')
        pass

def readSpam(page,data):
    email=str(data[2]).strip()
    print('read all in spam')
    cursor = create_cursor(page)
    xpathAction(page,action["Action"]["spam"])
    a=page.locator(action["Action"]["SpamReadAll"])
    print(a.count())
    for i in range(0,a.count()):
        xpathAction(page,action["Action"]["InboxReadAll"])
        scroll(page)
        xpathAction(page,action["Action"]["backButton"])
    query3=f'''update job_email set status  = "1", remark = "read {a.count()} mail in spam"  where jobid = "{profileid}" and Email="{email}";''' 
    database.updateDb(query3)
    
def readInbox(page,data):
    email=str(data[2]).strip()
    print('read all in inbox')
    cursor = create_cursor(page)    
    xpathAction(page,action["Action"]["inbox"])
    xpathAction(page,action["Action"]["search"])
    search=page.query_selector(action["Action"]["search"])
    search.type('is:unread')
    xpathAction(page,action["Action"]["searchButton"])
    page.wait_for_timeout(3000)
    a=page.locator(action["Action"]["InboxReadAll"])
    print(a.count())
    for i in range(0,a.count()):
        xpathAction(page,action["Action"]["InboxReadAll"])
        scroll(page)
        xpathAction(page,action["Action"]["backButton"])

    query4=f'''update job_email set status  = "1", remark = "read {a.count()} mail in inbox"  where jobid = "{profileid}" and Email="{email}";''' 
    database.updateDb(query4)




def main(url,channel,headless,slowMo,data,profileid):
    with sync_playwright() as p:
        email=str(data[2]).strip()
        print(email)
        browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",channel=channel,headless=False,slow_mo=slowMo,proxy={'server':str(data[4])+":"+str(data[5]),})
        context = browser.new_context(geolocation={"longitude": float(data[12]), "latitude": float(data[11])})
        try:
            context = browser.new_context(storage_state=f"SessionData/{email}.json")
        except Exception as e:
            if not os.path.exists(f"SessionData/{email}.json"):    
                browser.close()
                seedLogin.requestJS(data,profileid)
                browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",channel=channel,headless=False,slow_mo=slowMo,proxy={'server':str(data[4])+":"+str(data[5])})
                context = browser.new_context(geolocation={"longitude": float(data[12]), "latitude": float(data[11])})
                context = browser.new_context(storage_state=f"SessionData/{email}.json")
            pass

        if os.path.exists(f"SessionData/{email}.json"):
            page = context.new_page()
            stealth_sync(page)
            page.goto(login["Login"]["url"])
            timeout(page,15000)
        else:
            print('Error in login!')
        try:
            page.wait_for_selector(action["Action"]["Composed"])
        except Exception as e:
            browser.close()
            seedLogin.requestJS(data,profileid)
            pass

        time.sleep(3)
        if str(config["config"]["ProcessType"]) == "read":
            time.sleep(1)
            if config["config"]["read_inbox"] == "Yes":
                readInbox(page,data)

            if config["config"]["read_spam"] == "Yes":
                readSpam(page,data)

        if str(config["config"]["ProcessType"]) == "notspam":
            print('you are in notspam!!!')
            actionsNS(page,data,profileid)
            actionIB(page,data,profileid)

        context.storage_state(path=f"SessionData/{email}.json")
        browser.close()





if __name__ == '__main__':
    HeaderData=CoreConfig() # get ims_user and password from coreconfig file.
    outData=[]
    jsonObj=getJson()
    profileData=[];tmp=[]
    if not os.path.exists(f'C:\production\\SessionData'):
        os.mkdir(f'C:\production\\SessionData')
    getData=requests.get(f'http://{HeaderData.ims_user}:{HeaderData.password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/checkjob') #checking for job and getting profileID
    for i in getData.json():
        profileid=i["profileid"]
        if not os.path.exists(f"C:\production\\log\\{profileid}"):
            os.mkdir(f"C:\production\\log\\{profileid}")
        if not os.path.exists(f"C:\production\\Selectors\\{profileid}"):
            os.mkdir(f"C:\production\\Selectors\\{profileid}")
        machine_ip=i["machine_ip"]
        machine_user=i["machine_user"]
        if str(os.getlogin().strip()) == str(machine_user).strip():     #Check for machine username like(user001)
            if not i["profileid"]:
                print('The required data from request module is not found! please check/upload data on portal')
            else:
                if i["extrafield"]:
                    json_object = json.dumps(i["extrafield"], indent=4)
                with open(f"C:\production\\Selectors\\{profileid}\\config.json", "w") as outfile:
                    outfile.write(json_object)  #json should be inside Selector folder
                URL=f'''http://{HeaderData.ims_user}:{HeaderData.password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/getjobemail/{i["profileid"]}''' #actual URL
                Data=requests.get(URL)
                action,captcha,config,login,popup=jsonObj.getData(profileid)
        else:
            print("User Selection Mismatched!! Please check login user")
            exit()

    if Data:
        for i in Data.json():
            tmp.append(list(i.values()))
        for i in tmp:
            i.insert(0,"")
            i.insert(0,"")
            profileData.append(i)

    def proxyHandler(data):
        proxy=data[4]
        port=data[5]
        location=loc.geoLoc(proxy,port)
        try:
            latitude=location.split(',')[0]
            longitude=location.split(',')[1]
        except Exception as e:
            latitude=40.71
            longitude=73.95
        data.append(str(latitude))
        data.append(str(longitude))
        outData.append(data)

    

    # for i in profileData:
    #     location=loc.geoLoc(i[4],i[5])
    #     try:
    #         latitude=location.split(',')[0]
    #         longitude=location.split(',')[1]
    #     except Exception as e:
    #         latitude=40.71
    #         longitude=73.95
    #     i.append(str(latitude))
    #     i.append(str(longitude))
    #     outData.append(i)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(proxyHandler,data):data for data in profileData}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data1 = future.result()
            except Exception as exc:
                print('%r generated an exception in proxychecking: %s' % (url, exc))
            else:
                print('getting proxy data!')


    ########### Below code will update database that data has been received for processing ############

    updateSeed=f"update jobs set status = 3 where id = {profileid} and machine_ip='{machine_ip}';"
    database.updateDb(updateSeed)

    ############ Database update Done #######################
    time.sleep(3)
    print(config["config"]["ProcessType"])
    if str(config["config"]["ProcessType"]) == "login":    # checking for ProcessType if process type is login then will jump to login part
        print('In login')
        seedLogin.login(config,outData,profileid)
    time.sleep(3)

    print(config["config"]["ProcessType"])

    if str(config["config"]["ProcessType"]) == "notspam" or str(config["config"]["ProcessType"]) == "read":    # checking for ProcessType if process type is notspam then will jump to not spam part.
        print('true')
        nsData=[]
        dir_list = os.listdir(SessionFilePath)
        dir_list = [w.replace('.json', '') for w in dir_list]
        for i in dir_list:
            for j in outData:
                if i in str(j[2].strip()):
                    nsData.append(j)

        
    
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["config"]["Worker"])) as executor:
            #future_to_url = {executor.submit(main,str(login["Login"]["url"]),str(config["config"]["channel"]),bool(config["config"]["headless"]),int(config["config"]["slowMo"]),data,profileid): data for data in nsData}
            future_to_url = {executor.submit(main,str(login["Login"]["url"]),str(config["config"]["channel"]),bool(config["config"]["headless"]),int(config["config"]["slowMo"]),data,profileid): data for data in nsData}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data1 = future.result()
                except Exception as exc:
                    print('%r generated an exception in jobs: %s' % (url, exc))
                else:
                    print('Done!')