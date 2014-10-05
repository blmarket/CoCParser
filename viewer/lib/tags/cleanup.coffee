_ = require 'underscore'

{pool} = require './common'

cleanUp = (cb) ->
  query = """
  DELETE FROM src WHERE id IN 
      (SELECT MID FROM 
          (SELECT MIN(src_id) as MID, COUNT(*) AS CNT, category, name, value 
           FROM src LEFT JOIN tags ON src.id = src_id WHERE type = 1 AND name = 'clan_place' 
           GROUP BY category, value
          ) AS t WHERE CNT > 1
      )
  ;
  """

  pool.query query, [ ], cb
  return

# Test 
cleanUp -> console.log arguments

middleware = (req, res, next) ->
  cleanUp (err) ->
    (next err; return) if err?
    res.jsonp "OK"
    return
  return

module.exports.middleware = middleware
