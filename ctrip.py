# coding=utf-8
import requests
import json
import random
import time
import pymysql
import threading
import queue
from json.decoder import JSONDecodeError

# 设置单线程锁，控制mysql数据库插入更新操作
lock = threading.Lock()

# citycode字典, cityid字典 均解析自 http://flights.ctrip.com/itinerary/api/poi/get 获取的json数据

hotcities = {
	'BJS':'北京','SHA':'上海','CAN':'广州','SZX':'深圳',
	'CTU':'成都','HGH':'杭州','WUH':'武汉','SIA':'西安',
	'CKG':'重庆','TAO':'青岛','CSX':'长沙','NKG':'南京',
	'XMN':'厦门','KMG':'昆明','DLC':'大连','TSN':'天津',
	'CGO':'郑州','SYX':'三亚','TNA':'济南','FOC':'福州'
}


citycodes = {
	'AAT':'阿勒泰','AKU':'阿克苏','AOG':'鞍山','AQG':'安庆','AVA':'安顺','AXF':'阿拉善左旗',
	'MFM':'澳门','NGQ':'阿里','RHT':'阿拉善右旗','YIE':'阿尔山','AEB':'百色','BAV':'包头','BFJ':'毕节',
	'BHY':'北海','BJS':'北京','NAY':'北京(南苑机场)','PEK':'北京(首都国际机场)','BPL':'博乐',
	'BSD':'保山','DBC':'白城','KJI':'布尔津','NBS':'白山','RLK':'巴彦淖尔','BPX':'昌都','CDE':'承德',
	'CGD':'常德','CGQ':'长春','CHG':'朝阳','CIF':'赤峰','CIH':'长治','CKG':'重庆','CSX':'长沙',
	'CTU':'成都','CWJ':'沧源','CZX':'常州','JUH':'池州','SWA':'潮州','SWA':'潮汕','DAT':'大同',
	'DAX':'达县','DAX':'达州','DCY':'稻城','DDG':'丹东','DIG':'迪庆','DLC':'大连','DLU':'大理',
	'DNH':'敦煌','DOY':'东营','DQA':'大庆','HXD':'德令哈','LUM':'德宏','DSN':'鄂尔多斯','EJN':'额济纳旗',
	'ENH':'恩施','ERL':'二连浩特','FOC':'福州','FUG':'阜阳','FUO':'佛山','FYJ':'抚远','FYN':'富蕴',
	'CAN':'广州','GMQ':'果洛','GOQ':'格尔木','GYS':'广元','GYU':'固原','KHH':'高雄','KOW':'赣州',
	'KWE':'贵阳','KWL':'桂林','AHJ':'红原','HAK':'海口','HCJ':'河池','HDG':'邯郸','HEK':'黑河',
	'HET':'呼和浩特','HFE':'合肥','HGH':'杭州','HIA':'淮安','HJJ':'怀化','HLD':'海拉尔','HMI':'哈密',
	'HNY':'衡阳','HRB':'哈尔滨','HTN':'和田','HTT':'花土沟','HUN':'花莲','HUO':'霍林郭勒','HUZ':'惠州',
	'HZG':'汉中','TXN':'黄山','CYI':'嘉义','JDZ':'景德镇','JGD':'加格达奇','JGN':'嘉峪关','JGS':'井冈山',
	'JHG':'景洪','JIC':'金昌','JIU':'九江','JJN':'晋江','JMU':'佳木斯','JNG':'济宁','JNZ':'锦州',
	'JXA':'鸡西','JZH':'九寨沟','KNH':'金门','SWA':'揭阳','TNA':'济南','KCA':'库车','KGT':'康定',
	'KHG':'喀什','KJH':'凯里','KMG':'昆明','KRL':'库尔勒','KRY':'克拉玛依','HZH':'黎平','JMJ':'澜沧',
	'LCX':'龙岩','LFQ':'临汾','LHW':'兰州','LJG':'丽江','LLB':'荔波','LLV':'吕梁','LNJ':'临沧',
	'LPF':'六盘水','LXA':'拉萨','LYA':'洛阳','LYG':'连云港','LYI':'临沂','LZH':'柳州','LZO':'泸州',
	'LZY':'林芝','LUM':'芒市','MDG':'牡丹江','MFK':'马祖','MIG':'绵阳','MXZ':'梅州','MZG':'马公',
	'NZH':'满洲里','OHE':'漠河','KHN':'南昌','LZN':'南竿','NAO':'南充','NGB':'宁波','NKG':'南京',
	'NLH':'宁蒗','NNG':'南宁','NNY':'南阳','NTG':'南通','MZG':'澎湖列岛','PZI':'攀枝花','SYM':'普洱',
	'BAR':'琼海','BPE':'秦皇岛','IQM':'且末','IQN':'庆阳','JIQ':'黔江','JJN':'泉州','JUZ':'衢州',
	'NDG':'齐齐哈尔','TAO':'青岛','RIZ':'日照','RKZ':'日喀则','HPG':'神农架','QSZ':'莎车','SHA':'上海',
	'PVG':'上海(浦东国际机场)','SHA':'上海(虹桥国际机场)','SHE':'沈阳','SHF':'石河子','SJW':'石家庄',
	'SQD':'上饶','SQJ':'三明','SWA':'汕头','SYX':'三亚','SZX':'深圳','WDS':'十堰','WGN':'邵阳',
	'HYN':'台州','RMQ':'台中','TCG':'塔城','TCZ':'腾冲','TEN':'铜仁','TGO':'通辽','THQ':'天水',
	'TLQ':'吐鲁番','TNH':'通化','TNN':'台南','TPE':'台北','TSN':'天津','TTT':'台东','TVS':'唐山',
	'TYN':'太原','YTY':'泰州','HLH':'乌兰浩特','UCB':'乌兰察布','URC':'乌鲁木齐','WEF':'潍坊','WEH':'威海',
	'WNH':'文山','WNZ':'温州','WUA':'乌海','WUH':'武汉','WUS':'武夷山','WUX':'无锡','WUZ':'梧州',
	'WXN':'万州','ACX':'兴义','GXH':'夏河','HKG':'香港','JHG':'西双版纳','NLT':'新源','SIA':'西安',
	'WUT':'忻州','XFN':'襄阳','XIC':'西昌','XIL':'锡林浩特','XMN':'厦门','XNN':'西宁','XUZ':'徐州',
	'ENY':'延安','INC':'银川','LDS':'伊春','LLF':'永州','UYN':'榆林','YBP':'宜宾','YCU':'运城',
	'YIC':'宜春','YIH':'宜昌','YIN':'伊宁','YIW':'义乌','YKH':'营口','YNJ':'延吉','YNT':'烟台',
	'YNZ':'盐城','YTY':'扬州','YUS':'玉树','CGO':'郑州','DYG':'张家界','HSN':'舟山','NZL':'扎兰屯',
	'YZY':'张掖','ZAT':'昭通','ZHA':'湛江','ZHY':'中卫','ZQZ':'张家口','ZUH':'珠海','ZYI':'遵义'
}


cityids = {
	'阿勒泰':175,'阿克苏':173,'鞍山':178,'安庆':177,'安顺':179,'阿拉善左旗':21269,'澳门':59,
	'阿里':97,'阿拉善右旗':21863,'阿尔山':1658,'百色':1140,'包头':141,'毕节':22031,'北海':189,
	'北京':1,'北京(南苑机场)':1,'北京(首都国际机场)':1,'博乐':2548,'保山':197,'白城':1116,
	'布尔津':3326,'白山':199,'巴彦淖尔':3887,'昌都':575,'承德':562,'常德':201,'长春':158,'朝阳':211,
	'赤峰':202,'长治':137,'重庆':4,'长沙':206,'成都':28,'沧源':21741,'常州':213,'池州':218,'潮州':215,
	'潮汕':956,'大同':136,'达县':234,'达州':234,'稻城':1222,'丹东':221,'迪庆':93,'大连':6,'大理':36,
	'敦煌':11,'东营':236,'大庆':231,'德令哈':2542,'德宏':3997,'鄂尔多斯':3976,'额济纳旗':21339,
	'恩施':245,'二连浩特':7626,'福州':258,'阜阳':257,'佛山':251,'抚远':21943,'富蕴':255,'广州':32,
	'果洛':21862,'格尔木':132,'广元':267,'固原':321,'高雄':720,'赣州':268,'贵阳':38,'桂林':33,
	'红原':7835,'海口':42,'河池':3969,'邯郸':275,'黑河':281,'呼和浩特':103,'合肥':278,'杭州':17,
	'淮安':577,'怀化':282,'海拉尔':142,'哈密':285,'衡阳':297,'哈尔滨':5,'和田':294,'花土沟':83679,
	'花莲':6954,'霍林郭勒':21091,'惠州':299,'汉中':129,'黄山':23,'嘉义':5152,'景德镇':305,'加格达奇':1143,
	'嘉峪关':326,'井冈山':307,'景洪':35,'金昌':1158,'九江':24,'晋江':406,'佳木斯':317,'济宁':318,
	'锦州':327,'鸡西':157,'九寨沟':91,'金门':7203,'揭阳':956,'济南':144,'库车':329,'康定':4130,'喀什':109,
	'凯里':333,'昆明':34,'库尔勒':330,'克拉玛依':166,'黎平':3852,'澜沧':21596,'龙岩':348,'临汾':139,
	'兰州':100,'丽江':37,'荔波':1708,'吕梁':7631,'临沧':1236,'六盘水':605,'拉萨':41,'洛阳':350,'连云港':353,
	'临沂':569,'柳州':354,'泸州':355,'林芝':108,'芒市':3997,'牡丹江':150,'马祖':7808,'绵阳':370,'梅州':3053,
	'马公':5383,'满洲里':1083,'漠河':155,'南昌':376,'南竿':91804,'南充':377,'宁波':375,'南京':12,'宁蒗':1161,
	'南宁':380,'南阳':385,'南通':82,'澎湖列岛':5383,'攀枝花':1097,'普洱':3996,'琼海':52,'秦皇岛':147,
	'且末':399,'庆阳':404,'黔江':7708,'泉州':406,'衢州':407,'齐齐哈尔':149,'青岛':7,'日照':1106,'日喀则':92,
	'神农架':657,'莎车':21827,'上海':2,'上海(浦东国际机场)':2,'上海(虹桥国际机场)':2,'沈阳':451,'石河子':426,
	'石家庄':428,'上饶':411,'三明':437,'汕头':447,'三亚':43,'深圳':30,'十堰':452,'邵阳':1111,'台州':578,
	'台中':3849,'塔城':455,'腾冲':1819,'铜仁':1227,'通辽':458,'天水':464,'吐鲁番':21811,'通化':456,
	'台南':3847,'台北':617,'天津':3,'台东':3848,'唐山':468,'太原':105,'泰州':15,'乌兰浩特':484,
	'乌兰察布':7518,'乌鲁木齐':39,'潍坊':475,'威海':479,'文山':1342,'温州':491,'乌海':1133,'武汉':477,
	'武夷山':26,'无锡':13,'梧州':492,'万州':487,'兴义':1139,'夏河':497,'香港':58,'西双版纳':35,'新源':3360,
	'西安':10,'忻州':513,'襄阳':496,'西昌':494,'锡林浩特':500,'厦门':25,'西宁':124,'徐州':512,'延安':110,
	'银川':99,'伊春':517,'永州':970,'榆林':527,'宜宾':514,'运城':140,'宜春':518,'宜昌':515,'伊宁':529,
	'义乌':536,'营口':1300,'延吉':523,'烟台':533,'盐城':1200,'扬州':15,'玉树':7582,'郑州':559,'张家界':27,
	'舟山':19,'扎兰屯':1135,'张掖':663,'昭通':555,'湛江':547,'中卫':556,'张家口':550,'珠海':31,'遵义':558
}

citycode_list = []
cityname_list = []
for citycode,cityname in citycodes.items():
	citycode_list.append(citycode)
	cityname_list.append(cityname)


# 随机生成由32位十六进制组成的字符串, 用于组成请求头的 refer 字段
def Random_Porting_Token():
	portingToken = ''
	randomlist = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
	for i in range(32):
		portingToken += random.choice(randomlist)
	return portingToken

# 请求头及请求参数设置，data参数不可或缺
def SetHeadersAndParams(dcitycode, acitycode, searchdate = '2018-08-25'):
	dcityname = citycodes[dcitycode]
	acityname = citycodes[acitycode]
	dcityid = cityids[dcityname]
	acityid = cityids[acityname]

	srcurl = 'http://flights.ctrip.com/itinerary/oneway/{}-{}?date={}&portingToken='.format(dcitycode, acitycode, searchdate)
	srcurl = srcurl + Random_Porting_Token()

	# content-type字段指定请求数据文件类型
	headers = {
		'POST':'/itinerary/api/12808/products HTTP/1.1',
		'Host': 'flights.ctrip.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
		'Accept': '*/*',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': srcurl,
		'content-type': 'application/json',
		'origin': 'http://flights.ctrip.com',
		'Connection': 'keep-alive'
	}

	# data = {"flightWay":"Oneway","classType":"ALL","hasChild":'false',"hasBaby":'false',"searchIndex":1,"portingToken":"3211f7b0880646999ff07c74bf47478e","airportParams":[{"dcity":"SHA","acity":"TNA","dcityname":"上海","acityname":"济南","date":"2018-09-01","dcityid":2,"acityid":144}]}
	data = {
		"flightWay":"Oneway",
		"classType":"ALL",
		"hasChild":'false',
		"hasBaby":'false',
		"searchIndex":1,
		"airportParams":[{
			"dcity":dcitycode,
			"acity":acitycode,
			"dcityname":dcityname,
			"acityname":acityname,
			"date":searchdate,
			"dcityid":dcityid,
			"acityid":acityid}]
	}

	return headers, json.dumps(data)

# 根据请求头获取json数据，并先判断通航情况
def GetJsonData(dcity, acity, searchdate = '2018-08-25'):

	if dcity not in cityname_list and dcity not in citycode_list:
		print('Departure city is illegal.')
		return None
	elif dcity in cityname_list:
		dcode_index = cityname_list.index(dcity)
		dcity = citycode_list[dcode_index]

	if acity not in cityname_list and acity not in citycode_list:
		print('Arrival city is illegal.')
		return None
	elif acity in cityname_list:
		acode_index = cityname_list.index(acity)
		acity = citycode_list[acode_index]

	headers, data = SetHeadersAndParams(dcity, acity, searchdate)
	req = requests.post('http://flights.ctrip.com/itinerary/api/12808/products', headers = headers, data = data)
	# print(req.text)
	try:
		jsonData = json.loads(req.text)
	except JSONDecodeError as e:
		print('The data is illegal, do not match the json format')
		return None

	# print(jsonData)
	try:
		if jsonData.get('data').get('error') != None:
			# error取值要么为null，要么为： {'code':'103','message':'不通航'}
			return None
	except KeyError as e:
		print('No such key as data.error in the json data...')
		return None

	return jsonData

# 将获取到的json包进行解析并存至数据库
def SaveDataToMysql(jsonData):

	conn = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = '123456', db = 'ctrip', charset = 'utf8')
	cur = conn.cursor()

	try:
		routeList = jsonData['data']['routeList']
		for eachFlight in routeList:
			# print(eachFlight['routeType'])
			# 直飞航班 routeType 为 Flight
			if eachFlight['routeType'] == 'Flight':
				legs = eachFlight['legs']
				flight = legs[0]['flight']
				cabins = legs[0]['cabins']
				characteristic = legs[0]['characteristic']

				# 航班号，共享航班号及共享航班名，航空公司及其代码，机型，特殊机型情况
				flightNumber = flight['flightNumber']
				sharedFlightNumber = flight['sharedFlightNumber']
				sharedFlightName = flight['sharedFlightName']
				airlineCode = flight['airlineCode']
				airlineName = flight['airlineName']
				craftTypeCode = flight['craftTypeCode']
				craftKind = flight['craftKind']
				craftTypeName = flight['craftTypeName']
				craftTypeKindDisplayName = flight['craftTypeKindDisplayName']
				specialCraft = flight['specialCraft']
				# print(flightNumber, sharedFlightNumber, sharedFlightName, airlineCode, airlineName, craftTypeCode, craftKind, craftTypeName, craftTypeKindDisplayName, specialCraft)
			
				departureAirportInfo = flight['departureAirportInfo']
				arrivalAirportInfo = flight['arrivalAirportInfo']

				# 起飞城市及其三字代码，出发机场
				dcityTlc = departureAirportInfo['cityTlc']
				dcityName = departureAirportInfo['cityName']
				dairportTlc = departureAirportInfo['airportTlc']
				dairportName = departureAirportInfo['airportName']
				dterminalName = departureAirportInfo['terminal']['name']

				# 抵达城市及其三字代码，到达机场
				acityTlc = arrivalAirportInfo['cityTlc']
				acityName = arrivalAirportInfo['cityName']
				aairportTlc = arrivalAirportInfo['airportTlc']
				aairportName = arrivalAirportInfo['airportName']
				aterminalName = arrivalAirportInfo['terminal']['name']

				# 出发时间，抵达时间
				departureDate = flight['departureDate']
				arrivalDate = flight['arrivalDate']
				# print(dcityTlc, dcityName, dairportTlc, dairportName, dterminalName, acityTlc, acityName, aairportTlc, aairportName, aterminalName)
				# print(departureDate, arrivalDate)

				# 历史误点率，历史平均误点率
				comfort = flight['comfort']
				if comfort == '':
					comfortHistoryPunctuality = comfortHistoryPunctualityArr = 0
				else:
					comfortJsonData = json.loads(comfort)
					comfortHistoryPunctuality = comfortJsonData['HistoryPunctuality']
					comfortHistoryPunctualityArr = comfortJsonData['HistoryPunctualityArr']
					if comfortHistoryPunctuality == '':
						comfortHistoryPunctuality = '0%'
					if comfortHistoryPunctualityArr == '':
						comfortHistoryPunctualityArr = '0%'
					comfortHistoryPunctuality = int(comfortHistoryPunctuality.replace('%', ''))
					comfortHistoryPunctualityArr = int(comfortHistoryPunctualityArr.replace('%', ''))
				# print(comfortHistoryPunctuality, comfortHistoryPunctualityArr)

				# 最低价格，最低头等舱价格
				lowestPrice = characteristic['lowestPrice']
				lowestCfPrice = characteristic['lowestCfPrice']
				# print(lowestPrice, lowestCfPrice)

				# 经济舱(Y)，公务舱(C)，头等舱(F) 标价
				standardPrices = characteristic['standardPrices']
				if standardPrices == None:
					standardPriceY = standardPriceC = standardPriceF = 0
				else:
					if len(standardPrices) == 3:
						standardPriceY = standardPrices[0]['price']
						standardPriceC = standardPrices[1]['price']
						standardPriceF = standardPrices[2]['price']
					elif len(standardPrices) == 2:
						standardPriceY = standardPrices[0]['price']
						standardPriceC = standardPrices[1]['price']
						standardPriceF = 0
					else:
						standardPriceY = standardPrices[0]['price']
						standardPriceC = 0
						standardPriceF = 0
				# print(standardPriceY, standardPriceC, standardPriceF)

				# 最低票价及最低折扣（三种舱位）
				lowestSalePriceY = lowestSalePriceC = lowestSalePriceF = 0
				lowestRateY = lowestRateC = lowestRateF = 0.0
				for eachCabin in cabins:
					price = eachCabin['price']
					if eachCabin['cabinClass'] == 'Y':
						if lowestSalePriceY == 0 or lowestSalePriceY >= price['salePrice']:
							lowestSalePriceY = price['salePrice']
						if lowestRateY == 0.0 or lowestRateY >= price['rate']:
							lowestRateY = price['rate']

					if eachCabin['cabinClass'] == 'C':
						if lowestSalePriceC == 0 or lowestSalePriceC >= price['salePrice']:
							lowestSalePriceC = price['salePrice']
						if lowestRateC == 0.0 or lowestRateC >= price['rate']:
							lowestRateC = price['rate']

					if eachCabin['cabinClass'] == 'F':
						if lowestSalePriceF == 0 or lowestSalePriceF >= price['salePrice']:
							lowestSalePriceF = price['salePrice']
						if lowestRateF == 0.0 or lowestRateF >= price['rate']:
							lowestRateF = price['rate']
				# print(lowestSalePriceY, lowestSalePriceC, lowestSalePriceF, lowestRateY, lowestRateC, lowestRateF)

				# 数据库中已有该航班信息则更新，无则插入该航班信息
				cur.execute("""SELECT * FROM Flight,AirportInfo,CharacteristicsPrice 
					WHERE Flight.flightNumber = %s 
					AND Flight.flightNumber=AirportInfo.flightNumber 
					AND Flight.flightNumber=CharacteristicsPrice.flightNumber""", (flightNumber))
				if cur.rowcount == 0:
					cur.execute("""INSERT INTO Flight (
						flightNumber, sharedFlightNumber, sharedFlightName, airlineCode, 
						airlineName, craftTypeCode, craftKind, craftTypeName,
						craftTypeKindDisplayName, specialCraft) VALUES (
							%s, %s, %s, %s,
							%s,	%s, %s, %s,
							%s, %s)""", (
						flightNumber, sharedFlightNumber, sharedFlightName, airlineCode, 
						airlineName, craftTypeCode, craftKind, craftTypeName,
						craftTypeKindDisplayName, specialCraft))

					cur.execute("""INSERT INTO AirportInfo (
						flightNumber, dcityTlc, dcityName, dairportTlc, dairportName, dterminalName, 
						acityTlc, acityName, aairportTlc, aairportName, aterminalName, departureDate, 
						arrivalDate, comfortHistoryPunctuality, comfortHistoryPunctualityArr) VALUES (
							%s, %s, %s, %s, %s, %s,
							%s,	%s,	%s,	%s, %s, %s,
							%s,	%s, %s)""", (
						flightNumber, dcityTlc, dcityName, dairportTlc, dairportName, dterminalName, 
						acityTlc, acityName, aairportTlc, aairportName, aterminalName, departureDate, 
						arrivalDate, comfortHistoryPunctuality, comfortHistoryPunctualityArr))

					cur.execute("""INSERT INTO CharacteristicsPrice (
						flightNumber, lowestPrice, lowestCfPrice, standardPriceY, 
						standardPriceC,	standardPriceF, lowestSalePriceY, lowestSalePriceC, 
						lowestSalePriceF, lowestRateY, lowestRateC, lowestRateF) VALUES (
							%s, %s, %s, %s,
							%s,	%s, %s, %s,
							%s, %s, %s, %s)""", (
						flightNumber, lowestPrice, lowestCfPrice, standardPriceY, 
						standardPriceC,	standardPriceF, lowestSalePriceY, lowestSalePriceC, 
						lowestSalePriceF, lowestRateY, lowestRateC, lowestRateF))

					conn.commit()
					print('The flight %s has been inserted into the database.' % flightNumber)
				else:
					cur.execute("""UPDATE Flight SET 
						sharedFlightNumber=%s, sharedFlightName=%s, airlineCode=%s, 
						airlineName=%s, craftTypeCode=%s, craftKind=%s, craftTypeName=%s, 
						craftTypeKindDisplayName=%s, specialCraft=%s 
						WHERE flightNumber=%s;""", (
						sharedFlightNumber, sharedFlightName, airlineCode, 
						airlineName, craftTypeCode, craftKind, craftTypeName,
						craftTypeKindDisplayName, specialCraft, flightNumber))

					cur.execute("""UPDATE AirportInfo SET 
						dcityTlc=%s, dcityName=%s, dairportTlc=%s, dairportName=%s, dterminalName=%s, 
						acityTlc=%s, acityName=%s, aairportTlc=%s, aairportName=%s, aterminalName=%s, 
						departureDate=%s, arrivalDate=%s, comfortHistoryPunctuality=%s, comfortHistoryPunctualityArr=%s 
						WHERE flightNumber=%s;""", (
						dcityTlc, dcityName, dairportTlc, dairportName, dterminalName, 
						acityTlc, acityName, aairportTlc, aairportName, aterminalName, 
						departureDate, arrivalDate, comfortHistoryPunctuality, comfortHistoryPunctualityArr, flightNumber))

					cur.execute("""UPDATE CharacteristicsPrice SET	
						lowestPrice=%s, lowestCfPrice=%s, standardPriceY=%s, standardPriceC=%s,	
						standardPriceF=%s, lowestSalePriceY=%s, lowestSalePriceC=%s, lowestSalePriceF=%s, 
						lowestRateY=%s, lowestRateC=%s, lowestRateF=%s 
						WHERE flightNumber=%s;""", (
						lowestPrice, lowestCfPrice, standardPriceY, standardPriceC, 
						standardPriceF, lowestSalePriceY, lowestSalePriceC, lowestSalePriceF, 
						lowestRateY, lowestRateC, lowestRateF, flightNumber))

					conn.commit()
					print('The flight %s in the database has been updated.' % flightNumber)
	except pymysql.err.ProgrammingError:
		print('You have some errors in your SQL syntax.')
	finally:
		cur.close()
		conn.close()

# 多线程执行函数
def MultiThreading(dcityname, acityname, dcitycode, acitycode, searchdate):

	jsonData = GetJsonData(dcitycode, acitycode, searchdate)
	lock.acquire()
	print('正在处理 %s 到 %s 的机票信息...' % (dcityname, acityname))
	# print(threading.current_thread())
	if jsonData == None:
		print('code: 103, message: 不通航')
	else:
		SaveDataToMysql(jsonData)
		print('The json data package of this flight has been managed.\n')
	lock.release()

# main controller
def ManagerFunction(searchdate):

	print('.....Start The Robot Now.....\n')
	part_queue = queue.Queue()

	#for dcitycode, dcityname in sorted(citycodes.items()):
	for dcitycode, dcityname in sorted(hotcities.items()):
		#for acitycode, acityname in sorted(citycodes.items()):
		for acitycode, acityname in sorted(hotcities.items()):
			if dcitycode != acitycode:
				eachparams = [dcityname, acityname, dcitycode, acitycode, searchdate]
				part_queue.put(eachparams)
						
		multithreads = []
		#print(part_queue.qsize())
		while not part_queue.empty():
			for i in range(7):
				# get()时如果队列为空则默认将当前线程阻塞，需要将此情况改为退出循环
				# part_queue.get_nowait()
				try:
					# block=False 当队列为空时抛出队列空异常
					t = threading.Thread(target = MultiThreading, args = part_queue.get(block = False))
					multithreads.append(t)
					t.start()
				except queue.Empty:
					break

			# 等所有子线程完成任务后再执行主线程，否则主线程等待
			for t in multithreads:
				t.join()
			time.sleep(random.randint(3,5))
			print('just wait no more than 5 seconds.\n')

		print('*'*40 + 'Flights from %s finished.' % dcityname + '*'*40 + '\n')
		time.sleep(random.randint(7,15))

	print('.....Congratulations to you!!! You have got all data.....')


if __name__ == '__main__':
	# 获取某个日期全国所有航班的信息
	ManagerFunction('2018-08-15')
	# 获取固定城市的航班
	# jsonData = GetJsonData('三亚', '重庆', '2018-08-15')
	# SaveDataToMysql(jsonData)
	
