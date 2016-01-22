import requests
from bs4 import BeautifulSoup, SoupStrainer

#boat maker/model, seller contact number, price

def getRawHtml(url):
    search_link = url
    r = requests.get(search_link)
    return r.text

page = 1
end_page = 4981 # number of total pages
count_per_page = 28 # not necessary, but notable as default count per page

boats = {} #key = boat_id, value = list[make/model, contact number, price]

while page <= end_page:
	raw_html = getRawHtml("http://www.boattrader.com/search-results/NewOrUsed-any/Type-any/Category-all/Zip-07054/Radius-4000/Sort-Length:DESC/Page-%s,28?" % page)
	soup = BeautifulSoup(raw_html, "html.parser")
	listings = soup.find_all('section', {'class': 'boat-listings'})

	for boat in listings[0].find_all('li'):
		if 'data-reporting-impression-product-id' not in boat.attrs: # skip if li element does not have an id
			pass
		else:
			id_num = boat['data-reporting-impression-product-id'].encode('utf-8')

			if id_num not in boats: # add to dictionary if id was not already added
				links = boat.find_all('a', href = True)
				if len(links) != 0:
					link = links[0]
					url = 'http:' + link['href'].encode('utf-8')
					boat_html = getRawHtml(url)
					boat_soup = BeautifulSoup(boat_html, "html.parser")

					#for each attribute, check to see if it exists for the listing
					#if it is unavailable, assign 'n/a'
					price = boat_soup.find_all('span', {'class': 'bd-price contact-toggle'})
					if len(price) != 0:
						price = price[0].text.encode('utf-8')
					else:
						price = 'n/a'

					make = boat_soup.find_all('span', {'class': 'bd-make'})
					if len(make) != 0:
						make = make[0].text.encode('utf-8')
					else:
						make = 'n/a'

					model = boat_soup.find_all('span', {'class': 'bd-model'})
					if len(model) != 0:
						model = model[0].text.encode('utf-8')
					else:
						model = 'n/a'

					phone_num = boat_soup.find_all('a', {'class': 'call-btn mobile'})
					if len(phone_num) != 0:
						phone_num = phone_num[0]['href'].encode('utf-8')
					else:
						phone_num = 'n/a'

					#assign values to boats dictionary for each key id
					boats[id_num] = [make, model, phone_num, price]
					print boats[id_num]

	print 'page %s done' % page
	page += 1 # go to next page
