import tweepy
from time import sleep
import sqlite3

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="FrXAe21CMIO4FZntC0kP1g"#"KnhA5gkBD60gYKyGzvtIxA"#"VORPhOqA1ZmcLDmnY7v5Q"#
consumer_secret="W7sbfryP39KJlk4B82TMw4B4N8uFl0Kh82H8dpDI"#"7BihjMcDP6VS6i67vizHoGWDHTApxRjTTxriF9UtJew"#"bSZPvQR2IEVj2cCEM5hq562cfRmy1InNdjWluRA"#

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="202036216-ybGKofoFIXyFgQlJVPGtBGmGdSfIUOWF1Hh5t6pU"#"1972547462-1nHN7TnYoCFjO1APUVVVRlMEoSn9uIhQx2pYUcM"#"1969681843-Yk1LVRRhll2ec9QLMWIHCvrDArcum0msWmVoVVs"#"#
access_token_secret="Yt3HAwxWKzwD09VKiFK2lrpSpQbwHY1g7PIOTub9E"#"JtnkcPi8fGfVUzCxnkgBGpl7k1MtmlmFh2vMFyNhY"#"Vrwc0ekRi414iCQRPnixOGvhn8CBJelhCEt83KpatU"#

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out



def find_descriptions(dbid):

    con = sqlite3.connect("si-601-project_yni.db")
    con.text_factory = str #To output the string instead of unicode
    cur = con.cursor()
    cur.execute("SELECT user_twitteraccount FROM top_venue%s" % (dbid))
    #for r in cur.fetchall():
    accountlist = [r[0] for r in cur.fetchall()]#To transfer a tuple to a list of twitter account
    for data in accountlist:#To get the pure twitter account string without 'u' or ();
        #print data
    
        eachfilename = 'top_venue_%s_%s'%(dbid,str(data))+'.txt' #Creat .txt file to write word count.
        #print eachfilename

        try:
            commenter_des = api.get_user(str(data)).description.encode('utf-8')#First check if this twitter account exists
            wr = open (eachfilename,'w')
            wr.write(commenter_des+'\n')
            print "File is ganerated: %s"%(eachfilename)
            
            friendids = api.friends_ids(str(data))#Get a list of friends' twitter id

            controller = []
            i = -1
            while len(controller)<11:#For each twitter account a commenter is folloing, find 10 of their friends' description:                    
                try:
                    i +=1                        
                    friend_des = api.get_user(friendids[i]).description.encode('utf-8')
                    if friend_des !='':
                        wr.write(friend_des+'\n')
                        controller.append(friend_des)
                        print 'Wrting friend description',i                            
                except:
                    print 'error'
                    break
            wr.close()               

        except tweepy.TweepError, e:#If the twitter account doesn't exist, print out the error message
            print 'failed because of %s' % e.reason

        
            

def main():
    find_descriptions("1")
    #find_descriptions("2")
    #find_descriptions("3")


    

if __name__ == '__main__':
  main()        


# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's 
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# api.update_status('Updating using OAuth authentication via Tweepy!')
