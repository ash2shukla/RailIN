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

        retval['train_base']=dic1

        data2 = data[1].split('~~~')
        data2_1 = data2[0].split('~')
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

        retval['train_base'] = dic1

        data2_arr = data2[1].split('~~')

        info_count = len(data2_arr)

        base_arr = data2_arr[0].split('~')

        retval['train_base']['type'] = base_arr[0]
        retval['train_base']['train_id'] = base_arr[1]
        retval['train_base']['distance_from_to'] = base_arr[7]
        retval['train_base']['average_speed'] = base_arr[8]
        if len(base_arr)==16:
            retval['train_base']['notif_coach'] = base_arr[12]
        else:
            pass
        try:
            retval['train_base']['notif_special'] = data2_arr[1].split('~')[3]
        except:
            pass
        try:
            # if this field has more words than a train type i.e. 3-4 then it is a notif
            if len(data_arr[2].split())>5:
                retval['train_base']['notif_special2'] = data2_arr[2]
            else:
                pass
        except:
            pass
        try:
            retval['train_base']['owned_by'] = data2_arr[3].split('~')[1]
        except:
            pass
        try:
            retval['train_base']['owned_by'] = data2_arr[3].split('~')[1]
        except:
            pass
        try:
            # if this part is having a alpha only string then it is owned by or region where train comes from
            val = data2_arr[4].split('~')[1]
            if all(i.isalpha() for i in val):
                retval['train_base']['owned_by'] = val
            else:
                retval['train_base']['rake_share'] = val
        except:
            pass
        try:
            val = data2_arr[5].split('~')[1]
            if ':' in val:
                retval['coach_arrangement'] = []
                for i in val.split(':'):
                    index = str(val.index(i))
                    i = i.split(',')
                    retval['coach_arrangement'].append({index : {'tag':i[0],'coach_id':i[1],'type':i[2]}})
            else:
                pass
        except:
            pass

        return retval

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
