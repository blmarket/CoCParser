fs = require 'fs'
mysql = require 'mysql'

conn = mysql.createConnection {
  host: 'localhost'
  user: 'root'
  database: 'cocparser'
}

conn.query 'SELECT * FROM src', (err, rows) ->
  conn.end()
  for row in rows
    fs.writeFile "#{row.id}.png", row.PNG, -> return
  return
