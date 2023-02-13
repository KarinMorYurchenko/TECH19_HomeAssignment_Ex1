import json
import datetime
import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from datetime import datetime

cisco_url = "https://cisco.com"
ex_url = "https://www.cisco.com/c/en/us/support/routers/910-industrial-router/model.html"


def log_in(user_name, password):
	driver = webdriver.Chrome()
	driver.get(cisco_url)
	driver.maximize_window()
	email_box_element = find_element_and_click(
		driver, 'fw-c-header__button--login--desktop', 'userInput'
	)
	email_box_element.click()
	email_box_element.send_keys(user_name)
	password_box_element = find_element_and_click(
		driver, 'login-button', 'okta-signin-password'
	)
	password_box_element.send_keys(password)
	login_button_element = driver.find_element(By.ID, 'okta-signin-submit')
	login_button_element.click()


def find_element_and_click(driver, arg1, arg2):
	button_element = driver.find_element(By.ID, arg1)
	button_element.click()
	return driver.find_element(By.ID, arg2)


def product_info(union_products_link):
	for product_link in union_products_link:
		url_product = get_product_url(product_link)
		product_name = get_products_names(url_product)
		product_category = get_product_category(url_product)
		product_series = get_products_series(url_product)
		product_path = get_products_path(url_product, product_name)
		release_date = get_product_release_date(url_product)
		eosale_date = get_product_end_of_sale_date(url_product)
		eosupport_date = get_product_end_of_support_date(url_product)
		# downloads_lastes = get_downloads_info(url_product)
		product_info_output = {'vendor': cisco_url,
							   'url': url_product,
							   'series': product_series,
							   'cagetory': product_category,
							   'model': product_name,
							   'path': product_path,
							   'release': release_date,
							   'endofsale': eosale_date,
							   'endofsupport': eosupport_date
							   # 'downloads': [{downloads_lastes}]
							   }
		print(json.dumps(product_info_output, indent=4, default=str))


def get_product_url(product_link):
	return f"https://www.cisco.com{product_link}"


def get_downloads_info(product_link):
	product_url = requests.get(product_link)
	download_soup = BeautifulSoup(product_url.text, 'html.parser')
	dd_list_in_table = download_soup.find(class_="expand_row_cell").find_all('dd')
	ver_num = dd_list_in_table[1]
	file_name = dd_list_in_table[3]
	size = dd_list_in_table[4]
	md5 = download_soup.find(class_="md5ChecksumText")
	all_releases_url = download_soup.find(class_="download-all-releases").get('href')

	return [
		{'latest': ver_num, 'filename': file_name, 'size': size, 'md5': md5},
		{
			'all': all_releases_url,
		},
	]


def get_products_names(product_link):
	product_name_respond = requests.get(product_link)
	product_name_soup = BeautifulSoup(product_name_respond.text, 'html.parser')
	return product_name_soup.find(id="fw-pagetitle").text


def check_what_kind_of_dates_product_has(product_link):
	product_name_respond = requests.get(product_link)
	product_name_soup = BeautifulSoup(product_name_respond.text, 'html.parser')
	if "Release" in product_name_soup.find_all('tr')[4].text:
		return get_product_release_date(product_link)
	if "end" in product_name_soup.find_all('tr')[4].text:
		return get_product_end_of_sale_date(product_link)
	if "end" in product_name_soup.find_all('tr')[4].text:
		return get_product_end_of_support_date(product_link)


def get_product_end_of_sale_date(product_link):
	product_name_respond = requests.get(product_link)
	product_name_soup = BeautifulSoup(product_name_respond.text, 'html.parser')
	all_th_list = product_name_soup.find_all('th')
	th = '<th>End-of-Sale Date</th>'
	if th not in str(all_th_list):
		return ""
	list_of_trs = product_name_soup.find_all('tr')
	for tr in list_of_trs:
		if th in str(tr):
			date_format = "%d-%b-%Y"
			match = re.search(r'\d{2}-[A-Z]{3}-\d{4}', str(tr))
			match_string = match.group()
			date = datetime.strptime(match_string, date_format)
			return convert_date_to_unix(date)


def get_product_end_of_support_date(product_link):
	product_name_respond = requests.get(product_link)
	product_name_soup = BeautifulSoup(product_name_respond.text, 'html.parser')
	all_th_list = product_name_soup.find_all('th')
	th = '<th>End-of-Support Date</th>'
	if "End-of-Support" not in str(all_th_list):
		return ""
	list_of_trs = product_name_soup.find_all('tr')
	for tr in list_of_trs:
		if th in str(tr):
			date_format = "%d-%b-%Y"
			match = re.search(r'\d{2}-[A-Z]{3}-\d{4}', str(tr))
			match_string = match.group()
			date = datetime.strptime(match_string, date_format)
			return convert_date_to_unix(date)


def get_product_release_date(product_link):
	product_name_respond = requests.get(product_link)
	product_name_soup = BeautifulSoup(product_name_respond.text, 'html.parser')
	all_th_list = product_name_soup.find_all('th')
	th = '<th>Series Release Date</th>'
	th2 = 'Release Date'
	if "Release Date" not in str(all_th_list):
		return ""
	list_of_trs = product_name_soup.find_all('tr')
	for tr in list_of_trs:
		tr_str = str(tr).replace(' ', '')
		if th.replace(' ', '') in str(tr_str) or th2.replace(' ', '') in str(tr_str):
			date_format = "%d-%b-%Y"
			match = re.search(r'\d{2}-[A-Z]{3}-\d{4}', str(tr))
			match_string = match.group()
			date = datetime.strptime(match_string, date_format)
			return convert_date_to_unix(date)


def convert_date_to_unix(date):
	return int((time.mktime(date.timetuple())))


def get_products_series(product_link):
	product_url = requests.get(product_link)
	bs = BeautifulSoup(product_url.text, 'html.parser')
	return bs.find(id="fw-pagetitle").text


def get_product_category(product_link):
	product_url = requests.get(product_link)
	category_soup = BeautifulSoup(product_url.text, 'html.parser')
	return category_soup.find_all("span")[5].text


def get_products_path(product_link, product_name):
	product_url = requests.get(product_link)
	products_soup = BeautifulSoup(product_url.text, 'html.parser')
	path_soup = products_soup.find_all('ul')[2].text.replace('\n', '').replace(' ', '/'). \
		replace('P', '/P').replace('S', '/S').replace('//', '/')
	path2 = "".join(path_soup)
	return f"{path_soup}/{product_name}"


def union_all_products_links_from_all_categories(category_links):
	union_product_links = []
	for category_link in category_links:
		link_respond = requests.get(category_link)
		category_soup = BeautifulSoup(link_respond.text, 'html.parser')
		product_links_by_number_list = category_soup.find(id="prodByNumber").find_all('a')
		for product_link in product_links_by_number_list:
			product_link_by_number = product_link.get('href')
			if "/3g-small-cell/" or "/univeral-small-cell-7000-series/" in str(product_link_by_number):
				continue
			union_product_links.append(product_link_by_number)
		product_by_alpha_limks_list = category_soup.find(id="prodByAlpha").find_all('a')
		for product_link in product_by_alpha_limks_list:
			product_link_by_alpha = product_link.get('href')
			if "/duo/" in str(product_link_by_alpha):
				continue
			union_product_links.append(product_link_by_alpha)
		product_end_of_support_links_list = category_soup.find(id="eolanchor").find_all('a')
		for product_link in product_end_of_support_links_list:
			product_end_of_support_link = product_link.get('href')
			union_product_links.append(product_end_of_support_link)
	return union_product_links


def get_all_product_links():
	all_products = "https://www.cisco.com/c/en/us/support/all-products.html"
	all_product_links = []
	all_products_support_respond = requests.get(all_products)
	all_products_soup = BeautifulSoup(all_products_support_respond.text, 'html.parser')
	top_product_categories = all_products_soup.find(id="top-categories").find_all('li')
	for top_product_link in top_product_categories:
		top_url = str(top_product_link.find('a').get('href')).replace('//', 'https://')
		all_product_links.append(top_url)

	return all_product_links


# log_in('karinayurchenko@gmail.com', 'tq5vtNdw!')
product_info(union_all_products_links_from_all_categories(get_all_product_links()))
