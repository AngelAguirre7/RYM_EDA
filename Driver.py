# Import function file
import extraction_functions as ef

# Import Packages
import pandas as pd
import time
import csv
import random

def rym_extraction():
	# Record time program spent to run
	start_time = time.time()

	# Starting Link
	page = 'https://rateyourmusic.com/charts/top/album/all-time/separate:live/' # Note: Im excluding live releases

	# Start Arrays which later will get converted to csv
	links = []
	data = [['Album_Title','Artist_Name','Year of Release','Average_Rating','Number_Of_Ratings','Genres','Descriptors','Language']]

	# Get links from first chart page
	ef.get_links(page,links)

	'''
	Iterate through chart pages until reaching 1000th 
	album applying get_links function to get the album page link
	'''
	for x in range(2,26):
		# Brief pause between 7 and 15 seconds
		time.sleep(random.uniform(7,16))
		# Apply get_links to get all links in a chart page
		ef.get_links(page+str(x)+'/',links)
		
		
	#print(len(links))
	'''
	iterate through album links
	extracting information from each page
	'''
	for link in links:
		# apply extract_info to extract specified variables from album page
		ef.extract_info('https://rateyourmusic.com'+link,data)
		# Brief pause between 30 and 60 seconds
		time.sleep(random.uniform(30,60))
		print(link)

	# Convert Array into appropriate dataframe and export as csv

	df_albums = pd.DataFrame(data)

	df_albums.columns = df_albums.iloc[0]
	df_albums = df_albums[1:]

	df_albums.to_csv('Top_1000_RYM_Albums_03012025.csv')

	print("The program took", time.time() - start_time, "to run")

if __name__ == '__main__':
	rym_extraction()

