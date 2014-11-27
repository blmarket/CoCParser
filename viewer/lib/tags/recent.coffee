_ = require 'underscore'

{pool, aggregate} = require './common'

recent = (cb) ->
  query = """
  SELECT src_id, category, data_url, name, value \
  FROM src LEFT JOIN tags ON src.id = src_id \
  WHERE src.type = '1' AND \
  src.category = ( \
    SELECT category FROM src ORDER BY id DESC LIMIT 1 \
  )
  """

  getV = (arr, k) -> return Number(it.value) for it in arr when it.name == k

  pool.query query, [ ], (err, rows) ->
    (cb err; return) if err?
    ret = _.sortBy aggregate(rows), (v) -> getV(v.tags, 'clan_place')
    cb null, ret
    return
  return

recentMiddleware = (req, res, next) ->
  recent (err, data) ->
    (next err; return) if err?
    console.log data
    res.jsonp data
    return
  return

module.exports.recentMiddleware = recentMiddleware
