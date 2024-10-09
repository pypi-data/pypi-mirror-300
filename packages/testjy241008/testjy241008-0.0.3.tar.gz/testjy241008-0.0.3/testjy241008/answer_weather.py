import requests
from datetime import datetime
import xmltodict



def get_current_date():
    current_date = datetime.now().date()
    str_current_data = current_date.strftime("%Y%m%d")
    # tomorrow = int(str_current_data)+1
    tomorrow = int(str_current_data)
    # print(tomorrow)
    return str(tomorrow)

def get_current_hour():
    now = datetime.now()
    return now.strftime("%H%M")

int_to_weather = {
    "0": "맑음",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림"
}

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst' # 초단기예보

keys = str()

params ={'serviceKey' : keys, 
         'pageNo' : '1', 
         'numOfRows' : '10', 
         'dataType' : 'XML', 
         'base_date' : get_current_date(), 
         'base_time' : get_current_hour(), 
         'nx' : '55', 
         'ny' : '127' }


def set_keys(input: str):
    params['serviceKey'] = input


def forecast_degree(params):
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url, params)

    #XML -> 딕셔너리
    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    # print(dict_data)
    temp = str()
    sky = str()

    for item in dict_data['response']['body']['items']['item']:
        if item['category'] == 'T1H':
            temp = item['obsrValue']

    return float(temp)
        # 강수형태: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)


def forecast_status():
    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url, params)

    #XML -> 딕셔너리
    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    # print(dict_data)

    temp = str()
    sky = str()

    for item in dict_data['response']['body']['items']['item']:
        # 강수형태: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if item['category'] == 'PTY':
            sky = item['obsrValue']

    return int(sky)



# print(forecast_status())


day_status = {
    '오늘': 0,
    '내일': 1
}

city_status = {
    '서울': [0, 0]
}


def query(input_string: str):
    day_str = str()
    city_str = str()
    return_str = str()

    if '날씨' in input_string:
        if '오늘' in input_string:
            # params['base_date'] = "오늘"
            day_str = '오늘'
            pass
        elif '내일' in input_string:
            # params['base_date'] = "내일"
            day_str = '내일'
            pass
        else:
            return "날짜 입력 정보가 올바르지 않습니다."


        for city in city_status.keys():
            if city in input_string:
                # params['nx'] = city_status[city][0]
                # params['ny'] = city_status[city][1]
                city_str = city
                pass
            else:
                return "도시 정보가 올바르지 않습니다."

        return_str = day_str + " " + city_str + "의 날씨는 "

        sky_status = forecast_status()

        if sky_status == 0:
            return return_str+"맑습니다."
            pass
        elif sky_status == 1:
            return return_str+"비가 오고 흐립니다."
            pass
        elif sky_status == 2:
            return return_str+'비와 눈이 내립니다.'
            pass
        elif sky_status == 3:
            return return_str+'눈이 내립니다.'
            pass
        elif sky_status == 5:
            return return_str+'빗방울이 내립니다.'
            pass
        elif sky_status == 6:
            return return_str+'빗방울과 눈이 날립니다.'
            pass
        elif sky_status == 7:
            return return_str+'눈발이 날립니다.'
            pass
        else:
            return "날씨 입력 정보가 올바르지 않습니다."
    



