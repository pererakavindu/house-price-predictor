import geopy
geocoder=geopy.Nominatim(user_agent='kavi')
import requests
from bs4 import BeautifulSoup
file_path = "/content/drive/MyDrive/example.txt"
fp=open(file_path, 'w')
for i in range(100):
  url=f'https://ikman.lk/en/ads/colombo/houses-for-sale?page={i}'
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
  }

  # Send a GET request to the website
  response = requests.get(url, headers=headers)
  # Check if the request was successful
  if response.status_code == 200:
      print("Successfully fetched the page.")
  else:
      print(f"Failed to fetch the page. Status code: {response.status_code}")
      continue
  soup = BeautifulSoup(response.content, 'html.parser')
  listing=soup.findAll('a',class_='gtm-ad-item')
  webpages=[]
  for ad in listing:
    webpages.append('https://ikman.lk'+ad.get('href'))
  for ad in webpages:
    scraped={
        'Price:':0,
        'Address:':0,
        'Bedrooms:':0,
        'Bathrooms:':0,
        'House size:':0,
        'Land size:':0,
        'Long:':0,
        'Lat:':0
    }
    try:
      url=ad
      response = requests.get(url, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')
      tags=soup.findAll('div',class_='word-break--2nyVq')
      data=[]
      for tag in tags:
        data.append(tag.text.strip())
      scraped['Price:']=soup.find('div',class_='amount--3NTpl').text
      for info in scraped.keys():
        if info=='Price:':
          continue
        if info in data:
          scraped[info]=data[data.index(info)+1]
      try:
        print('default address')
        if scraped['Address:']==0:
          raise ValueError('address not found')
        scraped['lat:']=geopy.Nominatim(user_agent='kavi').geocode(scraped['Address:']).latitude
        scraped['long:']=geopy.Nominatim(user_agent='kavi').geocode(scraped['Address:']).longitude
      except:
        print('secondary address')
        addr_tags=soup.findAll('a',class_='subtitle-location-link--1q5zA')
        scraped['Address:']=addr_tags[0].text+addr_tags[1].text
        scraped['lat:']=geocoder.geocode(scraped['Address:']).latitude
        scraped['long:']=geocoder.geocode(scraped['Address:']).longitude
      scraped['Price:']=scraped['Price:'].replace('Rs','')
      scraped['Price:']=scraped['Price:'].replace(',','')
      print(scraped)
      fp.write(f"{scraped['Price:']},{scraped['lat:']},{scraped['long:']},{scraped['Bathrooms:']},{scraped['Bedrooms:']},{scraped['House size:']},{scraped['Land size:']}\n")
    except:
      pass
