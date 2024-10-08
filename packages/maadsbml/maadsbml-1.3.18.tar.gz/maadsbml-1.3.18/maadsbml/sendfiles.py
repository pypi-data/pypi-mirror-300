#############################################################
#
#  Author: Sebastian Maurice, PhD
#  Copyright by Sebastian Maurice 2018
#  All rights reserved.
#  Email: Sebastian.maurice@otics.ca
#
#############################################################

import json, urllib
import requests
import csv
import os
#import imp
import re
import urllib.request
import asyncio
import validators
from urllib.parse import urljoin
from urllib.parse import urlsplit
import aiohttp
from aiohttp import ClientSession
import async_timeout
import pandas as pd
from scipy import stats
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt
import math

def readfile(fn):
    dataset = pd.read_csv(fn)

    return dataset

def distattr(bestdist,bestname):
   shape=0
   for key in bestdist[bestname]:
        if key != 'loc' and key != 'scale':
           value = bestdist[bestname][key]
           shape = value

   scale = bestdist[bestname]['scale']
   loc = bestdist[bestname]['loc']

   return shape,loc,scale
    
def finddistribution(filename,varname,dataarray=[],folderpath='',imgname='distimage',common=1,topdist=5):
    isarray = 0
    if filename != "":
      try:
        dataset=readfile(filename)
        dcol = dataset[varname].values    
      except Exception as e:
        return "ERROR: Unable to read datafile {}".format(filename),"","",""

    if len(dataarray) > 0:
      dcol = list(dataarray)
      isarray = 1
      
    if varname == '':
        return "ERROR: Invalid variable name to analyse: {}".format(varname),"","",""
        
    
    if common==0:
      f = Fitter(dcol,
           distributions=get_distributions())
    else:
      f = Fitter(dcol,
           distributions=get_common_distributions())
        
    f.fit()
    
    distnames=f.summary(topdist).index.values # the best distribution is the first one

    bestdist=f.get_best(method = 'sumsquare_error')
    shape,loc,scale=distattr(bestdist,distnames[0])

    djname = {}
    dj = {}
    for disname in distnames:
        dj = {}
        dj['x'] = f.x
        dj['pdf'] = list(f.fitted_pdf[disname])
        djname[disname] = dj
        #datajson = json.dumps(dj)

    djname['bestdistribution'] = distnames[0]
    djname['shape'] = round(shape,3)
    djname['loc'] = round(loc,3)
    djname['scale'] = round(scale,3)
    fd=f.summary(topdist)
    df = fd.drop('kl_div', axis=1)
    dfc=df.to_json(orient="columns")
    djname['summary']=json.loads(dfc) 
    djname['filename'] = filename
    djname['varname'] = varname
    djname['folderpath'] = folderpath
    djname['distimagefilename'] = "{}.png".format(imgname)
    djname['jsondatafilename'] = "{}.json".format(imgname)

    d=stats.describe(dcol)
    djname['nobs'] = d.nobs
    mm=list(d.minmax)
    djname['min'] = float(mm[0])
    djname['max'] = float(mm[1])
    djname['mean'] = round(d.mean,3)
    djname['variance'] = round(d.variance,3)
    djname['std'] = round(math.sqrt(d.variance),3)
    djname['skewness'] = round(d.skewness,3)
    djname['kurtosis'] = round(d.kurtosis,3)
    
    djname['isarray'] = isarray

    if imgname != "":
      try:   
       with open("{}/{}_data.json".format(folderpath,imgname), 'w') as f:
         json.dump(djname, f)
      except Exception as e:
        return "ERROR: Cannot save JSON file to disk at {}/{}.json".format(folderpath,imgname),"","","" 

      plt.xlabel(varname)
      plt.ylabel('Probability Density')     
      plt.title("Best Distribution For Data Is {} with Shape={}, Loc={}, Scale={}".format(distnames[0],round(shape,3),round(loc,3),round(scale,3)),fontdict={'fontsize':8})

      try:
       plt.savefig("{}/{}.png".format(folderpath,imgname),dpi=190)
      except Exception as e:
       return "ERROR: Cannot save Image file to disk at {}/{}.png".format(folderpath,imgname),"","",""
    
      plt.clf()
    return "INFO: Success finding distributions for data. JSON Data File Saved here: {}/{}.json, Imagefile Saved here: {}/{}.png".format(folderpath,imgname,folderpath,imgname),\
            bestdist,distnames[0],json.dumps(djname)
    

#########################################################################

#########################################################################
def formaturl(maindata,host,microserviceid,prehost,port):

    if len(microserviceid)>0:    
      mainurl=prehost + "://" + host +  ":" + str(port) +"/" + microserviceid + "/?hyperpredict=" + maindata
    else:
      mainurl=prehost + "://" + host + ":" + str(port) +"/?hyperpredict=" + maindata
        
    return mainurl
    
async def tcp_echo_client(message, loop,host,port,usereverseproxy,microserviceid):

    hostarr=host.split(":")
    hbuf=hostarr[0]
   # print(hbuf)
    hbuf=hbuf.lower()
    domain=''
    if hbuf=='https':
       domain=host[8:]
    else:
       domain=host[7:]
    host=domain  

    if usereverseproxy:
        geturl=formaturl(message,host,microserviceid,hbuf,port) #host contains http:// or https://
        message="GET %s\n\n" % geturl 

    reader, writer = await asyncio.open_connection(host, port)
    try:
      mystr=str.encode(message)
      writer.write(mystr)
      datam=''
      while True:
        data = await reader.read(1024)
      #  print(data)
        datam=datam+data.decode("utf-8")
       # print(datam)
        if not data:
           break
        
        await writer.drain()
   #   print(datam)  
      prediction=("%s" % (datam))
      writer.close()
    except Exception as e:
      print(e)
      return e
    
    return prediction

def hyperpredictions(pkey,theinputdata,host,port,username,algoname='',seasonname='',usereverseproxy=0,microserviceid='',password='123',company='otics',email='support@otics.ca',maadstoken='123'):

    if pkey=='' or theinputdata == '' or host== '' or port=='' or username=='':
        print("ERROR: Please specify pkey, theinputdata, host, port, username")
        return

    if '_nlpclassify' not in pkey:
      theinputdata=theinputdata.replace(",",":")
    else:  
      buf2 = re.sub('[^a-zA-Z0-9 \n\.]', '', theinputdata)
      buf2=buf2.replace("\n", "").strip()
      buf2=buf2.replace("\r", "").strip()
      theinputdata=buf2

    if usereverseproxy:
       theinputdata=urllib.parse.quote(theinputdata)
  
    value="%s,[%s],%s,%s,%s,%s,%s,%s" % (pkey,theinputdata,maadstoken,username,company,email,algoname,seasonname)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_client(value, loop,host,port,usereverseproxy,microserviceid))
    #loop.close()
    return val

async def tcp_echo_clienttrain(message, loop,host,port,microserviceid,timeout=1200):

    #if len(microserviceid)>0:
#    geturl=formaturltrain(message,host,microserviceid,hbuf,port) #host contains http:// or https://
 #   message="%s" % geturl 
    try:
     with async_timeout.timeout(timeout):
      async with ClientSession() as session:
        html = await fetch(session,message)
        await session.close()
        return html
    except Exception as e:
     pass   

def genpkey(username,filename):
     pkey = ""
     chars_to_remove= [" ", "(", ")","%","$","&","#","+","=","\\","@",".","/",":","*","?","\"","|","<",">"]
     
     if username != "" and filename != "":
         sc = set(chars_to_remove)
         for i in sc:
           filename = filename.replace(i, '_')

     pkey = username + "_" + filename

     return pkey

#pkey=genpkey('admin','aesopowerdemand.csv')
#print(pkey)
    
def hypertraining(host,port,filename,dependentvariable,removeoutliers=0,hasseasonality=0,summer='6,7,8',winter='11,12,1,2',shoulder='3,4,5,9,10',trainingpercentage=70,shuffle=0,deepanalysis=0,username='admin',timeout=1200,company='otics',password='123',email='support@otics.ca',usereverseproxy=0,microserviceid='',maadstoken='123',mode=0):

# curl "http://localhost:5595?hypertraining=1&mode=0&username=admin&company=otics&email=support@otics.ca&filename=aesopowerdemand.csv&removeoutliers=0&
#hasseasonality=0&dependentvariable=AESO_Power_Demand&summer=6,7,8&winter=11,12,1,2&shoulder=3,4,5,9,10&trainingpercentage=70&shuffle=0&deepanalysis=0"
#maads.hypertraining(maadstoken,host,port,filename,dependentvariable,username='admin',mode=0,timeout=180,company='otics',removeoutliers=0,hasseasonality=0,summer='6,7,8',winter='11,12,1,2',shoulder='3,4,5,9,10',trainingpercentage=70,shuffle=0,deepanalysis=0,password='123',email='support@otics.ca',usereverseproxy=0,microserviceid='')

    if host=='' or port=='' or filename=='' or dependentvariable == '':
        print("Please enter host,port,filename,dependentvariable")
        return ""

    print("Please wait...this could take 3-5 minutes") 
    
    url = "%s:%s/?hypertraining=1&" % (host,port)
    params = {'mode': str(mode), 'username': username,'company': company,'email': email,'filename': filename,'removeoutliers': str(removeoutliers),'hasseasonality': str(hasseasonality),'dependentvariable': dependentvariable,'summer': summer,'winter': winter,'shoulder': shoulder, 'trainingpercentage': str(trainingpercentage),'shuffle': str(shuffle),'deepanalysis': str(deepanalysis)}
    mainurl = url + urllib.parse.urlencode(params)

    print(mainurl)
    try:
      value="%s" % (mainurl)
      loop = asyncio.get_event_loop()
      val=loop.run_until_complete(tcp_echo_clienttrain(value, loop,host,port,microserviceid,timeout))
    except IOError as e: 
      if e.errno == errno.EPIPE: 
        pass

    if val == None:
       pkey=genpkey(username,filename)
       val="{\"AlgoKey\":\"" + pkey + "\", \"BrokenPipe\":\"Broken pipe exception was caught - this may happen due to network issues. The system will finish - use the AlgoKey and check the exception folder for your algorithm JSON, and check PDFREPORTS folder for your pdf.\"}" 
       return val
    
  #  loop.close()
    return val

def algodescription(host,port,pkey,timeout=300,usereverseproxy=0,microserviceid=''):
    if host=='' or port=='' or pkey=='':
        print("Please enter host,port, and PKEY (this is the key you eceived from the hypertraining funtion.)")
        return ""

    url = "%s:%s/?algoinfo=1&pkey=%s" % (host,port,pkey)
    mainurl = url

    print(mainurl)
  
    value="%s" % (mainurl)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clienttrain(value, loop,host,port,microserviceid,timeout))
 #   loop.close()
    return val

def rundemo(host,port,demotype=1,timeout=1200,usereverseproxy=0,microserviceid='',username='admin',filename=''):

    print("Please wait...this could take 3-5 minutes") 
    url = "%s:%s/?rundemo=%s" % (host,port,str(demotype))
    mainurl = url

    print(mainurl)
  
    value="%s" % (mainurl)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clienttrain(value, loop,host,port,microserviceid,timeout))
#    loop.close()

    if demotype==1:
        filename='aesopowerdemand.csv'

    if demotype==0:
        filename='aesopowerdemandlogistic.csv'
        
    if val == None:
       pkey=genpkey(username,filename)
       val="{\"AlgoKey\":\"" + pkey + "\", \"BrokenPipe\":\"Broken pipe exception was caught - this may happen due to network issues. The system will finish - use the AlgoKey and check the exception folder for your algorithm JSON, and check PDFREPORTS folder for your pdf.\"}" 
       return val

    return val

def abort(host,port=10000):

    url = "%s:%s/?abort=1" % (host,port)
    mainurl = url

    print(mainurl)
  
    value="%s" % (mainurl)
    loop = asyncio.get_event_loop()
    val=loop.run_until_complete(tcp_echo_clienttrain(value, loop,host,port,''))
#    loop.close()
    return val

#########################################################

async def fetch(client,url):
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()

