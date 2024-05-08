# Full-Text Search API

Full-text search allows you to search the full text of all EDGAR filings submitted since 2001. The full text of a filing includes all data in the filing itself as well as all attachments (such as exhibits) to the filing.

You can search by keyword, ticker, company name, CIK number, and/or reporter's last name—individually or in combination.

Boolean operators allow for searches where all words entered are required to be in the resulting documents, exact phrases matching, exclude terms, OR logic clauses, and wildcards. Any of these can be combined in a single search.

## API Endpoint

`https://api.sec-api.io/full-text-search`

Supported HTTP methods: POST

Request and response content type: JSON

## Authentication

Use the API key shown in your user profile after sign up. There are two ways to use your API key. It's either/or.

- Set as Authorization header. Before making a POST request to `https://api.sec-api.io/full-text-search`, you need to set the Authorization header to YOUR_API_KEY
- Set as query parameter. Example: `https://api.sec-api.io/full-text-search?token=YOUR_API_KEY`

In this case, you make POST requests to the endpoint `https://api.sec-api.io/full-text-search?token=YOUR_API_KEY` and not anymore to `https://api.sec-api.io/full-text-search`.

## Response Format

Returned filings are sorted by an internal score. The score is calculated based on the number of occurrences of the search term in the document. The more often a search term is present in the document, the higher the score. Filings with the highest score are returned first. Each response returns 100 filings matching your search.

The API returns a JSON object with two keys:

- `total` (object) - An object with two variables "value" and "relation". If "relation" equals "gte" (= greater than or equal), the "value" is always 10,000. This indicates that more than 10,000 filings match the query. In order to retrieve all filings, you have to iterate over the results using the "from" and "size" variables sent to the API. If "relation" equals "eq" (= equal), the "value" represents the exact number of filings matching the query. In this case, "value" is always less than 10,000. We don't calculate the exact number of matching filings for results greater than 10,000.
- `filings` (array) - The array holding all filings matching your search criteria. Filing format:
    - `accessionNo` (string) - accession number of filing. Example: 0000065011-21-000020
    - `cik` (string) - CIK of filer. Trailing zeros are removed. Example: 65011
    - `companyNameLong` (string) - company name of the filer. Example: MEREDITH CORP (MDP) (CIK 0000065011)
    - `ticker` (string) - if available, ticker of the filer.
    - `description` (string) - description of the document. Example: EXHIBIT 99 FY21 Q2 EARNINGS PRESS RELEASE
    - `formType` (string) - filing type. Example: 8-K
    - `type` (string) - type of the document. Example: EX-99
    - `filingUrl` (string) - URL of the filing or attachment. Example: https://www.sec.gov/Archives/edgar/data/65011/000006501121000020/fy21q2exh99earnings.htm
    - `filedAt` (string) - date of filing. Format: yyyy-mm-dd Example: 2021-02-04

## Request Parameters

Request parameters in POST body. JSON.

- `query` (string, required) - search string, case insensitive. Example: apple returns all filings and attachments mentioning "apple".
- `startDate` (string, optional) - used in combination with endDate. Allows searching for filings filed from startDate to endDate. Format: yyyy-mm-dd. Example: 2021-02-19. Default: 30 days ago.
- `endDate` (string, optional) - used in combination with startDate. Same format as startDate. Default: today.
- `ciks` (array of strings, optional) - if set, the system only considers filings filed by a CIK listed in the array. Trailing zeros in a CIK are not required, but can be provided. Example: [ "0001811414", "1318605" ]. Default: all CIKs.
- `formTypes` (array of strings, optional) - if set, the system only searches in filings (and their attachments) of the specified type. All other filing types are ignored. Example: [ "8-K", "10-Q", "10-K" ]. Default: all filings.
- `page` (string, optional) - used for pagination. The API returns 100 matching filings per request. Increase the value in order to retrieve the next 100 filings matching your search. Example: 3 returns the third page. Default: 1.
