import urllib.request , socket
socket.setdefaulttimeout(180)

class proxyChecking():
    def is_bad_proxy(proxyList):
        workingProxy=[]
        for item in proxyList:
            try:
                proxy_handler = urllib.request.ProxyHandler({'http':str(item+":"+str(proxyList[item]))})
                opener = urllib.request.build_opener(proxy_handler)
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                sock=urllib.request.urlopen('http://www.google.com')
                workingProxy.append(item)    
            except urllib.error.HTTPError as e:
                print('Error code: ', e.code)
                return (e.code)
            except Exception as detail:
                print( "ERROR:", detail)
                return 1
        return(workingProxy)