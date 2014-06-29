__author__ = 'drew'

from BeautifulSoup import BeautifulSoup

import MySQLdb
import Config
import urllib2
import random
import re

def getSource(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        request = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(request)
        page_source = response.read()
        return page_source
    except:
        return None

def visitedUrl(cursor, db, url):
    try:
        cursor.execute("INSERT INTO movie_urls_visited (url) VALUES (%s)", (url,))
        db.commit()
        return 0
    except:
        print 'Visited INSERT ERROR'
        return -1



def alreadyVisited(cursor, db, url):
    cursor.execute("SELECT id FROM movie_urls_visited WHERE url=%s", (url,))
    id = cursor.fetchone()
    if id:
        return True
    else:
        return False

def addMovie(cursor, db, title):
    try:
        cursor.execute("INSERT INTO movie_titles (title) VALUES (%s)", (title,))
        db.commit()
        return 0
    except:
        print 'Title INSERT ERROR'
        return -1

def main():
    db = MySQLdb.connect(host=Config.DBHOST, # your host, usually localhost
                         user=Config.DBUSER, # your username
                         passwd=Config.DBPASS, # your password
                         db=Config.DBNAME) # name of the data base


    cur = db.cursor()

    #cur.execute("SELECT * FROM User")

    #for row in cur.fetchall():
    #    print row[1]

    rootUrl = 'http://www.rottentomatoes.com'

    urls = []
    brokenUrls = []
    urls.append(rootUrl)
    while len(urls) != 0:
        currUrl = urls.pop()

        if currUrl in brokenUrls:
            continue

        if 'ad.doubleclick' in currUrl:
            brokenUrls.append(currUrl)
            continue

        if alreadyVisited(cur, db, currUrl):
            continue
        else:
            visitedUrl(cur, db, currUrl)

        urlSource = getSource(currUrl)
        if not urlSource:
            brokenUrls.append(currUrl)
            continue

        print 'Visiting: ' + currUrl

        soup = BeautifulSoup(urlSource)
        for link in soup.findAll('a'):
            linkHref = link.get('href')
            if not linkHref:
                continue
            if 'movie' in linkHref:
                if linkHref[0] == '/' and '.com' not in linkHref[0] and 'http' not in linkHref[0] and 'https' not in linkHref[0]:
                    url = rootUrl + linkHref
                    #print url
                    urls.append(url)
                    random.shuffle(urls)
                else:
                    continue
                    #url = linkHref
                    #print url
                    #urls.append(url)
                    #random.shuffle(urls)

        for link in soup.findAll('a', attrs={"target": "_top"}):
            success = addMovie(cur, db, link.contents[0].string)
            if success != -1:
                print 'Adding movie: ' + link.contents[0].string

        for link in soup.findAll('div', attrs={"class": "information"}):
            print link.find('a').contents[0].string


if __name__ == '__main__':
    main()