import gdata.spreadsheet.service
import MySQLdb as mdb
import json

config = json.load(open('config.json'))

def readMySQL():
    con = mdb.connect(config[u'host'], config[u'user'], config[u'password'], config[u'database'])
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM samples")
        for it in cur.fetchall():
            print it

client = gdata.spreadsheet.service.SpreadsheetsService()
client.email = 'blmarket@gmail.com'
client.password = '' # fill password...
client.ProgrammaticLogin()

target_id = "1DdAxXDlKcdL5NlOOdWliH508vNmCyo_sI34Giw5SgPQ"

print client
