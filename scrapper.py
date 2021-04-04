import requests
from bs4 import BeautifulSoup
from clint.textui import progress

'''
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
'''

# specify the URL of the archive here
archive_url = "https://dl1.zoopix.ir/Series/Office/S01/"

base_url = "https://dl1.zoopix.ir"

# incase downloaded some episodes and now re runing the program
downloaded = ["E01", "E02", "E03"]

def get_video_links():
    
    # create response object
    r = requests.get(archive_url)
    
    # create beautiful-soup object
    soup = BeautifulSoup(r.content,'html5lib')
    
    # find all links on web-page
    links = soup.findAll('a')

    # filter the link sending with .mp4
    video_links = [base_url + link['href'] for link in links if link['href'].endswith('mkv') and not any(x in link['href'] for x in downloaded)]

    return video_links


def download_video_series(video_links):

    for link in video_links:
        # print(link)
        '''iterate through all links in video_links and download them one by one'''
    
        # obtain filename by splitting url and getting
        # last string
        file_name = link.split('/')[-1]

        print( "Downloading file:%s"%file_name)
        
        # create response object
        r = requests.get(link, stream = True)
        
        # download started
        with open("theOffice/S01/" + file_name, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            # for chunk in r.iter_content(chunk_size = 1024*1024):
            #     if chunk:
            #         f.write(chunk)
            for chunk in progress.bar(r.iter_content(chunk_size=1024*1024), expected_size=(total_length/(1024*1024)) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        
        print( "%s downloaded!\n"%file_name )

    print ("All videos downloaded!")
    return


if __name__ == "__main__":

    # getting all video links
    video_links = get_video_links()

    # download all videos
    download_video_series(video_links)
    

    
