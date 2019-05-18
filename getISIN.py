
# use getisin() function to get full name as well as ISIN. 
# Only return the first search result from businessinsider 
# ( so I added full name. The user shall check whether the result is correct )
# example getisin('apple')

import requests

import re


def getisin(companyname):
    
    session_requests = requests.session()
    
    searchload = {
    
    "_search": companyname,
    
    }
    
    url = 'https://markets.businessinsider.com/searchresults?_search='
    counter = 0
    
    names = companyname.split(' ')
    
    for name in names:
        if counter != 0:
            url = url + '+' + name
        else:
            url = url + name
            counter += 1


    result = session_requests.post(
        url = url, 
        headers = dict(referer = url),
        data = companyname
    )   
    
#    findings = pd.unique(re.findall(r'<td scope="col" class=""><a href="/isin-preview/\?isin=(.+?)">.+?</a>',result.text))
    
    stockurl = 'https://markets.businessinsider.com'+re.findall(r'<a href="(/stocks/.+)" title.+>.+</a>',result.text)[0]
    
    stockresponse = session_requests.get(
    url = stockurl, 
    headers = dict(referer = stockurl),
    )
    
    
    
    return pd.unique(re.findall(r'Full Name.+?<td  width="30%" >[\\]r[\\]n[\\]t[\\]t[\\]t[\\]t[\\]t[\\]t(.+?)[\\]r.+?</td>',str(stockresponse.content))) +', '+ pd.unique(re.findall(r"Portfolio\.addInstrumentToPortfolioV3\(\'(.+?)\',",stockresponse.text))[0]
    
