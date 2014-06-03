_ = require 'underscore'
mysql = require 'mysql'
express = require 'express'

config = require '../../config.json'

pool = mysql.createPool config

list = (cb) ->
  pool.query(
    "SELECT data_url, src_id, name, value, probability FROM src LEFT JOIN tags ON src.id = src_id WHERE type=1 AND probability IS NOT NULL"
    (err, data) ->
      obj = _.groupBy(data, (v) -> v.src_id)
      ret = (for k, v of obj
        image_url = v[0].data_url
        tags = (_.omit(vv, 'data_url', 'src_id') for vv in v)
        id: k, image_url: image_url, tags: tags
      )

      cb null, ret
  )
  return

listMiddleware = (req, res, next) ->
  list (err, data) ->
    (next err; return) if err?
    res.jsonp data
    return
  return

app = express()
app.get '/', listMiddleware

module.exports = app
