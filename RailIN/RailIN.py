from requests import get,post,Session
from CaptchaBreak import Captcha
from user_agent import generate_user_agent as gua
from json import dumps,loads
from prettify import Prettify
from datetime import date
'''
This API scrapes data of Indian Railways from erail.in and parses into JSON for use in personal applications.
Not intended for commercial use.

1. Get Route ( X )
2. Get Availability ( X )
3. Get Fare ( X )
4. Get Train Status ( X )
5. Get StationCode ( X )
6. Get PNR ( X )

'''

class RailIN:
    # Website asks for captcha which can be pre-generated due to the flaw
    def getPNR(self,PNR):
        if (len(str(PNR))<10) or (len(str(PNR))>10):
            return dumps({'error':'PNR must be 10 digit.'})
        URL_captcha = 'http://www.indianrail.gov.in/enquiry/captchaDraw.png'
        # create a Session
        s = Session()
        s.headers['User-Agent'] = gua()
        probable_captcha = Captcha().decode(s.get(URL_captcha).content)
        try:
            URL = 'http://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha='+probable_captcha+'&inputPnrNo='+PNR+'&inputPage=PNR'
            return loads(s.get(URL).text)
        except:
            return dumps({'error':'some captcha error occured'})

    def getRoute(self,TN):
        ID = self.getTrain(TN)
        try:
            ID['error']
        except KeyError:
            ID = ID['train_base']['train_id']
        URL_Route = "https://erail.in/data.aspx?Action=TRAINROUTE&Password=2012&Data1="+ID+"&Data2=0&Cache=true"
        return Prettify().StationToJson(get(URL_Route).text)

    def getAllTrains(self,F,T):
        URL_Trains = "https://erail.in/rail/getTrains.aspx?Station_From="+F+"&Station_To="+T+"&DataSource=0&Language=0&Cache=true"
        return Prettify().TrainsToJson(get(URL_Trains,headers = {'User-Agent':gua()}).text)

    # Pass in date month and year
    def getTrainsOn(self,F,T,DD,MM,YYYY):
        retval = []
        D = date(YYYY,MM,DD).weekday()
        for i in self.getAllTrains(F,T):
            if i['train_base']['running_days'][D]=='1':
                retval.append(i)
        return dumps(retval)

    def getTrain(self,TN):
        URL_Train = "https://erail.in/rail/getTrains.aspx?TrainNo="+str(TN)+"&DataSource=0&Language=0&Cache=true"
        try:
            return Prettify().TrainsToJson(get(URL_Train).text)[0]
        except:
            return {'error':'Unexpected Server Response'}

    def getAvailability(self,TN,SSTN,DSTN,CLS,QT,DD,MM):
        URL_Avail = "https://d.erail.in/AVL_Request?Key="
        val = '_'.join([str(TN),SSTN,DSTN,CLS,QT,str(DD)+'-'+str(MM)])
        return Prettify().AvailToJson(get(URL_Avail+val).text)


    def getFare(self,TN,F,T):
        URL_Fare = "https://erail.in/data.aspx?Action=GetTrainFare&train="+str(TN)+"&from="+F+"&to="+T
        return Prettify().FareToJson(get(URL_Fare).text)

    def getStatus(self,TN,DD,MMM,YYYY,CD):
        D = '-'.join([str(DD), MMM, str(YYYY)])
        URL_Live = "https://data.erail.in/getIR.aspx?&jsonp=true&Data=RUNSTATUS~0_"+str(TN)+"_"+D+"_"+CD
        return loads(get(URL_Live).text.strip('()'))
