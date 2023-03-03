import concurrent.futures
from database import database
import os
import time

captchaAccount={'sachin': '8fc14d6a0b99cf6ecbc466c9ff1fb531', 'karthic': '9fdc79839941bdca3150c7f4a97eb388','diler':'1e66cf5d82b6e8c2ff2c5d6150f50963','pankaj':'94793df8c9040aa7bf531ae46c5e5770','deva':'e15ea81485bf0a42c168dc5af8469b38','jaydeep':'e5ee5f62dd3f51e8613d3ac6e1304a4c','nitin':'08f6386de67b12608565f608501d4933','pawan':'2cb05ba458d0ad0ebe9585303fd0f951','yogesh':'71a69a55b457b4417906bc49e333d4ac'}

#filePath=os.path.dirname(os.path.abspath(__file__))
SessionFilePath=f"C:\production\\SessionData\\"

class seedLogin():
    def requestJS(data,profileid,config):
        entity=config["config"]["Entity"]
        email=str(data[2].strip())
        password=str(data[3].strip())
        proxy=data[4]
        port=data[5]
        longitude=data[13]
        latitude=data[12]
        
        if entity == "Team A" or entity == "Team F" or entity == "Team L" or entity == "Team M" or entity == "Team S":
            captchaEntity=captchaAccount["sachin"]
        elif entity == "Team B" or entity == "Team G" or entity == "Team H" or entity == "Team I" or entity == "Team K" or entity == "Team T":
            captchaEntity=captchaAccount["karthic"]
        elif entity == "Team E" or entity == "Team Q":
            captchaEntity=captchaAccount["jaydeep"]
        elif entity == "Team J" or entity == "Team O":
            captchaEntity=captchaAccount["deva"]
        elif entity == "Team P":
            captchaEntity=captchaAccount["pankaj"]
        elif entity == "Team X":
            captchaEntity=captchaAccount["diler"]
        elif entity == "Team U":
            captchaEntity=captchaAccount["pawan"]
        elif entity == "Team V":
            captchaEntity=captchaAccount["yogesh"]
        else:
            captchaEntity=captchaAccount["nitin"]
        
        os.system(f"node y7.js {email} {password} {proxy} {port} {longitude} {latitude} {profileid} {captchaEntity}")
        time.sleep(2)
        emailId=[]
        #dir_list = os.listdir(SessionFilePath)
        #dir_list = [w.replace('.json', '') for w in dir_list]
        if os.path.exists(SessionFilePath+email+".json"):
            query=f'''update job_email set status  = "1", remark = "Login Sucessful" where jobid = "{profileid}" and Email = "{email}";''' 
            database.updateDb(query)
        else:
            query=f'''update job_email set status  = "2", remark = "Login Failed" where jobid = "{profileid}" and Email = "{email}";''' 
            database.updateDb(query)
        # for i in data:
        #     emailId.append(str(i[2]).strip())
            
        # finalList=set(emailId)-set(dir_list)
        
        # database.updateDb(query)
        

    def login(config,outData,profileid):
        with concurrent.futures.ThreadPoolExecutor(max_workers=int(config["config"]["Worker"])) as executor:
            future_to_url = {executor.submit(seedLogin.requestJS,data,profileid,config): data for data in outData}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data1 = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print('Done!')
                    
        time.sleep(1)

        exit()
        # for i in outData:
        #     emailId.append(str(i[2]).strip())
            
        # finalList=set(emailId)-set(dir_list)
        # query=f'''update job_email set status  = "2", remark = "Login2 Failed" where jobid = "{profileid}" and Email in {str(finalList).replace('{','(').replace('}',')')};''' 
        # database.updateDb(query)
