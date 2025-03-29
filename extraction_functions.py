# import neccesary packages
from bs4 import BeautifulSoup
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import time
#import random 

# Fuction iterates through a page_charts page and extracts all the album links
def get_links(page,data):

	driver = Driver(uc=True,incognito=True)
	driver.uc_open_with_reconnect(page, 10)
	driver.uc_gui_click_captcha()

	#wait until page loads to extract information
	try:
		element = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID,'page_charts')))
	finally:
		# use BeautifulSoup to extract all links in page
		pageSource = driver.page_source
		bs = BeautifulSoup(pageSource, 'html.parser')
		hrefs = bs.find_all("a",{"class":"page_charts_section_charts_item_link release"})

		# append links to the total list of links
		for href in hrefs:
			data.append(href['href'])

	# close and quit driver
	driver.quit()

# Function extracts info from album page
def extract_info(link,data):

	driver = Driver(uc=True,incognito=True)
	driver.uc_open_with_reconnect(link, 10)
	driver.uc_gui_click_captcha()

	# wait until page loads to extract information
	try:
		element = WebDriverWait(driver, 400).until(EC.presence_of_element_located((By.ID,'page_release')))
	finally:
		# Turn page source into BeautifulSoup Object
		pageSource = driver.page_source
		bs = BeautifulSoup(pageSource, 'html.parser')

		# Attempt to extract variables from album page
		try:
			album_title = bs.find('div',{'class':'album_title'}).get_text().split('\n', 1)[0].strip()
			artist_name = bs.find('a',{'class':'artist'}).get_text().strip()
			average_rating = float(bs.find('span',{'class':'avg_rating'}).get_text().strip())
			number_of_ratings = bs.find('span',{'class':'num_ratings'}).b.get_text().strip()
			genres = list(bs.find('tr',{'class':'release_genres'}).td.get_text().strip().replace("\n",", ").split(","))
			descriptors = list(bs.find('tr',{'class':'release_descriptors'}).td.get_text().strip().split(","))

			# For language if no language exist label it as none
			try:
				language = bs.find('td',{'style':'font-size:0.9em;color:var(--mono-5);'}).get_text().strip()
			except:
				language = "None"

			# I think there are cases when the full date is not avaliable only the year so this is what this is supposed to catch
			try:
				date = int(bs.find('a',{'style':'text-decoration:none;'}).get_text())
			except:
				date = int(bs.find_all('td',{'colspan':'2'})[2].get_text()[-4:])

			# Append entry into list
			data.append([album_title, artist_name, date, average_rating, number_of_ratings, genres, descriptors, language])
		except:
			# If fails take a screenshot 
			print("Something went wrong. Look at screenshot")
			driver.save_screenshot("error.png")

		# print(album_title)

	# close and quit driver
	driver.quit()