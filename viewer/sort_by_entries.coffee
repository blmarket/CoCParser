mysql = require 'mysql'
_ = require 'underscore'
async = require 'async'
express = require 'express'

config = require '../config.json'

pool = mysql.createPool config

get_name = (row, cb) ->
  id = row.id
  pool.query(
    "SELECT value FROM tags WHERE src_id = ? AND name = 'name'",
    [ id ],
    (err, rows) ->
      cb null, rows[0].value
      return
  )
  return

find_by_name = (name, cb) ->
  pool.query(
    "SELECT src_id FROM tags WHERE name = 'name' AND value = ?",
    [ name ],
    (err, rows) ->
      cb null, { 
        name: name,
        ids: (row.src_id for row in rows)
      }
      return
  )
  return

check_battle = (ids, cb) ->
  pool.query(
    """
    SELECT COUNT(value) AS g FROM tags WHERE src_id IN ? AND \
    name LIKE 'attack%' AND (value = '-1')
    """
    [ [ ids.ids ] ]
    (err, rows) ->
      (cb err; return) if err?
      console.log rows
      cb null, {
        name: ids.name
        entries: ids.ids.length
        off: rows[0].g
      }
      return
  )
  return


pool.query "SELECT id FROM src WHERE category = '20141221'", (err, rows) ->
  async.map rows, get_name, (err, rs) ->
    async.map rs, find_by_name, (err, ids) ->
      async.map ids, check_battle, (err, res) ->
        console.log _.sortBy(res, (a) -> a.off)
        process.exit()
        return
      return
    return
  return
