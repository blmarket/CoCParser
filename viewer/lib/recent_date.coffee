{pool} = require './common'

recent = (cb) ->
  query = "SELECT category FROM src ORDER BY id DESC LIMIT 1"
  pool.query query, (err, rows) ->
    (cb err; return) if err?
    cb null, rows[0].cateogry
    # date_view rows[0].category, cb
    return
  return

module.exports.recent = recent
