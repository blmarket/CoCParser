_ = require 'underscore'
mysql = require 'mysql'

config = require '../../config.json'

pool = mysql.createPool config

aggregate = (data) ->
  obj = _.groupBy(data, (v) -> v.src_id)
  return (for k, v of obj
    image_url = v[0].data_url
    date = v[0].category
    tags = (_.omit(vv, 'data_url', 'src_id') for vv in v)
    id: k, date: date, image_url: image_url, tags: tags
  )

module.exports.aggregate = aggregate
module.exports.pool = pool
