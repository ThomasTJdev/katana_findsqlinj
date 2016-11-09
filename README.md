mcs/gd.sql module for Katana
========================================

Module for finding website vuln for SQL injections

Katana/modules/mcs/prone_to_sql.py

 This python script is developed to show, how many vulnerables websites,
 which are laying around on the web. The main focus of the script is to
 generate a list of vuln urls. Please use the script with causing and
 alert the webadmins of vulnerable pages. The SQLmap implementation is
 just for showcasing.

## Requirements
* python2 (developed for python3 - python3 is still included but comment out)
* BeautifulSoup from bs4
* (optional) sqlmap
* [Katana](https://github.com/PowerScript/Katana)

## The script
 The script is divided into 3 main sections.
 
### Section 1
   In this section you have to provide a search string, which 'connects' to
   the websites database, e.g. 'php?id='. The script then crawls
   Bing or Google for urls containing it. 
   (Please be aware that you might get banned for crawling to fast, remember 
   an appropriate break/sleep between request).
   *Example of searches: php?bookid=, php?idproduct=, php?bookid=, php?catid=,*
                       *php?action=, php?cart_id=, php?title=, php?itemid=*

### Section 2
   This section adds a qoute ' to the websites url. If the website is
   prone to SQL injection, we'll catch this with some predefined error
   messages. The script will not add websites for blind SQL injections,
   due to the predefined error messages.

### Section 3
   This is just an activation of sqlmap with the bulk argument and no
   user interaction for validation of SQL injection.

License
-------

MIT, 2016 Thomas TJ (TTJ)

Other
-----

Want to try it without Katana? Test it with python3 here [findsqlinj](https://gitlab.com/ThomasTJ/find_sql_injection)
