_ = require 'underscore'
mysql = require 'mysql'
express = require 'express'
bodyParser = require 'body-parser'

config = require '../../config.json'

pool = mysql.createPool config

list = (filter, cb) ->
  query = "SELECT tags.id, data_url, src_id, name, value, probability FROM src LEFT JOIN tags ON src.id = src_id WHERE type=1"
  query += " AND probability IS NOT NULL" if filter?
  query += " AND name IN (?)" if filter?
  pool.query(query, [filter]
    (err, data) ->
      obj = _.groupBy(data, (v) -> v.src_id)
      ret = _.sortBy (for k, v of obj
        image_url = v[0].data_url
        tags = (_.omit(vv, 'data_url', 'src_id') for vv in v)
        id: k, image_url: image_url, tags: tags
      ), (v) -> v.tags[0].value

      cb null, ret
  )
  return

listMiddleware = (req, res, next) ->
  filter = req.param('filter') || null
  filter = filter.split ',' if filter?
  list filter, (err, data) ->
    (next err; return) if err?
    res.jsonp data
    return
  return

postMiddleware = [ bodyParser(), (req, res, next) ->
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

module.exports.list = list
module.exports.app = app
