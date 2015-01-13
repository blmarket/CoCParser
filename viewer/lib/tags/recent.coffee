_ = require 'underscore'
async = require 'async'

{pool, aggregate} = require './common'

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

recent = (cb) ->
  query = "SELECT category FROM src ORDER BY id DESC LIMIT 1"
  pool.query query, (err, rows) ->
    (cb err; return) if err?
    date_view rows[0].category, cb
    return
  return

recent_v2 = (cb) ->
  query = "SELECT category FROM src ORDER BY id DESC LIMIT 1"
  pool.query query, (err, rows) ->
    (cb err; return) if err?
    now = rows[0].category
    console.log now
    f1 = (cb) -> date_view now, cb
    f2 = (cb) -> date_browse now, cb
    async.parallel [ f1, f2 ], (err, results) ->
      (cb err; return) if err?
      cb null, {
        list: results[0]
        browse: results[1]
      }
      return
    return
  return

recentMiddleware = (req, res, next) ->
  recent (err, data) ->
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
    recent base_cb
  else
    date_view date, base_cb
  return

module.exports.recentMiddleware = recentMiddleware
module.exports.dateMiddleware = dateMiddleware
