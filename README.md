# ALevelDump
A simple script used to scrape A/L results in given range of IDs.

### Usage: 

 - Adjust range in  `'__main__'`
 - Run `python run.py`

### Additional Options:

    usage: ALevelDump [-h] [-p PROCESSES] [-l LIMIT] [-sp PATTERN]
    
    A simple script used to scrape A/L results in given range of IDs (by chehanr)
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PROCESSES, --processes PROCESSES
                            number of processes
      -l LIMIT, --limit LIMIT
                            upper limit of ids
      -sp PATTERN, --pattern PATTERN
                            start pattern

### Prerequisites: 

 - Run `pip install -r "requirements.txt"`  
 - Have Selenium WebDriver (PhantomJS) in ENV or Path.
