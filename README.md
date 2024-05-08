# SEC-Web-Scrapper
A Python Web Scrapper to get fillings from the SEC easily

## SEC Api
- The QueryApi is a search interface allowing us to seach and find SEC fillings across the entire EDGAR Database
-  For example, we can find all filings filed by Microsoft using a ticker search (ticker:MSFT) or build more complex search expressions using boolean and brackets operators
- The Query API returns the meta data of SEC filings matching the search query, such as filer details (e.g. ticker and company name), URLs to the filing and all exhibits, filing date, form type and more.
- We're looking for all filings with form type 10-K and its variants: 10-KT, 10KSB, 10KT405, 10KSB40, 10-K405. So, the Query API form type filter comes in handy.

` formType:("10-K", "10-KT", "10KSB", "10KSB40", "10-K405") `

- The brackets tell the Query API to include a filing in the response if the form type is either 10-K, or 10-KT, or 10KSB, and so on.

-The response of the Query API package in Python represents a dictionary (short: dict) with two keys: total and filings.

- The value of total is a dict itself and tells us, among other things, how many filings in total match our search query. The value of filings is a list of dicts, where each dict represents all meta data of a matching filing.

- We use the json Python package to pretty-print the first filing to the console to explore the structure of a filing dict.
