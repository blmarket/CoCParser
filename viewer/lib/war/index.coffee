_ = require 'lodash'
express = require 'express'
bodyParser = require 'body-parser'

{handle_recent} = require '../recent_date'
{pool} = require '../common'

date = '20150306'

pool.query(
  '''
  SELECT war.*, t1.value AS target1, t2.value AS target2 FROM war 
  JOIN tags AS t1 ON atk1_src = t1.src_id 
  JOIN tags AS t2 ON atk2_src = t2.src_id
  WHERE t1.name = 'number'
  AND t2.name = 'number'
  AND war.date = ?
  ''', [ date ], (err, rows) ->
    console.log rows
    return
)

by_date = (date, cb) ->
  pool.query '''
  SELECT eff_atks.*, src.data_url AS data_url FROM eff_atks LEFT JOIN src ON src_id = src.id WHERE date = ?
  ''', [ date ], (err, res) ->
    (cb err; return) if err?
    grouped = _.map(_.values(_.groupBy(res, (obj) -> obj.group_id)), (x) -> { group_id: x[0].group_id, data: x })
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
