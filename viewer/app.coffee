do ->
  fs = require 'fs'
  CS = require 'coffee-script'
  data = fs.readFileSync(__dirname + '/public/app.coffee').toString()
  fs.writeFileSync(__dirname + '/public/app.js', CS.compile data, { bare: true })
  return

http = require 'http'
express = require 'express'
morgan = require 'morgan'
mysql = require 'mysql'
bodyParser = require 'body-parser'

pool = mysql.createPool {
  host: 'localhost'
  user: 'root'
  database: 'cocparser'
}

app = express()

app.use morgan()
app.use (req, res, next) ->
  res.locals.pretty = true
  next()
  return

app.get '/', (req, res) -> res.render 'index.jade'
app.get '/labels/:id', (req, res, next) ->
  id = req.param 'id'
  pool.query 'SELECT * FROM samples WHERE src_id = ? LIMIT 1', [ id ], (err, rows) ->
    (next err; return) if err?
    (next new Error('no such row'); return) if rows.length == 0
    console.log rows[0]
    return
  return

app.get '/img/:id', (req, res, next) ->
  id = req.param 'id'
  pool.query 'SELECT `PNG` FROM src WHERE id = ? LIMIT 1', [ id ], (err, rows) ->
    (next err; return) if err?
    (next new Error('no such row'); return) if rows.length == 0
    ret = rows[0]['PNG']
    res.header('Content-type', 'image/png')
    res.send ret
    return
  return

app.get '/samples', (req, res) ->
  pool.query 'SELECT * FROM samples WHERE predict_attack = 1 ORDER BY name LIMIT 200', [], (err, rows) ->
    res.jsonp rows
  return

app.post '/samples', bodyParser(), (req, res, next) ->
  reqbody = req.body
  fields = (key for key of reqbody when key != 'id' and key != 'src_id')

  query = 'UPDATE samples SET `id` = `id`'
  params = []
  for field in fields
    query += ", `#{field}` = ? "
    params.push reqbody[field] || null

  query += ' WHERE src_id = ?'
  params.push reqbody.src_id

  pool.query query, params, (err) ->
    (next err; return) if err?
    res.jsonp req.body
    return
  return

app.use '/public', express.static(__dirname + '/public')

http.createServer(app).listen(3000)
