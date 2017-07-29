from bs4 import BeautifulSoup

class Prettify:
    def TrainsToJson(self,string):
        data = string.split('^')
        # data[0] is useless
        retval = []
        for i in data[1:]:
            retval.append(self.MakeSenseTrain(i))
        return retval

    def MakeSenseTrain(self,string):
        data = string.split('~~~~~~~~')
        data1 = data[0].split('~')
        retval = {}

        dic1 = {}

        dic1['train_no'] = data1[0]
        dic1['train_name'] = data1[1]
        dic1['source_stn_name'] = data1[2]
        dic1['source_stn_code'] = data1[3]
        dic1['dstn_stn_name'] = data1[4]
        dic1['dstn_stn_code'] = data1[5]
        dic1['from_stn_name'] = data1[6]
        dic1['from_stn_code'] = data1[7]
        dic1['to_stn_name'] = data1[8]
        dic1['to_stn_code'] = data1[9]
        dic1['from_time'] = data1[10]
        dic1['to_time'] = data1[11]
        dic1['travel_time'] = data1[12]
        dic1['running_days'] = data1[13]

        retval['train_base'] = dic1

        # dealing with the second part , third part isn't interpreted yet
        data2 = data[1].split('~~')
        # produces atleast 6 parts at max 8


        data2_1 = data2[0].split('~')
        # 0th - Extract coach types etc

        retval['coach_types']={}
        retval['coach_types']['1A'] = data2_1[0][0]
        retval['coach_types']['2A'] = data2_1[0][1]
        retval['coach_types']['3A'] = data2_1[0][2]
        retval['coach_types']['CC'] = data2_1[0][3]
        retval['coach_types']['SL'] = data2_1[0][5]
        retval['coach_types']['2S'] = data2_1[0][6]
        retval['coach_types']['GN'] = data2_1[0][8]

        retval['train_base']['source_depart'] = data2_1[5]
        retval['train_base']['dstn_reach'] = data2_1[6]
        retval['train_base']['type'] = data2_1[11]
        retval['train_base']['train_id']= data2_1[12]
        retval['train_base']['distance_from_to'] = data2_1[18]
        retval['train_base']['average_speed'] = data2_1[19]

        # 1st - Extract notification

        try:
            notif = data2[1].split('~')[3]
            retval['train_base']['notif_coach'] = notif
        except:
            pass

        # 2nd - Extract train type or notification
        for i in range(2,7):
            try:
                if data2[i] is not None:
                    key,value = self._extract(data2[i])
                    retval[key]=value
            except:
                pass
        return retval

    def _extract(self,string):
        val = string.strip('~')
        val = val.split('~')
        length = len(val)
        if length == 1:
            if val[0] == "" :
                return 'No Data'
            else:
                words = len(val[0].split())
                if words >3:
                    return "notif",val[0]
                if all((i.isalpha()) or (i=='&') or (i==' ') for i in val[0]) and (words <4) and (val[0]!='BG'):
                    return "train_type",val[0]
        if length >= 2:
            if all((i.isalpha()) or (i=='&') or (i==' ') for i in val[1]) and (len(val[1].split()) <4) and (val[1]!='BG') and len(val[1])>4:
                # Check camel case
                if all(i[0].isupper() and all(j.islower() for j in i[1:]) for i in val[1].split() if len(i)>1):
                    return "train_type",val[1]
            elif all(i.isalpha() and i.isupper() for i in val[1]) :
                # it is a region
                return "region",val[1]
            elif all((i.isdigit())or (i==",") for i in val[1]):
                return "rake_share",val[1].split(',')
            elif ':' in val[1]:
                coach = []
                data = val[1].strip(':').split(':')
                for i in range(len(data)):
                    f = data[i].split(',')
                    coach.append({str(i+1) : {'tag':f[0],'coach_id':f[1],'type':f[2]}})
                return "coach_arrangement",coach

    def StationToJson(self,string):
        retval = []
        data = string.split('^')
        if '|' in data[0]:
            start = 1
        else:
            start = 0
        for i in data[start:]:
            retval.append(self.MakeSenseStation(i))
        return retval

    def MakeSenseStation(self,string):
        retval = {}

        data = string.split('~')

        retval['index'] = data[0]
        retval['code'] = data[1]
        retval['name'] = data[2]
        retval['arrival'] = data[3]
        retval['depart'] = data[4]
        retval['halt'] = data[5]
        retval['distance_from_source'] = data[6]
        retval['day'] = data[7]
        retval['platform'] = data[8]
        retval['zone'] = data[10]
        retval['division'] = data[11]
        retval['lat'] = data[14]
        retval['lng'] = data[15]

        return retval

    def FareToJson(self,string):
            soup = BeautifulSoup(string,'lxml')
            tables = soup.findAll('table',{'class':'tableSingleFare table table-bordered table-condensed'})
            fare_table = tables[1]
            fare_rows = fare_table.findAll('tr')
            fare_types = [i.string for i in fare_rows[0].contents[1:]]
            fare_rates = []
            fare_contents = []
            retval = {}
            for i in fare_rows[1:]:
                tds = i.findAll('td')
                fare_contents.append(tds[0].string)
                temp = []
                for j in  tds[1:] :
                    if j.contents[0]!='-':
                        temp.append(j.b.string)
                    else:
                        temp.append('-')
                fare_rates.append(temp)
            for i in fare_contents:
                retval[i]={}
                for j in fare_types:
                    retval[i][j] = fare_rates[fare_contents.index(i)][fare_types.index(j)]
            return retval

    def AvailToJson(self,string):
        string_arr = string.split('~')[1:]
        if ')' in string_arr[0]:
            return {'status':'No Results Found'}
        else:
            data = string_arr[0].split('^')
            data[0] = data[0].split('_')
            return {
            'train_no':data[0][0],
            'from_code': data[0][1],
            'to_code' : data[0][2],
            'class':data[0][3],
            'date':data[0][4],
            'status':data[1]
            }
