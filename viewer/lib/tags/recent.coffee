_ = require 'underscore'
async = require 'async'

{pool, aggregate} = require '../common'
{recent} = require '../recent_date'

date_view = (date, cb) ->
  query = """
  SELECT src_id, category, data_url, name, value \
  FROM src LEFT JOIN tags ON src.id = src_id \
  WHERE src.type = '1' AND \
  src.category = ?
  """

  getV = (arr, k) -> return Number(it.value) for it in arr when it.name == k

  pool.query query, [ date ], (err, rows) ->
    (cb err; return) if err?
    ret = _.sortBy aggregate(rows), (v) -> getV(v.tags, 'clan_place')
    cb null, ret
    return
  return

date_browse = (date, cb) ->
  q1 = (cb) -> pool.query "SELECT MAX(category) AS prev FROM src WHERE category < ?", [ date ], (err, res) -> cb err, res
  q2 = (cb) -> pool.query "SELECT MIN(category) AS next FROM src WHERE category > ?", [ date ], (err, res) -> cb err, res

  async.parallel [ q1, q2 ], (err, results) ->
    (cb err; return) if err?
    cb null, [ results[0][0].prev, results[1][0].next ]
    return
  return

recentMiddleware = (req, res, next) ->
  recent (err, date) ->
    (next err; return) if err?
    date_view date, (err, data) ->
      (next err; return) if err?
      res.jsonp data
    return
  return

dateMiddleware = (req, res, next) ->
  date = req.param 'date'
  base_cb = (err, data) ->
    (next err; return) if err?
    res.jsonp data
    return
  if date == 'latest'
    recent (err, latest_date) ->
      (next err; return) if err?
      date_view latest_date, base_cb
      return
  else
    date_view date, base_cb
  return

module.exports.recentMiddleware = recentMiddleware
module.exports.dateMiddleware = dateMiddleware
