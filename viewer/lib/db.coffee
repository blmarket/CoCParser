mysql = require 'mysql'

config = require '../../config.json'

pool = mysql.createPool config

createPrediction = (type, field_name, cb) ->
  pool.query('''
  INSERT INTO `predictions` (`type`, `field_name`) VALUES (?, ?)
  ''', [type, field_name], (err, rows) -> cb err; return
  )
  return

getPrediction = (pid, cb) ->
  pool.query(
    'SELECT * FROM `predictions` WHERE `id` = ?', [ pid ]
    (err, rows) ->
      (cb err; return) if err?
      (cb new Error('no such row'); return) if rows.length == 0
      cb null, rows[0]
      return
  )
  return

getByPid = (pid, cb) ->
  getPrediction pid, (err, res) ->
    (cb err; return) if err?
    {type, field_name} = res
    pool.query("""
    SELECT `src`.`id` AS `src_id`, `samples`.??, `p`.`predict_result` \
    FROM `src` LEFT JOIN `samples` ON `src`.`id` = `samples`.`src_id` \
      LEFT JOIN (SELECT `src_id`, `predict_result` FROM `predict_result` WHERE `pid` = ?) AS `p` 
        ON `src`.`id` = `p`.`src_id` \
    WHERE `src`.`type` = ? 
    """, [field_name, pid, type], (err, rows) -> cb err, rows
    )
    return
  return

getMiddleware = (req, res, next) ->
  pid = req.param 'pid'

  getByPid pid, (err, rows) ->
    (next err; return) if err?
    res.jsonp rows
    return
  return

exports.getMiddleware = getMiddleware
