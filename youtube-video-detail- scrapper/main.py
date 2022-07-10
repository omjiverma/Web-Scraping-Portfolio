#Scapping youtube videos basic details
from pytube import YouTube

def yt_scraper(link):
    detail={}
    yt = YouTube(link)
    detail ={
        'title':yt.title,
        'views': yt.views,
        'length': yt.length,
        'description': yt.description.replace('\n',' '),
        'rating': yt.rating,
        'age_restricted': yt.age_restricted,
        'thumbnail_url': yt.thumbnail_url,
    }
    
    return detail
if __name__ == "__main__":
    #Run this file
    link =input('Enter yt Video url : ')
    data = yt_scraper(link)
    print(data)
else:
    pass
    #Else run where imported

