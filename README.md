# dateReplacer
Finds all date and time of a given webpage and format it by ISO8601 format.
- :Input: url
- :Output: text

#### Supported format 
- 民國105年10月10日 - Taiwan traditional datetime
- 2016-10-10
- Oct 10, 2016
- 2016年10月10日 
- 2016年10月
- 10月10日
- 同年10月 - In the same year
- 本月10日 - In this month
- 平成28年10月10日 - Japanese datetime representation

  
#### Recommended pages to test
 1. https://en.wikipedia.org/wiki/Date_format_by_country#cite_note-113"
 2. http://www.convertunits.com/dates/180/daysfrom/Oct+10,+2015
 
#### How to test online?
curl -H "Content-Type: application/json" -X POST -d '{"url":"REPLACE_YOUR_URL_HERE"}' https://fusions360.herokuapp.com/

