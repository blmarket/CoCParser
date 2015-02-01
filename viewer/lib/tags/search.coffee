_ = require 'underscore'

{pool, aggregate} = require '../common'

search = (name, cb) ->
  query = """
  SELECT src_id, category, data_url, name, value \
  FROM src LEFT JOIN tags ON src.id = src_id \
  WHERE \
  src.id IN (SELECT src_id FROM tags WHERE name = 'name' AND value = ? AND probability IS NULL) AND \
  probability IS NULL ORDER BY src_id
  """
  pool.query query, [ name ], (err, rows) ->
    (cb err; return) if err?
    ret = _.sortBy aggregate(rows), (v) -> -v.id
    cb null, ret
    return
  return

# search 'shashagaga', -> console.log arguments

searchMiddleware = (req, res, next) ->
  name = req.param 'name'
  search name, (err, data) ->
    (next err; return) if err?
    res.jsonp data
    return
  return

module.exports.searchMiddleware = searchMiddleware
