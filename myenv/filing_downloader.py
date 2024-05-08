from sec_api import QueryApi, RenderApi, FullTextSearchApi
from constants import API_KEY
from sec_api import QueryApi

renderApi = RenderApi(api_key=API_KEY)
queryApi = QueryApi(api_key=API_KEY)
filterApi = FullTextSearchApi(api_key=API_KEY)

# base_query = {
#   "query": { 
#       "query_string": { 
#           "query": "PLACEHOLDER", # this will be set during runtime 
#           "time_zone": "America/New_York"
#       } 
#   },
#   "from": "0",
#   "size": "200", # dont change this
#   # sort returned filings by the filedAt key/value
#   "sort": [{ "filedAt": { "order": "desc" } }]
# }

filterVariables = "cybersecurity"

base_query = {
    "query": filterVariables,
    "formTypes": ["10-K", "10-KT", "10KSB"],
    "startDate": "2001-01-01", # Gets all filings from 2001 
    "endDate": "2022-12-31", # Until the end of 2022
    "page": 0
}


# open the file we use to store the filing URLs
log_file = open("filing_urls.txt", "a")

for page in range(0, 9900, 100): # Query API returns a max of 100 fillings per search
    # set new "from" starting position of search 
    base_query["page"] = page;

    # gets the filings from the Api
    response = filterApi.get_filings(base_query)

    # no more filings in search universe
    if len(response["filings"]) == 0:
        break;

    # for each filing, only save the URL pointing to the filing itself 
    # and ignore all other data. 
    # the URL is set in the dict key "linkToFilingDetails"
    urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))

    # transform list of URLs into one string by joining all list elements
    # and add a new-line character between each element.
    urls_string = "\n".join(urls_list) + "\n"
    
    log_file.write(urls_string)

log_file.close()

print("All URLs downloaded")

# download filing and save to "filings" folder
def download_filing(url):
  try:
    filing = renderApi.get_filing(url)
    # file_name example: 000156459019027952-msft-10k_20190630.htm
    file_name = url.split("/")[-2] + "-" + url.split("/")[-1] 
    download_to = "./filings/" + file_name
    with open(download_to, "w") as f:
      f.write(filing)
  except Exception as e:
    print("Problem with {url}".format(url=url))
    print(e)
    
# load URLs from log file
def load_urls():
  log_file = open("filing_urls.txt", "r")
  urls = log_file.read().split("\n") # convert long string of URLs into a list 
  log_file.close()
  return urls

import os
import multiprocessing

def download_all_filings():
  print("Start downloading all filings")

  download_folder = "./filings" 
  if not os.path.isdir(download_folder):
    os.makedirs(download_folder)
    
  urls = load_urls()
#   urls = load_urls()[1:40]
  print("{length} filing URLs loaded".format(length=len(urls)))

  number_of_processes = 20

  with multiprocessing.Pool(number_of_processes) as pool:
    pool.map(download_filing, urls)
  
  print("All filings downloaded")
  
# download_all_filings()
  
