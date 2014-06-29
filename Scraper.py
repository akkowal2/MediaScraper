__author__ = 'drew'

from BeautifulSoup import BeautifulSoup

import MySQLdb
import Config

def main():
    db = MySQLdb.connect(host=Config.DBHOST, # your host, usually localhost
                         user=Config.DBUSER, # your username
                         passwd=Config.DBPASS, # your password
                         db=Config.DBNAME) # name of the data base

    cur = db.cursor()

    cur.execute("SELECT * FROM User")

    for row in cur.fetchall() :
        print row[1]


if __name__ == '__main__':
    main()