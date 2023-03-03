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
import requests
import time
from coreConfig import CoreConfig
from seedLogin import seedLogin
from playwright.sync_api import expect
import re
import random
list1 = [1, 2, 3, 4, 5, 6]

SessionFilePath=f"C:\production\\SessionData\\"

def xpathAction(page,ElementSelector):
    try:
        page.wait_for_selector(ElementSelector,timeout=10000)
        page.click(ElementSelector)
    except Exception as e:
        print("Exception in xpathAction",e)
        print(ElementSelector)
        pass


def scroll(page):
    for i in range(2):
        page.mouse.wheel(0, 100)
        page.mouse.wheel(100, 300)
        time.sleep(1)

def timeout(page,duration):
    page.wait_for_timeout(duration)

def handlePopup(page,pop,popupLen):
    for i in range(5):
        try:
            page.click(pop,timeout=1000)
        except Exception as e:
            pass

def getEmailCount(page,data,profileid):
    email=str(data[2]).strip()
    page.wait_for_selector(action["Action"]["Composed"])
    xpathAction(page,action["Action"]["spam"])
    spamSubject=str(data[8].strip())
    SpamSubjectSelector=str(action["Action"]["SpamSubjectSelector"])
    Sub=SpamSubjectSelector.replace('__Subject',str(spamSubject))
    a=page.locator(Sub)
    page.wait_for_timeout(3000)
    SpamCount=a.count()
    page.wait_for_selector(action["Action"]["inbox"])
    xpathAction(page,action["Action"]["inbox"])
    b=page.locator(Sub)
    page.wait_for_timeout(3000)
    InboxCount=b.count()
    print("################################################################################################")
    print(SpamCount)
    print(InboxCount)
    print("################################################################################################")
    query6=f'''update job_email set spam_count={SpamCount},inbox_count={InboxCount} where jobid='{profileid}' and Email='{email}';'''
    print(query6)
    database.updateDb(query6)


def inbox_archive(page):
    xpathAction(page,action["Action"]["archive"])
    # try:
    #     handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
    # except Exception as e:
    #     pass

def inbox_star(page):
    try:
        xpathAction(page,action["Action"]["SectionElm"])
    except Exception as e:
        pass
    # xpathAction(page,action["Action"]["star"])
    page.keyboard.type("L")
    try:
        xpathAction(page,action["Action"]["star"])
    except Exception as e:
        pass

def inbox_delete(page):
    xpathAction(page,action["Action"]["delete"])

def inbox_add_contact(page):
    xpathAction(page,action["Action"]["SectionElm"])
    page.wait_for_timeout(1500)
    xpathAction(page,action["Action"]["addSenderToContact"])

def spam_restore_inbox(page):
    xpathAction(page,action["Action"]["RestoreToInbox"])

def spam_move_inbox(page):
    xpathAction(page,action["Action"]["move"])
    page.wait_for_timeout(1500)
    xpathAction(page,action["Action"]["moveToInbox"])

def spam_delete(page):
    xpathAction(page,action["Action"]["delete"])

def spam_notspam(page):
    xpathAction(page,action["Action"]["notSpam"])  

def spam_star(page):
    xpathAction(page,action["Action"]["star"])

def reply_Email(page):

    xpathAction(page,action["Action"]["ReplyEmail"])
    textEmail=page.query_selector(action["Action"]["ReplyArea"])
    textEmail.type(action["Action"][f"Reply{random.choice(list1)}"])
    xpathAction(page,action["Action"]["SendButton"])

def processSpam(page,data,profileid,subjectType,SpamPercentCount,SpamNsType,SpamAction):
    # handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
    getEmailCount(page,data,profileid)
    email=str(data[2]).strip()
    if '%' in SpamPercentCount:
        CountSpamInPercentage=int(str(SpamPercentCount).replace('%',''))
    else:
        CountSpamInCount=int(SpamPercentCount)

    if subjectType == 'without_sub' and SpamNsType == 'all':
        print("SPAM:subjectType == 'without_sub' and SpamNsType == 'all'")
        cursor = create_cursor(page)
        cursor.click(action["Action"]["spam"])
        page.wait_for_timeout(3000)
        # handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        xpathAction(page,action["Action"]["spam"])
        # scroll(page)
        # scroll(page)
        xpathAction(page,action["Action"]["SelectALL"])
        page.wait_for_timeout(1000)
        print(SpamAction,type(SpamAction))
        if str('spam_star') in SpamAction:
            xpathAction(page,action["Action"]["SectionElm"])
            spam_star(page)
        if str('spam_restore_inbox') in SpamAction:
            spam_restore_inbox(page)
        if str('spam_move_inbox') in SpamAction:
            spam_move_inbox(page)
        if str('spam_notspam') in SpamAction:
            spam_notspam(page)
        if str('spam_delete') in SpamAction:
            spam_delete(page)
        query1=f'''update job_email set status  = "1" , remark = concat(remark,"\n All Selected Emails in Spam are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query1)
    if subjectType == 'without_sub' and SpamNsType == 'one':
        print("SPAM: subjectType == 'without_sub' and SpamNsType == 'one'")
        page.wait_for_timeout(1000)
        page.click(action["Action"]["spam"])
        a=page.locator(action["Action"]["SpamReadAll"])
        page.wait_for_timeout(3000)
        if CountSpamInPercentage:
            percentangeEmailCount=int(CountSpamInPercentage/100*a.count())
        else:
            percentangeEmailCount=CountSpamInCount
        for i in range(0,percentangeEmailCount):
            xpathAction(page,action["Action"]["SpamReadAll"])
            scroll(page)
            if str('spam_star') in SpamAction:
                spam_star(page)
            if str('spam_restore_inbox') in SpamAction:
                spam_restore_inbox(page)
            if str('spam_move_inbox') in SpamAction:
                spam_move_inbox(page)
            if str('spam_notspam') in SpamAction:
                spam_notspam(page)
            if str('spam_delete') in SpamAction:
                spam_delete(page)
        query2=f'''update job_email set status  = "1" , remark = concat(remark,"\n {percentangeEmailCount} Emails are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query2)
    if subjectType == 'with_sub' and SpamNsType == 'all':
        print("SPAM: subjectType == 'with_sub' and SpamNsType == 'all'")
        email=str(data[2]).strip()
        xpathAction(page,action["Action"]["inbox"])
        xpathAction(page,action["Action"]["search"])
        search=page.query_selector(action["Action"]["search"])
        search.type(f'in:bulk is:unread')
        xpathAction(page,action["Action"]["searchButton"])
        page.wait_for_timeout(3000)
        print('handling popup')
        handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        print('handling popup Done')
        scroll(page)
        xpathAction(page,action["Action"]["SelectALL"])
        xpathAction(page,action["Action"]["SectionElm"])
        if str('spam_star') in SpamAction:
            spam_star(page)

        if str('spam_restore_inbox') in SpamAction:
            spam_restore_inbox(page)
            handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        if str('spam_move_inbox') in SpamAction:
            spam_move_inbox(page)
            handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        if str('spam_notspam') in SpamAction:
            spam_notspam(page)
            handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        if str('spam_delete') in SpamAction:
            spam_delete(page)     
            handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))   
        query3=f'''update job_email set status  = "1" , remark = concat(remark,"\n All Selected Emails in Spam are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query3)

    if subjectType == 'with_sub' and SpamNsType == 'one':
        print("SPAM: subjectType == 'with_sub' and SpamNsType == 'one'")
        email=str(data[2]).strip()
        cursor = create_cursor(page)
        # handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        page.wait_for_selector(action["Action"]["Composed"])
        xpathAction(page,action["Action"]["spam"])
        try:
            spamSubject=str(data[8].strip())
            SpamSubjectSelector=str(action["Action"]["SpamSubjectSelector"])
            Sub=SpamSubjectSelector.replace('__Subject',str(spamSubject))
            a=page.locator(Sub)
            page.wait_for_timeout(3000)
            if CountSpamInPercentage:
                percentangeEmailCount=int(CountSpamInPercentage/100*a.count())
            else:
                percentangeEmailCount=CountSpamInCount
            print("CountSpamInPercentage",CountSpamInPercentage)
            print("percentangeEmailCount",percentangeEmailCount)
            for i in range(0,percentangeEmailCount):
                xpathAction(page,Sub)
                scroll(page)
                if str('spam_star') in SpamAction:
                    spam_star(page)
                if str('spam_restore_inbox') in SpamAction:
                    spam_restore_inbox(page)
                if str('spam_move_inbox') in SpamAction:
                    spam_move_inbox(page)
                if str('spam_notspam') in SpamAction:
                    spam_notspam(page)
                if str('spam_delete') in SpamAction:
                    spam_delete(page)                 
                timeout(page,1000)
            query4=f'''update job_email set status  = "1" , remark = concat(remark,"\n {percentangeEmailCount} Emails are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
            database.updateDb(query4)
        except Exception as e:
            print("Exception in actionNS")

def processInbox(page,data,profileid,subjectType,InboxPercentCount,InboxNSType,InboxAction):
    email=str(data[2]).strip()
    CountSpamInPercentage=''
    print("InboxPercentCount",InboxPercentCount)
    if '%' in InboxPercentCount:
        CountSpamInPercentage=int(str(InboxPercentCount).replace('%',''))
    else:
        CountSpamInCount=int(InboxPercentCount)
    
    if subjectType == 'without_sub' and InboxNSType == 'all':
        print("INBOX: subjectType == 'without_sub' and InboxNSType == 'all'")
        email=str(data[2]).strip()
        cursor = create_cursor(page)
        xpathAction(page,action["Action"]["inbox"])
        page.wait_for_timeout(3000)
        # handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        xpathAction(page,action["Action"]["SelectALL"])
        xpathAction(page,action["Action"]["SectionElm"])
        xpathAction(page,action["Action"]["markAsRead"])
        xpathAction(page,action["Action"]["SelectALL"])
        page.wait_for_timeout(2000)
    
        if str('inbox_star') in InboxAction:
            xpathAction(page,action["Action"]["SectionElm"])
            inbox_star(page)
        if str('inbox_archive') in InboxAction:
            xpathAction(page,action["Action"]["SelectALL"])
            inbox_archive(page)
        if str('inbox_delete') in InboxAction:
            xpathAction(page,action["Action"]["SelectALL"])
            inbox_delete(page)
        query5=f'''update job_email set status  = "1" , remark = concat(remark,"\n All Selected Emails in Inbox are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query5)

    if subjectType == 'without_sub' and InboxNSType == 'one':
        print("INBOX: subjectType == 'without_sub' and InboxNSType == 'one'")
        email=str(data[2]).strip()
        cursor = create_cursor(page)
        xpathAction(page,action["Action"]["inbox"])
        page.wait_for_timeout(3000)
        # handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        if CountSpamInPercentage:
            percentangeEmailCount=int(CountSpamInPercentage/100*a.count())
        else:
            percentangeEmailCount=CountSpamInCount
        print(percentangeEmailCount)
        for i in range(1,percentangeEmailCount+1):
            if str('inbox_star') in InboxAction and str('inbox_archive') not in InboxAction:
                xpathAction(page,f'(//span[@data-test-id="message-subject"])[{i}]')
                scroll(page)
                if config["config"]["reply_mail"] == "yes":
                    reply_Email(page)
                inbox_star(page)
            if str('inbox_archive') in InboxAction and str('inbox_star') in InboxAction:
                xpathAction(page,f'//span[@data-test-id="message-subject"]')
                scroll(page)
                if config["config"]["reply_mail"] == "yes":
                    reply_Email(page)
                inbox_star(page)
                inbox_archive(page)
            if str('inbox_delete') in InboxAction:
                xpathAction(page,f'//span[@data-test-id="message-subject"]')
                scroll(page)
                inbox_delete(page)
        query6=f'''update job_email set status  = "1" , remark = concat(remark,"\n {percentangeEmailCount} Emails are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query6)
    if subjectType == 'with_sub' and InboxNSType == 'all':
        print("INBOX: subjectType == 'with_sub' and InboxNSType == 'all'")
        email=str(data[2]).strip()
        cursor = create_cursor(page)     
        xpathAction(page,action["Action"]["inbox"])
        page.wait_for_timeout(3000)
        xpathAction(page,action["Action"]["search"])
        search=page.query_selector(action["Action"]["search"])
        search.type(f'subject:{str(data[8].strip())}')
        xpathAction(page,action["Action"]["searchButton"])
        page.wait_for_timeout(3000)
        handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        scroll(page)
        xpathAction(page,action["Action"]["SelectALL"])
        xpathAction(page,action["Action"]["SectionElm"])
        xpathAction(page,action["Action"]["markAsRead"])       
        xpathAction(page,action["Action"]["SelectALL"])
        xpathAction(page,action["Action"]["SectionElm"])
        print('**********************************',InboxAction)
        if str('inbox_star') in InboxAction:
            inbox_star(page)
            page.wait_for_timeout(2000)
        if str('inbox_archive') in InboxAction:
            inbox_archive(page)
        if str('inbox_delete') in InboxAction:
            inbox_delete(page)
        query7=f'''update job_email set status  = "1" , remark = concat(remark,"\n All Selected Emails in Inbox are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query7)

    if subjectType == 'with_sub' and InboxNSType == 'one':
        print("INBOX: subjectType == 'with_sub' and InboxNSType == 'one'")
        spamSubject=str(data[8].strip())
        email=str(data[2]).strip()
        cursor = create_cursor(page)
        xpathAction(page,action["Action"]["inbox"])
        page.wait_for_timeout(3000)
        handlePopup(page,popup["popUp"]["allPopUp"],list(popup["popUp"]["allPopUp"].split('|')))
        SpamSubjectSelector=str(action["Action"]["SpamSubjectSelector"])
        Sub=SpamSubjectSelector.replace('__Subject',str(spamSubject))
        a=page.locator(Sub)
        if CountSpamInPercentage:
            percentangeEmailCount=int(CountSpamInPercentage/100*a.count())
        else:
            percentangeEmailCount=CountSpamInCount

        for i in range(1,percentangeEmailCount+1):
            if str('inbox_star') in InboxAction and str('inbox_archive') not in InboxAction:
                xpathAction(page,f'({Sub})[{i}]')
                if config["config"]["reply_mail"] == "yes":
                    reply_Email(page)
                inbox_star(page)
            if str('inbox_archive') in InboxAction and str('inbox_star') in InboxAction:
                xpathAction(page,Sub)
                scroll(page)
                if config["config"]["reply_mail"] == "yes":
                    reply_Email(page)
                inbox_star(page)
                inbox_archive(page)
            if str('inbox_delete') in InboxAction:
                xpathAction(page,Sub)
                scroll(page)
                inbox_delete(page)
        query8=f'''update job_email set status  = "1" , remark = concat(remark,"\n {percentangeEmailCount} Emails are Proceed Sucessfully!")  where jobid = "{profileid}" and Email="{email}";''' 
        database.updateDb(query8)

def addContacts(page,data,profileid):
    a=str(data[11])
    print(a)
    for i in a.split("|"):
        users=str(i).split('@')[0]
        xpathAction(page,action["Action"]["Contacts"])
        xpathAction(page,action["Action"]["AllContacts"])
        xpathAction(page,action["Action"]["NewContacts"])
        xpathAction(page,action["Action"]["AddNewContacts"])
        firstName=page.query_selector(action["Action"]["FirstName"])
        firstName.type(users)
        ContactEmail=page.query_selector(action["Action"]["Email"])
        ContactEmail.type(i)
        xpathAction(page,action["Action"]["Save"])
        xpathAction(page,action["Action"]["Contacts"])
        


def main(url,channel,headless,slowMo,data,profileid,config):
    with sync_playwright() as p:
        email=str(data[2]).strip()
        password=str(data[3]).strip()
        print(password)
        browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",channel=channel,headless=False,slow_mo=slowMo,proxy={'server':str(data[4])+":"+str(data[5]),'username':'h4eylf1iebdh94cs6avvpxc','password':'RNW78Fm5'})
        context = browser.new_context(geolocation={"longitude": float(data[13]), "latitude": float(data[12])})
        try:
            context = browser.new_context(storage_state=f"SessionData/{email}.json")
        except Exception as e:
            if not os.path.exists(f"SessionData/{email}.json"):
                browser.close()
                seedLogin.requestJS(data,profileid,config)
                browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe",channel=channel,headless=False,slow_mo=slowMo,proxy={'server':str(data[4])+":"+str(data[5])})
                context = browser.new_context(geolocation={"longitude": float(data[13]), "latitude": float(data[12])})
                context = browser.new_context(storage_state=f"SessionData/{email}.json")
            pass

        if os.path.exists(f"SessionData/{email}.json"):
            page = context.new_page()
            stealth_sync(page)
            try:
                page.goto(login["Login"]["url"])
            except Exception as e:
                print('Proxy is slow loading second time.....')
                page.goto(login["Login"]["url"],timeout=180000)
            try:
                print('logged out')
                page.wait_for_selector("//a[@name='username' and contains(@data-email,'yahoo.com')]")
                print('logout user test')
                page.click("//a[@name='username' and contains(@data-email,'yahoo.com')]")
                page.wait_for_timeout(1000)
                password=page.query_selector(login["Login"]["LoginPassword"])
                password.type(str(data[3]).strip())
                page.click('text=Next')
                page.wait_for_timeout(3000)
                try:
                    page.wait_for_selector("//a[contains(text(),'Remind me') and contains(text(),'later')]")
                    xpathAction(page,"//a[contains(text(),'Remind me') and contains(text(),'later')]")
                except Exception as e:
                    pass
                page.wait_for_timeout(3000)
            except Exception as e:
                pass
        else:
            print('Error in login!')
        try:
            page.wait_for_selector(action["Action"]["Composed"])
        except Exception as e:
            query=f'''update job_email set status  = "2", remark = "Yahoo unable to recognized this email id or moight be logged out" where jobid = "{profileid}" and Email = "{email}";'''
            database.updateDb(query)
            browser.close()
            #seedLogin.requestJS(data,profileid,config)
            pass

        if str(config["config"]["ProcessType"]) == "read":
            if config["config"]["read_inbox"] == "Yes":
                readInbox(page,data)

            if config["config"]["read_spam"] == "Yes":
                readSpam(page,data)


        if str(config["config"]["ProcessType"]) == "notspam":
            subjectType=config["config"]["subject"]
            SpamPercentCount=config["config"]["spam_percentage_count"]
            SpamNsType=config["config"]["spam_ns_type"]
            SpamAction=config["config"]["spam_action"]
            InboxPercentCount=config["config"]["inbox_percentage_count"]
            InboxNSType=config["config"]["inbox_ns_type"]
            InboxAction=config["config"]["inbox_action"]

            processSpam(page,data,profileid,subjectType,SpamPercentCount,SpamNsType,SpamAction)
            page.wait_for_timeout(4000)
            processInbox(page,data,profileid,subjectType,InboxPercentCount,InboxNSType,InboxAction)
            page.wait_for_timeout(4000)

        if str(config["config"]["ProcessType"]) == "addContacts":
            print('you arte here!')
            addContacts(page,data,profileid)


        context.storage_state(path=f"SessionData/{email}.json")
        browser.close()

if __name__ == '__main__':
    HeaderData=CoreConfig() # get ims_user and password from coreconfig file.
    outData=[]
    jsonObj=getJson()
    profileData=[];tmp=[]
    systemUser=str(os.getlogin().strip())
    if not os.path.exists(f'C:\production\\SessionData'):
        os.mkdir(f'C:\production\\SessionData')
    getData=requests.get(f'http://ns.codemskyapp.com/NotSpam/notspam_api/checkjob/{systemUser}') #checking for job and getting profileID
    
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
                URL=f'''http://ns.codemskyapp.com/NotSpam/notspam_api/getjobemail/{i["profileid"]}''' #actual URL
                Data=requests.get(URL)
                action,captcha,config,login,popup=jsonObj.getData(profileid)
                
        else:
            print("User Selection Mismatched!! Please check login user")
            exit()
    print(Data.json())
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

    


    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
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
    
    if str(config["config"]["ProcessType"]) == "login":    # checking for ProcessType if process type is login then will jump to login part
        print("############################**********************************##############################")
        print(outData)
        print('In login')
        seedLogin.login(config,outData,profileid)
    
    time.sleep(3)

    

    if str(config["config"]["ProcessType"]) == "notspam" or str(config["config"]["ProcessType"]) == "read" or str(config["config"]["ProcessType"]) == "addContacts":    # checking for ProcessType if process type is notspam then will jump to not spam part.
        nsData=[]
        dir_list = os.listdir(SessionFilePath)
        dir_list = [w.replace('.json', '') for w in dir_list]
        for i in dir_list:
            for j in outData:
                if str(i) == str(j[2].strip()):
                    nsData.append(j)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["config"]["Worker"])) as executor:
            #future_to_url = {executor.submit(main,str(login["Login"]["url"]),str(config["config"]["channel"]),bool(config["config"]["headless"]),int(config["config"]["slowMo"]),data,profileid): data for data in nsData}
            future_to_url = {executor.submit(main,str(login["Login"]["url"]),str(config["config"]["channel"]),bool(config["config"]["headless"]),int(config["config"]["slowMo"]),data,profileid,config): data for data in nsData}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data1 = future.result()
                except Exception as exc:
                    print(f"\n [ Error ]  >>  {type(exc).__name__} at line {exc.__traceback__.tb_lineno} of {__file__}: {exc}")
                    print('%r generated an exception in jobs: %s' % (url, exc))
                else:

                    print('Done!')