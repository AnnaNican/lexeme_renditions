
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re





def get_book_list():
	'''get book list available from archives
	# there is infinite scroll on the page, so use this to load more: https://www.accordbox.com/blog/how-crawl-infinite-scrolling-pages-using-python/ 
	 '''
	global alldata
	npages = 3
	alldata = pd.DataFrame(columns=[])

	for pagenum in range(1,npages):
		url = "https://archive.org/details/guggenheimmuseum?and%5B%5D=mediatype%3A%22texts%22&sort=titleSorter&page=" + str(pagenum)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		books = soup.find_all("div", {"class": "item-ia"})
		data = pd.DataFrame(columns=[])
		data['html'] = books
		alldata = alldata.append(data)



def clean_book_list():
	''' clean up data and extract correct fields'''
	for rownum, row in alldata.iterrows():
		try:
			year = re.findall(r'year="([^"]*)', str(row['html']))[0]
			print(year)
			alldata.loc[rownum, 'year']= year
			title = re.findall(r'title="([^"]*)', str(row['html']))[0]
			alldata.loc[rownum, 'title']= title
			book_img = re.findall(r'"item-img " source="([^"]*)', str(row['html']))[0]
			alldata.loc[rownum, 'book_img']= book_img
			alldata.loc[rownum, 'creator'] = re.findall(r'class="byv" title="([^"]*)', str(row['html']))[0]
			url = re.findall(r'href="([^"]*)', str(row['html']))[1]
			alldata.loc[rownum, 'book_url'] = re.findall(r'href="([^"]*)', str(row['html']))[1]
			bookurn = re.findall(r'\/details\/([^"]*)', url)[0]
			alldata.loc[rownum, 'book_urn'] = bookurn
			alldata.loc[rownum, 'book_text'] = 'https://archive.org/stream/'+ bookurn + '/' + bookurn + '_djvu.txt'
		except:
			next
		
	alldata.to_csv('../data/book_list.csv', index=False)


def download_books():
	'''download books into text docs '''
	for rownum, row in alldata.iterrows():
		print(row['book_text'])
		try:
			rawtext = requests.get(row['book_text'])
			souptext = BeautifulSoup(rawtext.text, 'html.parser')
			filename = "../data/books/" + row['book_urn'] + ".txt"
			file = open(filename, "w") 
		 	file.write(str(souptext)) 
			file.close() 
		except:
			next

if __name__ == '__main__':
	get_book_list()
	clean_book_list()
	download_books()
	print('all books downloaded into repo')




