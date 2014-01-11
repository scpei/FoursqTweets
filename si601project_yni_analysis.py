from operator import itemgetter
import csv, sqlite3,sys


def count1(): #Add all the words together and export to one file
    i=0
    while i <3:
        i +=1
        
        wr1 = open ("venue%s_tagcloud.txt"%i,"w")
        wr2 = open ("venue%s_wordcount.txt"%i,"w")
        
        userallwords = []#Create a list to put all the unique words of each user in it.
        counts = dict()#Create a dict to count if different users mentioned the same unique word
        
        #Is there a way to iterate all tables in a sql database?
        #Find twitter name in the database "si-601-project_yni", and use the twitter name to create tables in another database
        con1 = sqlite3.connect("si-601-project_yni.db")
        con1.text_factory = str #To output the string instead of unicode
        cur1 = con1.cursor()
        cur1.execute("SELECT user_twitteraccount FROM top_venue%s" % (i))
        #for r in cur.fetchall():
        accountlist = [r[0] for r in cur1.fetchall()]#To transfer a tuple to a list of twitter account
        for data in accountlist:#To get the pure twitter account string without 'u' or ();

            try:        
                con = sqlite3.connect("venue%s.db"%(i))
                con.text_factory = str #To output the string instead of unicode
                cur = con.cursor()
                cur.execute("SELECT word FROM %s"%data)
                #for r in cur.fetchall():
                words = [k[0] for k in cur.fetchall()]#To transfer a tuple to a list of twitter account
                for word in words:
                    userallwords.append(word)
                
            except Exception as e:
                print e
        print "Writing 'venue%s_tagcloud.txt'"%i
        
        filterword = ['all','s','and','or','in','of','the','a','for','i','my','to','&','at','by','is','on','you','your','-','that','this','from','things','about','be','with','not','it','who','where','when','we','co','http','t','m','com']
        
        for word in userallwords:
            if word not in filterword:
                wr1.write(word+' ')#wr1's mission already finished

            #This is wr2's mission:
            if word not in counts:
              counts[word] = 1
            else:
              counts[word] = counts[word]+1
                  
        c = counts.items()
        s = sorted(c, key=itemgetter(1))
        d = sorted(s, key=itemgetter(1),reverse=True)

        
        print "Writing 'venue%s_wordcount.txt'"%i
        for wordandcount in d:
            if wordandcount[0] not in filterword:
                wr2.write(wordandcount[0]+'\t'+str(wordandcount[1])+'\n')
            
        wr1.close()
        wr2.close()
    return



def main():
    count1()


if __name__ == '__main__':
  main()  
