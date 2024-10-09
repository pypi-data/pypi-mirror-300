# sealev
Allows to access various Sea Level Databases via python.
## Installation
To install the package use the command:     
```
pip install sealev
```
After the installation, it is possible to use the package in python:
```
python
```
## List of available databases: getDB()
Once you are in python environment you can give the following collamnds
```
from sealev.sldb import seaLevelDB
sl=seaLevelDB()
#
# get the list of available database sources:
dbs=sl.getDBs()
#
for db in dbs:
   print(db)
```
You will get a list of all the database that you can query.
# LIst the devices of a database: getDevs(\<database\>)

You can select one specific database, i.e. DART, and requst the list of available devices:
```
from sealev.sldb import seaLevelDB
sl=seaLevelDB()
darts=sl.getDevs('DART')
#
for dart in darts:
    print(dart['id'],dart['location'],format(dart['lat'])+'/'+format(dart['lon']))
#
```
The response will be:
```
21413 Station 21413 - SOUTHEAST TOKYO - 700NM ESE of Tokyo, JP 30.492/152.085
21414 Station 21414 - AMCHITKA - 170 NM South of Amchitka, AK 48.97/178.165
21415 Station 21415 - ATTU - 175 NM South of Attu, AK 50.12/171.867
21416 Station 21416 - KAMCHATKA PENINSULA - 240NM SE of Kamchatka Peninsula, RU 48.12/163.43
21418 Station 21418 - NORTHEAST TOKYO - 450 NM NE of Tokyo, JP 38.73/148.8
...
56003 Station 56003 - Indian Ocean 2     -     630km NNE of Dampier -15.019/118.073

```

The response if a list of devices; each device is a dictionary composed of:
- id   identifier of the device (will be used to retrieve data)
- location   place of the device
- country   country of the device
- lat/lon   coordinates of the device
- [group]   if it exists it represents a subclass of the database

the keyword 'id' contains the reference identifier to retrieve the level data.
## Retrieve sea level of a device: getLevel(\<database\>,\<device\>, \[\<tmin\>\],\[\<tmax\>\])
Suppose you want to retrieve the level values of one specific device, such as 21414 (Station 21414 - AMCHITKA - 170 NM South of Amchitka), you can give the following command:
```
from sealev.sldb import seaLevelDB
sl=seaLevelDB()
values=sl.getLevel('DART','21414')
for j in range(len(values['x'])):
    print(values['x'][j],values['y'][j])
```
The response of the example above is a list of data if the device has recent recorded data:
```
2024-10-02 00:00:00 5442.868
2024-10-02 00:15:00 5442.874
2024-10-02 00:30:00 5442.882
2024-10-02 00:45:00 5442.891
2024-10-02 01:00:00 5442.897
...
```
You can retrieve data from the past adding the keyword tmin, tmax in the getLevel call. Example
```
from sealev.sldb import seaLevelDB
sl=seaLevelDB()
values=sl.getLevel('GLOSS @vliz','mnza','2022-09-19 00:00:00','2022-09-21 00:00:00')
for j in range(len(values['x'])):
    print(values['x'][j],values['y'][j])
```
The example above retrieves and print the data related to the Tsunami event in Mexico.
![mexico_mnza](https://github.com/user-attachments/assets/a39715ed-7fb7-4e30-a16f-fccd189e6c83)

The response is a dctionary containing the following keys:
-   x   (list) containing a series of datatime values representing the time of the level
-   y   (list) containing a series of sea level values of the device (m)
each point of the x list will have a corresponding point in y
In the example above, if you have setup the matplotlib package (pip install matplotlib), you can plot the quantities with the commands:
  
```
import matplotlib.pyplot as plt
plt.plot(values['x'],values['y'])
plt.xlabel('Date/Time')
plt.ylabel('Level (m)')
plt.title('M7.6 MEXICO, 2022-09-19 18:05:00')
plt.show()
```
The following plot would be generated:
![Figure_1](https://github.com/user-attachments/assets/1e22fe49-07ce-454c-b1c9-f360a580d3e1)

As another example, let's show the Hurricane Helene 2024 at Clearwater Beach (USA)
```
from sealev.sldb import seaLevelDB
import matplotlib.pyplot as plt

sl=seaLevelDB()
values=sl.getLevel('GLOSS @vliz','cwfl','2024-09-24 00:00:00','2024-09-29 00:00:00')

plt.plot(values['x'],values['y'])
plt.xlabel('Date/Time')
plt.ylabel('Level (m)')
plt.title('Clearwater Beach (FL), Cyclone Helene-24')
plt.show()
```
the output will be:
![helene](https://github.com/user-attachments/assets/be44627b-a0c1-492b-a0a1-ca90463c7b2c)

##  Export to csv file:  to_csv(values,fnameout)
After having retrieved the values dictionary, you can export in a csv file.  Example

```
from sealev.sldb import seaLevelDB
sl=seaLevelDB()
values=sl.getLevel('GLOSS @vliz','mnza','2022-09-19 00:00:00','2022-09-21 00:00:00')
sl.to_csv(values,'output.csv')
```

## Extract other quantities
In some cases (i.e. JRC_TAD database), many other quantities are retrieved from the database in addition to the level.  In these cases the available keys are many more thabn x and y, that however always eist.  The other quantities can also be retrieved.
The xample below collects the data of Cadiz (IDSL-06) from the JRC database and creates a plot of the battery voltage.
```
import matplotlib.pyplot as plt
from sealev.sldb import seaLevelDB
sl=seaLevelDB()
#
values=sl.getLevel('JRC_TAD','IDSL-06','2024-10-03 00:00:00','2024-10-08 00:00:00')
print('List of possible quantities to plot:',values.keys())
plt.plot(values['x'],values['anag3'])
plt.xlabel('Date/Time')
plt.ylabel('Battery voltage (volt)')
plt.title('Cadiz device IDSL-06')
plt.show()
```
The output plot is the folllowing:
![voltage](https://github.com/user-attachments/assets/ded5d7ed-0fcf-46cc-bc52-25d12bcc80e3)
