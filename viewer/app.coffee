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

config = require '../config.json'

pool = mysql.createPool config

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

app.get '/samples', (req, res, next) ->
  filter_query = req.param('filter') || '1'
  pool.query(
    """
    SELECT `src`.`id` AS `src_id`, `category`, `name`, `attack`, `predict_attack`, `atkstars`, `predict_atkstars` \
    FROM `src` LEFT JOIN `samples` ON `src`.`id` = `samples`.`src_id` \
    WHERE #{filter_query} \
    ORDER BY category DESC, predict_attack = 1 DESC, predict_attack DESC, name, predict_atkstars DESC LIMIT 200
    """
    []
    (err, rows) ->
      (next err; return) if err?
      res.jsonp rows
      return
  )
  return

app.post '/samples', bodyParser(), (req, res, next) ->
  reqbody = req.body
  fields = (key for key of reqbody when key != 'id' and key != 'src_id')

  pool.query 'INSERT IGNORE INTO samples (src_id) VALUES (?)', [ reqbody.src_id ], (err) ->
    (next err; return) if err?
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
  return

app.use '/public', express.static(__dirname + '/public')

http.createServer(app).listen(3000)
