import csv

import requests
from bs4 import BeautifulSoup


class Test1(urls=[]):
	url = "https://www.cisco.com"

	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	product_information = []
	for rows in soup.find_all("tr"):
		if ("oddrow" in rows["class"]) or ("evenrow" in rows["class"]):
			vendor = rows.find("div", class_="name")
			url = rows.find("div", class_="name")
			series = rows.find("div", class_="name")
			category = rows.find("div", class_="name")
			model = rows.find("div", class_="name")
			path = rows.find("div", class_="name")
			release = rows.find("div", class_="name")
			endofsale = rows.find("div", class_="name")
			endofsupport = rows.find("div", class_="name")
			downloads = [{
				'lastest: ' + rows.find("div", class_="name"),
				'filename:' + rows.find("div", class_="name"),
				'size:' + rows.find("div", class_="name"),
				'md5:' + rows.find("div", class_="name"),
			}]
			product_information.append(
				[vendor, url, series, category, model, path, release, endofsale, endofsupport, downloads])

	with open("cisco_products.csv", 'a', encoding='utf-8') as toWrite:
		writer = csv.writer(toWrite)
		writer.writerows(product_information)
	print("Cisco Products Information")


if __name__ == '__main__':
	Test1(urls=['https://www.cisco.com/']).run()
