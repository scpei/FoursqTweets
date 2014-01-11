from operator import itemgetter,attrgetter
import re,sqlite3

def wordcount(dbid,twittername):
    try:
        f = open('top_venue_%s_%s.txt'%(dbid,twittername))
        counts = dict()
        for line in f:
            words = re.findall(r"[\w]+",line)


            for word in words:
                if word.lower() not in counts:
                  counts[word.lower()] = 1
                else:
                  counts[word.lower()] = counts[word.lower()]+1
        c = counts.items()
        s = sorted(c, key=itemgetter(1))
        d = sorted(s, key=itemgetter(1),reverse=True)

        #Create a database for No.dbid venue:
        print "Writing data to 'venue%s.db'..."%(dbid)
        with sqlite3.connect(r'venue%s.db'%(dbid)) as con:

            dbname = twittername
            #print dbname
            cur = con.cursor()
         
            cur.execute('DROP TABLE IF EXISTS %s'%(twittername))
        
            cur.execute('CREATE TABLE %s (word,count)' % (twittername))
                   
            cur.executemany('INSERT INTO %s VALUES (?,?)' % (twittername),d)
            
            con.commit()
           
            #rows = cur.fetchall()
            #print rows

        print "Mission Compeleted."    
        con.close()

    except Exception as e:
        print e
    
    return


def findtwittername(dbid):#Find twitter name in the database, and use the twitter name to create tables in another database

    con = sqlite3.connect("si-601-project_yni.db")
    con.text_factory = str #To output the string instead of unicode
    cur = con.cursor()
    cur.execute("SELECT user_twitteraccount FROM top_venue%s" % (dbid))
    #for r in cur.fetchall():
    accountlist = [r[0] for r in cur.fetchall()]#To transfer a tuple to a list of twitter account
    for data in accountlist:#To get the pure twitter account string without 'u' or ();
        wordcount(dbid,str(data))#Transfer the varable to another function
    
    return

def main():
    #findtwittername("1")
    #findtwittername("2")
    findtwittername("3")


    

if __name__ == '__main__':
  main() 


