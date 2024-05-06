from sec_api import QueryApi, RenderApi
from constants import API_KEY
from sec_api import QueryApi

renderApi = RenderApi(api_key=API_KEY)
queryApi = QueryApi(api_key=API_KEY)

base_query = {
  "query": { 
      "query_string": { 
          "query": "PLACEHOLDER", # this will be set during runtime 
          "time_zone": "America/New_York"
      } 
  },
  "from": "0",
  "size": "200", # dont change this
  # sort returned filings by the filedAt key/value
  "sort": [{ "filedAt": { "order": "desc" } }]
}

# open the file we use to store the filing URLs
log_file = open("filing_urls.txt", "a")

# start with filings filed in 2022, then 2020, 2019, ... up to 1995
# uncomment next line to fetch all filings filed from 2022-1995
# for year in range(2021, 1994, -1):
for year in range(2022, 2020, -1):
  print("Starting download for year {year}".format(year=year))
  
  # a single search universe is represented as a month of the given year
  for month in range(1, 13, 1):
    # get 10-Q and 10-Q/A filings filed in year and month
    # resulting query example: "formType:\"10-Q\" AND filedAt:[2021-01-01 TO 2021-01-31]"
    universe_query = \
        "formType:(\"10-K\", \"10-KT\", \"10KSB\", \"10KT405\", \"10KSB40\", \"10-K405\") AND " + \
        "filedAt:[{year}-{month:02d}-01 TO {year}-{month:02d}-31]" \
        .format(year=year, month=month)
  
    # set new query universe for year-month combination
    base_query["query"]["query_string"]["query"] = universe_query;

    # paginate through results by increasing "from" parameter 
    # until we don't find any matches anymore
    # uncomment next line to fetch all 10,000 filings
    # for from_batch in range(0, 9800, 200): 
    for from_batch in range(0, 400, 200):
      # set new "from" starting position of search 
      base_query["from"] = from_batch;

      response = queryApi.get_filings(base_query)

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

    print("Filing URLs downloaded for {year}-{month:02d}".format(year=year, month=month))

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
    
  # uncomment next line to process all URLs
  urls = load_urls()
  urls = load_urls()[1:40]
  print("{length} filing URLs loaded".format(length=len(urls)))

  number_of_processes = 20

  with multiprocessing.Pool(number_of_processes) as pool:
    pool.map(download_filing, urls)
  
  print("All filings downloaded")
  
download_all_filings()
  
