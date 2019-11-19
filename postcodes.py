import requests
import time
import json
import csv

api_key = 'pk.d8a3afc49f5f76f0e7287c9d86f474ac'
address = ""
adlist = []
criteria = input("Search criteria help narrow the scope of the addresses. Beginning of postcodes like 'G3, KA7, PA13' \n"
                 "or council areas such as 'South Lanarkshire, South Ayrshire, Dumfries & Galloway' can help with \n"
                 "correct retrieval. \n"
                 "\n"
                 "Please enter one search criteria: ")
print('Please open file "addresses.txt" and enter a comma separated list of street names and or house numbers. You may \n'
      'use other address identifiers however only one identifier can be used per address.')
ready = input('This script will generate the highest confidence full address based on your search criteria. This \n '
              'information can be found in "addresses_info.txt" in the same location as the script, in the same order as \n'
              'the input data. \n'
              '\n'
              'Press "y" then enter to continue. ')
if ready.lower() == 'y':
    with open('addresses.txt') as read_file:
        csv_reader = csv.reader(read_file, delimiter=",")
        for row in csv_reader:
            print("Imported: ", row)
            adlist.append(row)
url = "http://eu1.locationiq.com/v1/search.php"
with open('addresses_info.txt', 'a') as the_file:
    for x in adlist:
        v = ''
        for s in range(len(x)):
            if x[s] != '':
                v += x[s]
        time.sleep(0.5)
        try:
            address = v
            requesturl = url + "?key=" + api_key + "&q=" + address + "&format=JSON"
            response = requests.get(requesturl).json()
            for x in range(len(response)):
                if response[x]['display_name'].find(criteria) > 0:
                    final = response[x]['display_name']
                    print(final)
                    the_file.write(final)
                else:
                    final = "ADDRESS FOUND BUT NOT IN {} AREA".format(criteria)
                    the_file.write(final + " " + response[x]['display_name'])
        except ValueError as e:
            print(e, " ValueError, " + address)
            the_file.write(address + "VALUE ERROR \n")
        except KeyError as e:
            print("Cannot find address: " + address)
            the_file.write(address + 'KEY ERROR \n')