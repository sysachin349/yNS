import os
import json
#filePath=os.path.dirname(os.path.abspath(__file__))
SelectorFilePath=f"C:\production\\Selectors\\"



class getJson():
    def getData(self,profileid):
        SelectorFilePathforConfig=f"C:\production\\Selectors\\{profileid}\\"  # this path is necessary for config loading only.
        with open(SelectorFilePath+"action.json") as Jfile:
            self.action=Jfile.read()
            self.action=json.loads(self.action)
            Jfile.close()
        with open(SelectorFilePath+"captcha.json") as Jfile:
            self.captcha=Jfile.read()
            self.captcha=json.loads(self.captcha)
            Jfile.close()
        with open(SelectorFilePathforConfig+"config.json") as Jfile:
            self.config=Jfile.read()
            self.config=json.loads(self.config)
            Jfile.close()
        with open(SelectorFilePath+"login.json") as Jfile:
            self.login=Jfile.read()
            self.login=json.loads(self.login)
            Jfile.close()
        with open(SelectorFilePath+"popup.json") as Jfile:
            self.popup=Jfile.read()
            self.popup=json.loads(self.popup)
            Jfile.close()
        print("**************************************")
        print(self.config["config"]["ProcessType"])
        return(self.action,self.captcha,self.config,self.login,self.popup)
        



