{pool} = require './common'

recent = (cb) ->
  query = "SELECT category FROM src WHERE category NOT LIKE 'E%' ORDER BY id DESC LIMIT 1"
  pool.query query, (err, rows) ->
    (cb err; return) if err?
    cb null, rows[0].category
    return
  return

handle_recent = (req, res, next) ->
  date = req.params.date
  if date == 'recent'
    recent (err, recent_date) ->
      (next err; return) if err?
      req.params.date = recent_date
      next()
      return
    return
  next()
  return

module.exports.recent = recent
module.exports.handle_recent = handle_recent
