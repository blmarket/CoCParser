_ = require 'lodash'
async = require 'async'
express = require 'express'
bodyParser = require 'body-parser'

{handle_recent} = require '../recent_date'
{pool} = require '../common'

by_date = (date, callback) ->
  tag_clouds = (cb) ->
    pool.query(
      '''
      SELECT war.id, tags.name, tags.value FROM war
      JOIN tags ON war.src_id = tags.src_id 
      WHERE war.date = ?
      ''', [ date ], (err, rows) ->
        (cb err; return) if err?
        ret = _.mapValues(
          _.groupBy(rows, (it) -> it.id)
          (it) -> 
            _.reduce(it, 
              (res, jt) ->
                res[jt.name] = jt.value
                return res
              {}
            )
        )
        cb null, ret
        return
    )
    return

  target_ranks = (cb) ->
    pool.query(
      '''
      SELECT war.id, war.date, src.data_url, 
        t1.value AS target1, t2.value AS target2 FROM war 
      JOIN src ON war.src_id = src.id
      JOIN tags AS t1 ON atk1_src = t1.src_id 
      JOIN tags AS t2 ON atk2_src = t2.src_id
      WHERE t1.name = 'number'
      AND t2.name = 'number'
      AND war.date = ?
      ''', [ date ], (err, rows) ->
        (cb err; return) if err?
        cb null, rows
        return
    )
    return

  async.parallel [ target_ranks, tag_clouds ], (err, results) ->
    (callback err; return) if err?
    [ ret, clouds ] = results
    for it in ret
      it.tags = clouds[it.id]
    callback null, _.sortBy(ret, (it) -> Number(it.tags.clan_place))
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

# Test code here
if require.main == module
  by_date '20150306', (err, res) ->
    console.log err
    console.log res
    return

module.exports.app = app
