from selenium import webdriver
from selenium.webdriver.common.by import By

website = "https://www.cisco.com/c/en/us/support/routers/910-industrial-router/model.html"
driver = webdriver.Chrome()
driver.get(website)

product_table_info = driver.find_element(By.CSS_SELECTOR, 'table > tbody')
table_rows = product_table_info.find_elements(By.TAG_NAME, 'tr')
table_headers = product_table_info.find_elements(By.TAG_NAME, 'th')
# table_data = product_table_info.find_elements(By.TAG_NAME, 'td')

series = []
category = "Routers"
model = []
product_info = []
release = []
endofsale = []
endofsupport = []

series.append(
	(driver.find_element(By.XPATH, '//*[@id="fw-content"]/div[2]/div/div/div[1]/table/tbody/tr[1]/td/a').text))
model.append(driver.find_element(By.XPATH, '//*[@id="fw-pagetitle"]').text)
release.append(driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(4) > td').text)
endofsale.append(driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(5) > td').text)
endofsupport.append(driver.find_element(By.CSS_SELECTOR, 'tr:nth-child(6) > td').text)

dict = {
	'series': series,
	'category': category,
	'model': model,
	'release': release,
	'end of sale': endofsale,
	'end of support': endofsupport}

for keys, values in dict.items():
	for value in dict.values():
		print(value)
