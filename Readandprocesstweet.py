#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd


# In[2]:


# The first 25 characters are not needed
tweets =  json.loads(open('tweet.js','r', encoding = 'UTF-8').read().replace('\n','')[25:])


# In[3]:


def dfise(tweet):
    
    dfdict = {}
    dfdict['id_str'] = tweet['tweet']['id_str']
    dfdict['created_at']= tweet['tweet']['created_at']
    dfdict['full_text']= tweet['tweet']['full_text']
    try:
        dfdict['in_reply_to_status_id_str']= tweet['tweet']['in_reply_to_status_id_str']
    except:
        dfdict['in_reply_to_status_id_str']=''
    
    dfdict['isRT'] = tweet['tweet']['full_text'][:2] == 'RT'
    
    return pd.DataFrame(dfdict, index = [dfdict['id_str']])


# In[4]:


dfs = []
for tweet in tweets:
    dfs.append(dfise(tweet))


# In[5]:


dfcombined = pd.concat(dfs)
dfcombined['time'] = pd.to_datetime(dfcombined['created_at'])


# In[ ]:


# if you want to save the DataFrame
# dfcombined.to_hdf('tweets.hdf', key = 'tweet', mode='w')


# In[6]:


# Change time period for each file here
bins = pd.date_range('2015-01-01', periods=310, freq='W')
dfcombined['bin'] = pd.cut(dfcombined['time'],bins,labels = bins[:-1])


# In[7]:


# remove retweets// to keep retweets just write: dfproown =  dfpro.copy()
dfown =  dfcombined[~dfcombined ['isRT']].copy()


# In[8]:


# Hashtags is considered as titles in the markdown file. Need to convert it to real # before converting
dfown['nohashtag'] = dfown['full_text'].str.replace('#','\#')
dfown['Combined'] = '### Tweet_id: '+dfown['id_str']+'\n'+dfown['created_at']+'//\t'+'Replying_to:'+dfown['in_reply_to_status_id_str']+'\n\n'+dfown['nohashtag']+'\n'


# In[10]:


# Generate files
for i in range(310):
    tempdf = dfown[dfown['bin']==bins[i]].copy()
    string = "Start \n"+'\n'.join(tempdf['Combined'].to_list())
    
    f = open("tweet"+str(bins[i])[:10]+".md", "w", encoding = 'UTF-8')
    f.write(string)
    f.close()


# In[ ]:





# In[ ]:




