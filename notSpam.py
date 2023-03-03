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
import calculation

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




def handleLogs(status,remark,jobid,Email):
    pass


def actionsNS(page,data):
    cursor = create_cursor(page)
    # if bool(config["config"]["handlePopup"]):
    #     handlePopup(page,list[popup["popUp"]["themesPopup"]])
    page.wait_for_selector(action["Action"]["Composed"])
    xpathAction(page,action["Action"]["spam"])
    try:
        spamSubject=str(action["Action"]["Subject"])
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
            for i in range(5):                      #mouse scrolling
                page.mouse.wheel(0, 15000)
                time.sleep(2)
                i += 1
            xpathAction(page,action["Action"]["notSpam"])
            timeout(page,5000)

    except Exception as e:
        print("Exception in actionNS")

def actionIB(page):
    try:
        spamSubject=str(action["Action"]["Subject"])
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
    except Exception as e:
        pass


def readInbox(page):
    handlePopup(page,list[popup["popUp"]["themesPopup"]])
    page.wait_for_selector(action["Action"]["inbox"])
    cursor = create_cursor(page)
    cursor.click(action["Action"]["inbox"])
    a=page.locator(action["Action"]["InboxReadAll"])
    for i in range(0,a.count()):
        xpathAction(page,action["Action"]["InboxReadAll"])
        for i in range(5):                      #mouse scrolling
                page.mouse.wheel(0, 15000)
                time.sleep(2)
                i += 1

def readSpam(page):
    cursor = create_cursor(page)
    handlePopup(page,list[popup["popUp"]["themesPopup"]])
    page.wait_for_selector(action["Action"]["Composed"])
    xpathAction(page,action["Action"]["spam"])
    a=page.locator(action["Action"]["SpamReadAll"])
    for i in range(0,a.count()):
        xpathAction(page,action["Action"]["SpamReadAll"])
        for i in range(5):
            page.mouse.wheel(0, 15000)
            time.sleep(2)
            i +=1
        
# def SessionLogin(page,data):
#     try:
#         xpathAction(page,login["Login"]["Login"])
#         xpathAction(page,login["Login"]["userName"])
#         user=page.query_selector(login["Login"]["userName"])
#         user.type(str(data[2]).strip())
#         page.click('text=Next')
#         print("Done!")
#         timeout(page,50000)
#         page.wait_for_selector(login["Login"]["LoginPassword"])
#         password=page.query_selector(login["Login"]["LoginPassword"])
#         password.type(str(data[3]).strip())
#         page.click('text=Next')
#         timeout(page,10000)
#     except Exception as e:
#         print(f"\n [ Error ]  >>  {type(e).__name_} at line {e.__traceback__.tb_lineno} of {_file__}: {e}")
#         pass


def main(url,channel,headless,slowMo,data):
    with sync_playwright() as p:
        email=str(data[2]).strip()
        browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",channel=channel,headless=False,slow_mo=slowMo,proxy={'server':str(data[4])+":"+str(data[5])})
        context = browser.new_context(geolocation={"longitude": float(data[12]), "latitude": float(data[11])})
        try:
            context = browser.new_context(storage_state=f"SessionData/{email}.json")
        except Exception as e:
            if not os.path.exists(f"SessionData/{email}.json"):    
                browser.close()
                requestAPI(data)
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
            f = open("logs", "a")
            f.write(f"LoginFailed for {email}")
            f.close()

        try:
            page.wait_for_selector(action["Action"]["Composed"])
        except Exception as e:
            browser.close()
            pass

        if config["config"]["read_inbox"] == "Yes":
            readInbox(page)
        if config["config"]["read_spam"] == "Yes":
            readSpam(page)

        actionsNS(page,data)
        actionIB(page)

        context.storage_state(path=f"SessionData/{email}.json")
        browser.close()

def requestAPI(data,profileid):
    email=str(data[2]).strip()
    # if not os.path.exists(f"SessionData/{email}.json"):
    #     reqUrl = "http://127.0.0.1:8888/yahooLogin"
    #     headersList = {
    #     "Accept": "*/*",
    #     "Content-Type": "application/json" 
    #     }
    #     payload = json.dumps({
    #     "email":str(data[2].strip()),
    #     "password":str(data[3].strip()),
    #     "proxy":data[4],
    #     "port":data[5],
    #     "longitude": data[12], 
    #     "latitude": data[11]
    #     })      
    # response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
    print('test')

if __name__ == '__main__':
    user='ims_user'
    password='oD1W$paXo'
    outData=[]
    proxyList={}


    jsonObj=getJson()
    action,captcha,config,login,popup=jsonObj.getData() #get JSON data

    # for i in output:
    #     proxyList[i[4]]=i[5]
    # workingProxy=proxyChecking.is_bad_proxy(proxyList)

    # dataObj=getSQLDATA()
    # ProfileData=dataObj.getProfileData(str(config["config"]["profileID"]))  #get mysqldata based on profile id, located in config.json

    # print(ProfileData)
    # print(type(ProfileData))
    
###############################################################################
    while 1:
        profileData=[]
        tmp=[]
        profileid=""
        machine_ip=""
        machine_user=""
        getData=requests.get(f'http://{user}:{password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/checkjob') #checking for job and getting profileID
        print(getData.json())
        for i in getData.json():
            profileid=i["profileid"]
            machine_ip=i["machine_ip"]
            machine_user=i["machine_user"]
            if str(os.getlogin().strip()) == str(machine_user).strip():
                if not i["profileid"]:
                    print("no Data")
                else:
                    if i["extrafield"]:
                        json_object = json.dumps(i["extrafield"], indent=4)
                    with open("Selectors/config.json", "w") as outfile:
                        outfile.write(json_object)  #json should be inside Selector folder
                        
                    URL=f'''http://{user}:{password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/getjobemail/{i["profileid"]}''' #actual URL
                    #testingURL=f'''http://{user}:{password}@web.codemskyapp.com/app/data/NotSpam/notspam_api/getjobemail/19'''
                    Data=requests.get(URL)
            else:
                exit()
                print("User selection mismatch!")

        if Data:
            print(Data.json())
        else:
            print("No Data")
            exit()

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
        
        
        
        
############################################################LOGIN###############################
        # updateSeed=f"update jobs set status = 3 where id = {profileid} and machine_ip='{machine_ip}';"
        # database.updateDb(updateSeed)

        if str(config["config"]["ProcessType"]) == "login":
        

            with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["config"]["Worker"])) as executor:
                future_to_url = {executor.submit(requestAPI,data,profileid): data for data in outData}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data1 = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))
                    else:
                        print('Done!')
            
            emailid=[]
            
            dir_list = os.listdir(SessionFilePath)
            query=f'''update job_email set status  = "1", remark = "Login Sucessful" where jobid = "{profileid}" and Email in {str(dir_list).replace('[','(').replace(']',')').replace('.json','')};''' 
            database.updateDb(query)
            
            dir_list = [w.replace('.json', '') for w in dir_list]
            
                
            
            for i in outData:
                emailid.append(str(i[2]).strip())
            finalList=set(emailid)-set(dir_list)
            print('**************************************')
            query=f'''update job_email set status  = "2", remark = "Login Failed" where jobid = "{profileid}" and Email in {str(finalList).replace('{','(').replace('}',')')};''' 
            database.updateDb(query)
            exit()
        else:
        
            with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["config"]["Worker"])) as executor:
                future_to_url = {executor.submit(main,str(login["Login"]["url"]),str(config["config"]["channel"]),bool(config["config"]["headless"]),int(config["config"]["slowMo"]),data): data for data in outData}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data1 = future.result()
                    except Exception as exc:
                        print('%r generated an exception: %s' % (url, exc))
                    else:
                        print('Done!')


        time.sleep(120)



# # asyncio.run(main())

