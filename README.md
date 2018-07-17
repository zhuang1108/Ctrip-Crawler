## Annex Description

The file *“ctrip.py”* is created to pick up the ticket information on Ctrip. The main idea of its implementation is:
  * set up the request head
  * obtain the JSON packets from the web site according to the request head
  * parse the JSON packets
  * store the data to the MySQL database

The file *“ctripTables.txt”* is the specification of database table building. According to the information field, three tables can be set up and each with the flight number as the unique primary key. Although this way of building tables makes it more complex to write MySQL statements to add, delete or modify data in the database (to get all the information of a flight we need to operate on three tables at the same time), it can reduce the storage space of data occupied by this way.


## URL Acquisition

The URL for getting JSON data is found in ulrs like [http://flights.ctrip.com/itinerary/oneway/sha-can?ddate1=2018-08-20](http://flights.ctrip.com/itinerary/oneway/sha-can?ddate1=2018-08-20). This website showed after the visitors being registered by CTRIP Website likes [http://flights.ctrip.com/booking/sha-can-day-1.html?ddate1=2018-08-20](http://flights.ctrip.com/booking/sha-can-day-1.html?ddate1=2018-08-20). The reason of Website changes may be due to the lack of restrictions on the access speed of the previous procedures to the website( `time.sleep(3)` ).

The URL for the request for JSON data is [http://flights.ctrip.com/itinerary/api/12808/products](http://flights.ctrip.com/itinerary/api/12808/products). The data parameter is necessary and the **Content-Type** field in the request header needs to be specified as ***application/json***.

Before sending the request header, you need to set the request parameter, which likes as follows:  
>data = {  
>>"flightWay":"Oneway",  
>>"classType":"ALL",  
>>"hasChild":'false',  
>>"hasBaby":'false',  
>>"searchIndex":1,  
>>"portingToken":"3211f7b0880646999ff07c74bf47478e",  
>>"airportParams":[{  
>>>"dcity":"SHA",  
>>>"acity":"TNA",  
>>>"dcityname":"上海",  
>>>"acityname":"济南",  
>>>"date":"2018-09-01",  
>>>"dcityid":2,  
>>>"acityid":144}]  
>}


## Test For Data In Database

notes: the database did not store all the data when performing these data query tests against the databse.

Mysql statements 1:  
>`select flightnumber,sharedflightnumber,airlinecode,airlinename,crafttypename,crafttypekinddisplayname,createdtime from  
> flight where flightnumber="HU7669";`   
![result 1](https://github.com/zhuang1108/MyFirstRepository/blob/master/images/QQ截图20180717191638.png)

Mysql statements 2:  
>`select flight.flightnumber,airportinfo.dcityname,airportinfo.acityname,characteristicsprice.lowestprice from  
> flight,airportinfo,characteristicsprice where flight.flightnumber=airportinfo.flightnumber and  
> flight.flightnumber=characteristicsprice.flightnumber and lowestprice<300;`   
![result 2](https://github.com/zhuang1108/MyFirstRepository/blob/master/images/QQ截图20180717183143.png)




