FoursqTweets
============

For people who check in on FourSquare at a particular place, are there any common interests (e.g. The type of users they are following on Twitter) between them? Can I find some patterns and characteristics for a place? 


How it works:

There are four python scripts to collect and manipulate data. After running the four scripts, a txt file will be created for generating a tag-cloud image on Tagul.com. Now I will go through the steps of the workflow.	

Step1: Choose one category you want to search, and define the searching criteria (latitude and longitude, Intent: browse, radius, Category) on Foursquare API "Search Venues" page, and copy the url into the script. In the modified version, you can choose three different categories. 

Step2: Run script "si601 project_yni.py" to find the top3 venues with checkin accounts in a certain category. The script will create a database called "si601-project_yni.db" with three tables for the three venus. For each venue, the script will find the mayor and at most 20 users who left a tip there(Foursquare API can only show at most 20 tips for a venue), and it will look for he user's twitter account then write at most 10 users' data into that venue's table with users full name, their foursquare id and twitter account names . 

Step3: Run the script "si601project_yni_twitter.py". The script will read the selected table in the database, pull out the users' twitter account name, get descriptions of the users and at most 10 of the friends they began following recently, and write them into a .txt file in the naming format of "top_venue_(venue number)_(twitter account).txt". If the twitter account is invalid, it will print out the error message and won't create the .txt file for the user.

Step4: Run the script "si601project_yni_wordcount.py". The script will read the txt files of twitter users descriptions, count each word matching the regular expression "[\w]+", sort the words according to frequency, create a database for each venue (venue1/2/3.db), create tables named after the Twitter accounts, and write the word and count into the it. In this step I faced a problem when I was using MRjob, since I have to read and write every txt file and I need to remove the "'"for each word. I finally solved the problem by replaying MRjob with another python script to automatically read every txt file created in prior steps and write the results into the database. 

Step5: Run the script "si601project_yni_analysis.py". This script will read the venue database, create a list to put in all the "unique word" of each description, filter out meaningless words, and count the number of rest of the words in each venue. The reason why I didn't count each word directly from all the descriptions is to avoid bias caused by a particular user. For example, if the word "football" appears 15 times in the descriptions collected for a twitter user, it may lead to misinterpretation that the 10 users for a venue have a common interest of football. So only counting unique word in descriptions for a user and see the overlap for the 10 users can better reflect if their interests overlap in some ways. The script "si601project_yni_analysis.py" will generate two txt files for each venue, one is for creating a tagcloud on Tagul, with words repeated according to their frequency in the analysis; another one is for plain reading, with word and the number of its frequency.
