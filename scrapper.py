import pandas as pd
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

warnings.filterwarnings('ignore')

YOUTUBE_LINK = 'https://www.youtube.com/feed/trending?bp=4gIKGgh0cmFpbGVycw%3D%3D'


def getDriver():
    chromeOptions = Options()
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chromeOptions)
    return driver


def getVideo(driver):
    VIDEO_DIV_TAG = 'ytd-video-renderer'
    driver.get(YOUTUBE_LINK)
    videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
    return videos


def parseVideo(video):
    # Title
    titleTag = video.find_element(By.ID, 'video-title')
    title = titleTag.text

    # URL
    url = titleTag.get_attribute('href')

    # Channel Name
    channelTag = video.find_element(By.CLASS_NAME, "ytd-channel-name")
    channel = channelTag.text

    # Thumbnail url
    thumbnailurlTag = video.find_element_by_tag_name('img')
    thumbnailUrl = thumbnailurlTag.get_attribute('src')

    # Description
    descriptionTag = video.find_element(By.ID, 'description-text')
    description = descriptionTag.text

    return {
        'Title': title,
        'Channel': channel,
        'URL': url,
        'Thumbnail URL': thumbnailUrl,
        'Description': description
    }


if __name__ == '__main__':
    print('Creating Driver...')
    driver = getDriver()

    print('Fetching the Page...')
    videos = getVideo(driver)

    print('Parsing Top 10 Trending Videos')
    videoData = [parseVideo(video) for video in videos[:10]]

    print(videoData[7])

    print("Saving video Datas in CSV file")

    videoDf = pd.DataFrame(videoData)
    videoDf.to_csv('trending.csv', index=False)
