# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 19:46:13 2019

@author: Abhishek_bhad
"""
import os, re, datetime, time
from bs4 import BeautifulSoup
import pandas as pd


tagName1='Lost Time Details'
tagName2="Cum. Hrs"
position=24
temp1=pd.DataFrame(str(soup).split("</tbody>"))
temp1.columns=['RawText']
posTag=temp1.RawText[temp1.RawText.str.contains(tagName1)].index.tolist() 
temp2=pd.DataFrame(str(list(temp1[posTag[0]:posTag[0]+1]['RawText'])[0]).split("</td>"))
temp2.columns=['RawText']
posTag=temp2.RawText[temp2.RawText.str.contains(tagName2)].index.tolist() 



temp2=pd.DataFrame(temp1['RawText'].astype(str)).split("</td>") 



def extract_value_from_tags(soup_obj,tagName,position):
    if len(soup_obj)>0:
        temp=pd.DataFrame(str(soup_obj).split("</td>"))
        temp.columns=['RawText']
        posTag=temp.RawText[temp.RawText.str.contains(tagName)].index.tolist() 
        if len(posTag)>0:
           text=list(temp[posTag[0]+position:posTag[0]+position+1]['RawText'])
           if len(text)>0 and len(re.findall(r'\d+',text[0]))>0:
              text=re.sub(r'\<(.*?)\>', '',text[0])
              text=re.findall(r'\d+\.\d+|\d+',text)[0] 
              return text
           else:
              return None 
    else:
        return None


def data_extraction(fn,soup_obj):
    if len(soup_obj)>0:
       temp=pd.DataFrame() 
       allData = soup_obj.findAll("td", {"class": "l"})
       tempdata=soup_obj.findAll("span", {"class": "l"})
       dates=allData[1].text
       drillingDays=tempdata[0].text
       #wellNo=allData[2].text
       wellName=allData[2].text
       rigNo=allData[5].text
       #totalFootage=allData[19].text
       totalFootage=extract_value_from_tags(soup_obj,'TOL',4)      
       temp=pd.DataFrame({'FileName':[fn],'ReportDate':[dates],'Rig':rigNo,'WellName':[wellName],'DrillingDays':[drillingDays],'TotalFootage':[totalFootage]})          
       return temp


def Clean_Text(text):
    if text!="":
       text=text.upper() 
       text = re.sub(r'[^\x00-\x7F]','', text)         # Remove all Non ASCII characters 
       text = re.sub(r'[\n]','',text)                  # Remove New Line Char
       #text=re.sub('\W+',' ',text)                     #stripping off any special characters and ensure space between words .
       text = " ".join(text.split())                   # Remove all white spaces
       return text   

def get_date(dt):
    if dt!='':
       dt=dt.replace("/","-") 
       #dates=""
       dates=str(datetime.datetime.strptime(dt, "%m-%d-%Y").date())
       return dates


def extract_personal_service_info(fn,soup_obj):
    if len(soup_obj)>0:
       Company=[]
       Category=[]
       NoOFPersons=[]
       OperatingHrs=[]
       OnLocationHrs=[]
       #extracting the text from html object
       allData = soup.findAll("td", {"class": "la"})
       dateData = soup_obj.findAll("td", {"class": "l"})
       dates=dateData[1].text
       #reading each data records
       for i in range(0,len(allData),5):
           Company.append(allData[i].text)
           Category.append(allData[i+1].text)
           NoOFPersons.append(allData[i+2].text)
           OperatingHrs.append(allData[i+3].text)
           OnLocationHrs.append(allData[i+4].text)
       temp=pd.DataFrame({'Company':Company,'Category':Category,'NoOFPersons':NoOFPersons,'OperatingHrs':OperatingHrs,'OnLocationHrs':OnLocationHrs})
       temp['FileName']=fn 
       temp['ReportDate']=dates
       return temp
   

######################MAIN FUNCTION#######################################################################
if __name__ == "__main__":
   start_time=time.perf_counter()
   process_start_time=time.ctime()
   print("Processing start at: " + str(process_start_time))
   path = r"C:\Analytics_Projects\LogFiles\GetData\TestReports" 
   finalData=pd.DataFrame()
   personalInfo=pd.DataFrame()
   msg1=msg2=msg3=""
   for filename in os.listdir(path):
       if filename.endswith(".html"):
          fullpath = os.path.join(path, filename)
        
        # Get Page, Make Soup
          soup = BeautifulSoup(open(fullpath), 'html.parser')
          try:
              x=data_extraction(filename,soup)
              finalData=finalData.append(x)
          except BaseException as e:
              msg1="\nError found with basic information in file "+filename
              print(msg1)   
          try:                         
              x=extract_personal_service_info(filename,soup)
              personalInfo=personalInfo.append(x)
          except BaseException as e:
              msg2="\nError found with personal & service information in file "+filename
              print(msg2)   
   f = open(path+"\\log.txt", "a")      
   f.write("\nProcessing start at: " + str(process_start_time))   
   f.write(msg1+msg2)
   f.close()
   elapsed_time = time.perf_counter() - start_time
   msg3="\nData has been extracted in time elapsed: {} seconds".format(round(elapsed_time,2))
   print(msg3)
   f = open(path+"\\log.txt", "a")   #open log file in append mode  
   f.write(msg3+"\n==========================================================")    # Write the processing end time 
   f.close()  # Close file
   finalData['WellName']=finalData['WellName'].apply(Clean_Text)
   finalData['ReportDate']=finalData['ReportDate'].apply(get_date)


extract_value_from_tags(soup,'Lost Time Details',15)


#ROUGH WORK
#soup = BeautifulSoup(open(fullpath), 'html.parser')
#finalData.to_csv("C:\\Analytics_Projects\\LogFiles\\PythonWork\\Results\\DataSet1.csv")
#personalInfo.to_csv("C:\\Analytics_Projects\\LogFiles\\PythonWork\\Results\\DataSet2.csv")    




