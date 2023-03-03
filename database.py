import pymysql

class database():
    def db(query):
        conn = pymysql.connect(host='127.0.0.1',user='root', password = 'swineflu2009',db='seed')
        cur = conn.cursor()
        cur.execute(query)
        print(query)
        output = cur.fetchall()
        return output

    def updateDb(query):
        try:
            conn = pymysql.connect(host='ns.codemskyapp.com',user='ns', password = 'ndgfdgf@sfd7',db='notspam')
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            print(Exception)
            conn.close()

    def readDb(query):
        conn = pymysql.connect(host='ns.codemskyapp.com',user='ns', password = 'ndgfdgf@sfd7',db='notspam')
        cur = conn.cursor()
        cur.execute(query)
        data=cur.fetchall()
        return(list(data))