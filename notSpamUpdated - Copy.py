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


filePath=os.path.dirname(os.path.abspath(__file__))
SessionFilePath=filePath+"\SessionData\\"

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

def handlePopup(page,popup):
    try:
        page.wait_for_selector("//button[@title='Done']")
        page.click("//button[@title='Done']")
        
    except Exception as e:
        print(f"\n [ Error ]  >>  {type(e).__name_} at line {e.__traceback__.tb_lineno} of {_file__}: {e}")
        print("Exceptions in popup")


def scroll(page):
    for i in range(5):
        page.mouse.wheel(0, 100)
        page.mouse.wheel(100, 300)
        time.sleep(2)


def actionsNS(page,data,profileid):
    email=str(data[2]).strip()
    cursor = create_cursor(page)
    # if bool(config["config"]["handlePopup"]):
    #     handlePopup(page,list[popup["popUp"]["themesPopup"]])
    page.wait_for_selector(action["Action"]["Composed"])
    xpathAction(page,action["Action"]["spam"])
    try:
        spamSubject=str(data[8].strip())
        print("spamSubject",spamSubject)
        SpamSubjectSelector=str(action["Action"]["SpamSubjectSelector"])
        print("SpamSubjectSelector",SpamSubjectSelector)
        Sub=SpamSubjectSelector.replace('__Subject',str(spamSubject))
        a=page.locator(Sub)
        page.wait_for_timeout(60000)
        if config["config"]["spam_percentage"]:     #10/100 * 80 = X
            percentangeEmailCount=int((int(config["config"]["spam_percentage"])/100*a.count()))
        else:
            percentangeEmailCount=a.count()
        for i in range(0,percentangeEmailCount):
            xpathAction(page,Sub)
            scroll(page)
            xpathAction(page,action["Action"]["notSpam"])
            timeout(page,5000)
            query=f'''update job_email set status  = "1" and remark = "Spam Read {a.count()}"  where jobid = "{profileid}" and Email="{email}";'''
            print(query)
            database.updateDb(query)
    except Exception as e:
        print("Exception in actionNS")

def actionIB(page,data,profileid):
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
            query=f'''update job_email set status  = "1", remark = "Not Spam done{a.count()}"  where jobid = "{profileid}" and Email="{email}";''' 
            print(query)
            database.updateDb(query)
    except Exception as e:
        pass


def readSpam(page):
    print('read all in spam')
    cursor = create_cursor(page)
    xpathAction(page,action["Action"]["spam"])
    a=page.locator(action["Action"]["SpamReadAll"])
    print(a.count())
    for i in range(0,a.count()):
        xpathAction(page,action["Action"]["InboxReadAll"])
        scroll(page)
        xpathAction(page,action["Action"]["backButton"])

    
def readInbox(page):
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

    





def main(url,channel,headless,slowMo,data,profileid):
    with sync_playwright() as p:
        email=str(data[2]).strip()
        print(email)
        browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",channel=channel,headless=False,slow_mo=slowMo,proxy={'server':str(data[4])+":"+str(data[5])})
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
            timeout(page,10000)
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
                readInbox(page)

            if config["config"]["read_spam"] == "Yes":
                readSpam(page)

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
    action,captcha,config,login,popup=jsonObj.getData() #get required Json data.

    while 1:        # this loop is continues for checking task
        profileData=[];tmp=[]
        getData=requests.get(f'http://{HeaderData.ims_user}:{HeaderData.password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/checkjob') #checking for job and getting profileID
        for i in getData.json():
            profileid=i["profileid"]
            machine_ip=i["machine_ip"]
            machine_user=i["machine_user"]
            if str(os.getlogin().strip()) == str(machine_user).strip():     #Check for machine username like(user001)
                if not i["profileid"]:
                    print('The required data from request module is not found! please check/upload data on portal')
                else:
                    if i["extrafield"]:
                        json_object = json.dumps(i["extrafield"], indent=4)
                    with open("Selectors/config.json", "w") as outfile:
                       outfile.write(json_object)  #json should be inside Selector folder
                    URL=f'''http://{HeaderData.ims_user}:{HeaderData.password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/getjobemail/{i["profileid"]}''' #actual URL
                    Data=requests.get(URL)
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

        for i in profileData:
            location=loc.geoLoc(i[4],i[5])
            try:
                latitude=location.split(',')[0]
                longitude=location.split(',')[1]
            except Exception as e:
                latitude=40.71
                longitude=73.95
            i.append(str(latitude))
            i.append(str(longitude))
            outData.append(i)

        ########### Below code will update database that data has been received for processing ############

        # updateSeed=f"update jobs set status = 3 where id = {profileid} and machine_ip='{machine_ip}';"
        # database.updateDb(updateSeed)

        ############ Database update Done #######################
        time.sleep(3)
        print(config["config"]["ProcessType"])
        if str(config["config"]["ProcessType"]) == "login":    # checking for ProcessType if process type is login then will jump to login part
            print('In login')
            seedLogin.login(config,outData,profileid)
        time.sleep(3)
        if str(config["config"]["ProcessType"]) == "notspam" or str(config["config"]["ProcessType"]) == "read":    # checking for ProcessType if process type is notspam then will jump to not spam part.
            nsData=[]
            dir_list = os.listdir(SessionFilePath)
            dir_list = [w.replace('.json', '') for w in dir_list]
            for i in dir_list:
                for j in outData:
                    if i in str(j[2].strip()):
                        nsData.append(j)
                        
        
            
        
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["config"]["Worker"])) as executor:
                future_to_url = {executor.submit(main,str(login["Login"]["url"]),str(config["config"]["channel"]),bool(config["config"]["headless"]),int(config["config"]["slowMo"]),data,profileid): data for data in nsData}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data1 = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))
                    else:
                        print('Done!')

        
        time.sleep(120)


    