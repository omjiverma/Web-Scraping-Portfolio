# By Omji Verma
# omjidvlpr@gmail.com
# github.com/omjiverma
# Trustpilot review scrapper
# Date :16/05/2022

from bs4 import BeautifulSoup
from hamcrest import none
import requests
import json
from urllib.error import HTTPError
hdr = {'User-Agent': 'Mozilla/5.0'}

URL='https://www.trustpilot.com'



class Crawler:
  data = {'User Country':[],'Review Title':[],'Review Description':[]}
  def __init__(self,site):
    """
    Args:
        url (_type_): full url of website to be scrapped. Example: avada.io
    """
    self.site = site
  def getpage(self,absolute_url=''):
    page_link=URL+'/review/'+self.site+absolute_url
    print(page_link)
    try:
      content_html = requests.get(page_link,headers=hdr).text
      bs=BeautifulSoup(content_html,'html.parser')
      return bs
    except HTTPError as e:
      print('Some Error occured')
      return None
  
  def detail(self):
    """
    This function gives the basic detail of company.
    """
    soup = self.getpage()
    company_name = soup.find_all('span',{'class':'typography_h1__Xmcta'})[0].get_text()
    total_reviews = soup.find(class_='styles_text__W4hWi').get_text()
    category = soup.find(class_='styles_mobileBreadcrumbLink__SmgGk').get_text()
    print(f'Company Name : {company_name} \nCategory : {category} \nReviews and Ratings : {total_reviews}')

  def show(self):
    """
    function to show scraped reviews
    """
    print(self.data)
  def reviews(self):
    """
    Function for crawling all reviewsCrawling All Reviews 
    """
    soup = self.getpage()
    blocks = soup.find_all(class_='styles_reviewCard__hcAvl')
    for block in blocks:
      reviewer_country = block.find_all('span',{'class':'typography_weight-inherit__iX6Fc'})[1].get_text()
      review_title = block.h2.get_text()
      if block.p is not None:
        review_description = block.p.get_text() 
      else:
        review_description = ''  
      self.data['User Country'].append(reviewer_country)
      self.data['Review Title'].append(review_title)
      self.data['Review Description'].append(review_description)
    
    next_page = soup.find('a',{'name':'pagination-button-next'})['href']
    next_page = '?'+next_page.split('?')[1]
    while next_page:
      print('Crawling Reviews')
      soup = self.getpage(next_page)
      blocks = soup.find_all(class_='styles_reviewCard__hcAvl')
      for block in blocks:
        reviewer_country = block.find_all('span',{'class':'typography_weight-inherit__iX6Fc'})[1].get_text()
        review_title = block.h2.get_text()
        if block.p is not None:
          review_description = block.p.get_text() 
        else:
          review_description = ''  
        self.data['User Country'].append(reviewer_country)
        self.data['Review Title'].append(review_title)
        self.data['Review Description'].append(review_description)
      try:
        next_page = soup.find('a',{'name':'pagination-button-next'})['href']
        next_page = '?'+next_page.split('?')[1]
         
      except:
        print('Done')
        break
      self.show()  

  def export(self,filename):
    """
    function to export reviews to json file

    Args:
        filename (_str_): name of file for exporting to json
    """
    with open(f"{filename}", "w") as outfile:
      json.dump(self.data, outfile)
      print(f'File exported to {filename}')




crawl = Crawler('castleglenwine.com')
crawl.reviews()
crawl.export('out.json')