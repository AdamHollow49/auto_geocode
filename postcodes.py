import requests
import time
import json
import csv

api_key = 'pk.d8a3afc49f5f76f0e7287c9d86f474ac'   # Public API Key
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
    with open('addresses.txt') as read_file:    # open user address list (csv)
        csv_reader = csv.reader(read_file, delimiter=",")
        for row in csv_reader:    # for each list
            print("Imported: ", row)    # notify import
            adlist.append(row)    # add to list to run through api
url = "http://eu1.locationiq.com/v1/search.php"   # api url
with open('addresses_info.txt', 'a') as the_file:   # open file to write, save changes, if it doesn't exist create it
    for x in adlist:    # run through list of previously acquired addresses
        v = ''    # var to merge components of sub arrays
        for s in range(len(x)):   # for each sublist item, if not blank append to v
            if x[s] != '':
                v += x[s]
        time.sleep(0.5)   # space API requests out
        try:    # make get request
            address = v
            requesturl = url + "?key=" + api_key + "&q=" + address + "&format=JSON"
            response = requests.get(requesturl).json()
            for x in range(len(response)):    # break JSON down to dictionary, for each entry
                if response[x]['display_name'].find(criteria) > 0:    # if there is a display name in entry
                    final = response[x]['display_name']   # assign var final value of this display name
                    print(final)
                    the_file.write(final)   # write display name to file
                else:   # if there is no display name entry
                    final = "ADDRESS FOUND BUT NOT IN {} AREA".format(criteria)
                    the_file.write(final + " " + response[x]['display_name'])   # advise no address in location area
        except ValueError as e:   # catch errors for value
            print(e, " ValueError, " + address)
            the_file.write(address + "VALUE ERROR \n")
        except KeyError as e:   # catch errors for key errors
            print("Cannot find address: " + address)
            the_file.write(address + 'KEY ERROR \n')
