# -*- coding: cp936 -*-
import foursquare,json,urllib2
from operator import itemgetter
import csv, sqlite3,sys

client = foursquare.Foursquare(client_id='KVGBL2A4MVQEPCOHVS51EU1JIEZAL0HHS4QC2Q3K2JI54CHP', client_secret='W30ZSXVO1H4LWYLNS3AFBXZVJBP2YCT1ADU5FNW44C11AGWX')


#A method to find users' twitter accounts
def users_twitter(top1_users):
    twitters = [] 
    for i in range(len(top1_users)):
        user_url = 'https://api.foursquare.com/v2/users/%s?oauth_token=DS1KFRQLDBZ5F4IMNE2QVSNZIIFNQZW2TZQ4AY1WN3YBX440&v=20131011' % (top1_users[i])
        user_response = urllib2.urlopen(user_url)
        user_info = user_response.read()
        user_data = json.loads(user_info)    

        #Find the users' twitter accounts      
        if 'twitter' in user_data['response']['user']['contact']:
            twitters.append(user_data['response']['user']['contact']['twitter'])
        else:
            twitters.append('NULL')

    return twitters



#For the top3 checkin venues, get user's accounts who left tips 
def top_venues_users(dbid,venueid):  
    
    #https://api.foursquare.com/v2/######venues/4aaa6549f964a520d25520e3
    url_top1 = 'https://api.foursquare.com/v2/venues/%s?oauth_token=DS1KFRQLDBZ5F4IMNE2QVSNZIIFNQZW2TZQ4AY1WN3YBX440&v=20131011' % (venueid)

    #Read the content
    response1 = urllib2.urlopen(url_top1)
    content1 = response1.read()
    content_dic1 = json.loads(content1)

    #Create a list of users
    top1_users =[]
    top1_usersname = []

    #Find the mayor user' ids
    print "The system is looking for the mayor of the No.%s venue..."%(dbid+1)
    mayor = content_dic1['response']['venue']['mayor']['user']['id']
    top1_users.append(mayor)
    firstname = content_dic1['response']['venue']['mayor']['user']['firstName']
    
    if 'lastName' in content_dic1['response']['venue']['mayor']['user']:
        lastname = content_dic1['response']['venue']['mayor']['user']['lastName']
        username = str(firstname)+ str(lastname)
    else:
        username = str(firstname)+ ''
        
    top1_usersname.append(username)
    
    #Find the users' ids who left tips in that vanue
    print "The system is looking for the visitors who left a tip for the No.%s venue..."%(dbid+1)
    tipitems = content_dic1['response']['venue']['tips']['groups'][0]['items']
    for i in range(len(tipitems)):
        top1_users.append(tipitems[i]['user']['id'])
        #print type(str(tipitems[i]['user']['firstName']))
        if 'lastName' in tipitems[i]['user']['id']:
            username = str(tipitems[i]['user']['firstName'])+ str(tipitems[i]['user']['lastName'])
        else:
            username = str(tipitems[i]['user']['firstName'])+ ''
        top1_usersname.append(username)
    
    #Use the users_twitter method to find the twitter accounts of users who left tips in a venue
    print "The system is pulling out the mayor and commentors' twitter accounts..."
    twitters = users_twitter(top1_users)
    
    #Another list for output into database
    wrapper_user = []

    usernumber=0
    for j in range(len(top1_users)): #For each of the user
        user_db = []
        if str(twitters[j]) != 'NULL' and usernumber <10: #Filter out those 'NULL' data
            usernumber +=1
            user_db.append(top1_usersname[j]) #User name
            user_db.append(int(top1_users[j])) #User id
            user_db.append(twitters[j]) #User twitter account. If it is empty input "NULL"
            wrapper_user.append(tuple(user_db))
    #print wrapper_user
        
        
    #Export to txt file
##    print "The system is writing data into .txt files..."        
##    f = open (r'top_venue_%s.txt'%(str(dbid+1)),'w')
##    for k in range(len(wrapper_user)):
##        f.write(str(wrapper_user[k][0])+'\t'+str(wrapper_user[k][1])+'\t'+str(wrapper_user[k][2])+'\n')
##    f.close()
##    print "The .txt file is created! \n"



    with sqlite3.connect(r'si-601-project_yni.db') as con:

        dbname = 'top_venue%s' % (dbid+1)
        #print dbname
        cur = con.cursor()
     
        cur.execute('DROP TABLE IF EXISTS %s'%(dbname))
    
        cur.execute('CREATE TABLE %s (user_name,user_id,user_twitteraccount)' % (dbname))
               
        cur.executemany('INSERT INTO %s VALUES (?,?,?)' % (dbname),wrapper_user)
        
        con.commit()
       
        #rows = cur.fetchall()
        #print rows
    con.close()


    return










#A method to search for food category venues in using Foursquare API Explorer, 
def area_venues():    
    #based on the latitude and longitude at NorthQuad, in the radius of 1000 meters:
    #https://api.foursquare.com/v2/#######venues/search?ll=42.281262,-83.740049&intent=browse&radius=1000

    print "The system is looking for top3 venues you're searching for in this area in a few seconds..."

    url_venues = 'https://api.foursquare.com/v2/venues/search?ll=42.281262,-83.740049&intent=browse&radius=1000&oauth_token=DS1KFRQLDBZ5F4IMNE2QVSNZIIFNQZW2TZQ4AY1WN3YBX440&v=20131020'

    #Read the content
    
    response = urllib2.urlopen(url_venues)
    content = response.read()
    content_dic = json.loads(content)

    #Create a wrapper list for sorting by checkincounts:
    wrapper = []
    for venue in content_dic['response']['venues']:
        venue_attr = []
        venue_attr.append(venue['name'])    
        venue_attr.append(venue['id'])
        venue_attr.append(venue['stats']['checkinsCount'])
        wrapper.append(venue_attr)
    wrapper.sort(key=lambda x:x[2],reverse=True)

    for i in range(3):
        print '''The top%s venue is: 
                %s, with %s checkins.'''%(i+1, wrapper[i][0],wrapper[i][2])
        venueid = str(wrapper[i][1])
        
        #Use the "top_venues_users" to find users who left tips in a venue
        top_venues_users(i, venueid)
                

    return

    


def main():
    area_venues()


    

if __name__ == '__main__':
  main()







    

      

