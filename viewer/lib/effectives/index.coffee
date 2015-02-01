_ = require 'lodash'
express = require 'express'
bodyParser = require 'body-parser'

{recent} = require '../recent_date'
{pool} = require '../common'

handle_recent = (req, res, next) ->
  date = req.params.date
  if date == 'recent'
    recent (err, recent_date) ->
      (next err; return) if err?
      req.params.date = recent_date
      next()
      return
  next()
  return

by_date = (date, cb) ->
  pool.query '''
  SELECT * FROM eff_atks WHERE date = ?
  ''', [ date ], (err, res) ->
    (cb err; return) if err?
    grouped = _.sortBy(_.values(_.groupBy(res, (obj) -> obj.group_id)), 'length')
    cb null, grouped
    return
  return

app = express()
app.get '/date/:date', handle_recent, (req, res, next) ->
  date = req.params.date
  by_date date, (err, data) ->
    (next err; return) if err?
    res.jsonp data
    return
  return

module.exports.app = app
