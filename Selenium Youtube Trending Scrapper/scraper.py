from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_URL='https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  driver.get(YOUTUBE_URL)
  VIDEO_DIV_CLASS = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_CLASS)
  return videos

def parse_video(video):
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text

  url = title_tag.get_attribute('href')

  img_tag = video.find_element(By.TAG_NAME,'img')

  thumbnail_url = img_tag.get_attribute('src')

  channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel_name = channel_div.text

  description = video.find_element(By.ID, 'description-text').text

  return {
    'title': title,
    'url': url,
    'thumbnail_url':thumbnail_url,
    'channel': channel_name,
    'description': description
  }

if __name__ == "__main__":
  print('Creating Driver')
  driver = get_driver()
  print('fetching Trending Videos')
  videos = get_videos(driver)

  print(f'found {len(videos)} videos')

  print('Getting Top 10 Videos')

  videos_data = [parse_video(video) for video in videos[:10]]

  print('Saving data to csv')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv')
