print("Content-type: text/html")
print()

import cgi
import requests
from bs4 import BeautifulSoup
import json
import urllib

form = cgi.FieldStorage(keep_blank_values=1)
place =  form.getvalue('place')
minprice =  form.getvalue('minprice')
maxprice =  form.getvalue('maxprice')
minbeds =  form.getvalue('minbeds')

print("Location entered: " + place)
print("<html>")
print("<head>")
print("<title>House Prices</title>")
print("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
print("<link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css\" integrity=\"sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7\" crossorigin=\"anonymous\">")
print("</head>")
print("<body>")

try:
    r = urllib.request.urlopen("http://api.zoopla.co.uk/api/v1/property_listings.json?area=%s&minimum_price=%s&maximum_price=%s&minimum_beds=%s&api_key=rwf84fjeak4k5vmfknd9h8j9" % (place, minprice, maxprice, minbeds))
except urllib.error.HTTPError as error:
    print("<h2>Not a location! please go back and enter another location</h2>")

data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
#print(data)

for item in data.get('listing'):
    print('')
    t = urllib.request.urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&radius=500&type=school&key=AIzaSyD8Y44_crpsPfHudm2vSb4EjQrIevxOvtM" % (item.get('latitude'), item.get('longitude')))
    data2 = json.loads(t.read().decode(t.info().get_param('charset') or 'utf-8'))
    print("<div class=\"container-fluid\">")
    print("<div class=\"row\">")
    print("<hr>")
    if item.get('num_bedrooms') == "0":
        print("<h3>Exciting Opportunity</h3>")
    else:
        print("<h3>%s Bedroom Home </h3>" % item.get('num_bedrooms'))
    if item.get('price') == 0:
        print("<p>Price: TBC</p>")
    else:
        print("<p>Price: %s</p>" % item.get('price'))
    print("<div class=\"col-md-4\">")
    print("<img src=\"%s\"/ class=\"img-responsive\">" % item.get('image_url'))
    print("</div>")
    print("<div class=\"col-md-8\">")
    print("<p>House type: %s</p>" % item.get('property_type'))
    print("<p>Address: %s</p>" % item.get('displayable_address'))
    print("<p>Description: %s</p>" % item.get('description'))
    print("<a href=\"https://maps.google.com/?q=%s,%s\">Click here to see the area</a>" % (item.get('latitude'), item.get('longitude')))
    print('<br>')
    print('<br>')
    print("Schools nearby:")
    print('')
    for item in data2.get('results'):
        print(item.get('name') + ", ")
    print("</div>")
    print("</div>")
    print("</div>")
print("</body>")
print("</html>")
