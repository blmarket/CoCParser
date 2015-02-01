_ = require 'underscore'
express = require 'express'
bodyParser = require 'body-parser'

{pool, aggregate} = require '../common'
{searchMiddleware} = require './search'
{dateMiddleware, recentMiddleware} = require './recent'
cleanup = require './cleanup'

list = (date, filter, cb) ->
  query = "SELECT tags.id, data_url, src_id, name, value, probability FROM src LEFT JOIN tags ON src.id = src_id WHERE type=1"
  query += " AND category = ?" if date?
  query += " AND probability IS NOT NULL"
  query += " AND name IN (?)" if filter?
  query += " ORDER BY probability ASC LIMIT 100"

  params = []
  params.push date if date?
  params.push filter if filter?

  pool.query query, params, cb
  return

listMiddleware = (req, res, next) ->
  filter = req.param('filter') || null
  date = req.param('date')
  filter = filter.split ',' if filter?
  list null, filter, (err, data) ->
    (next err; return) if err?
    res.jsonp data
    return
  return

postMiddleware = [ bodyParser.json(), (req, res, next) ->
  id = Number(req.param('id'))
  obj = _.pick(req.body, 'name', 'value')
  obj.probability = null

  pool.query "UPDATE tags SET ? WHERE id = ?", [ obj, id ], (err) ->
    (next err; return) if err?
    res.send 204
    return
  return
]

app = express()
app.get '/', listMiddleware
app.post '/:id', postMiddleware
app.get '/search/:name', searchMiddleware
app.get '/recent', recentMiddleware
app.get '/cleanup', cleanup.middleware
app.get '/date/:date', dateMiddleware

module.exports.list = list
module.exports.app = app
