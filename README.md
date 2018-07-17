Annex Description：

1. The file “ctrip.py” is created to pick up the ticket information on Ctrip. The main idea of its implementation is:
  (1). set up the request head；
  (2). obtain the JSON packets from the web site according to the request head；
  (3). parse the JSON packets；
  (4). store the data to the MySQL database.

2. The file “ctripTables.txt” is the specification of database table building. According to the information field, three tables can be set up and each with the flight number as the unique primary key. Although this way of building tables makes it more complex to write MySQL statements to add, delete or modify data in the database (to get all the information of a flight we need to operate on three tables at the same time), it can reduce the storage space of data occupied by this way.


URL Acquisition：
  The URL for getting JSON data is found in http://flights.ctrip.com/itinerary/oneway/sha-can?ddate1=2018-08-20. I got this website after being registered by CTRIP Website in http://flights.ctrip.com/booking/sha-can-day-1.html?ddate1=2018-08-20. The reason of Website changes may be due to the lack of restrictions on the access speed of the previous procedures to the web site(like time.sleep(3)).
   The URL for the request for JSON data is http://flights.ctrip.com/itinerary/api/12808/products. The data parameter is necessary and the Content-Type field in the request header needs to be specified as application/json. 
