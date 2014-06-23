_ = require 'underscore'
mysql = require 'mysql'
express = require 'express'

{list} = require './lib/tags'
config = require '../config.json'

pool = mysql.createPool config

list '20140608', null, (err, res) ->
  params = (for it in res
    kv = { url: it.image_url }
    for t in it.tags
      kv[t.name] = t.value
    [ kv.url, kv.clan_place, kv.name, kv.attack1, kv.attack2, kv.total_stars ]
  )

  pool.query "TRUNCATE samples", ->
    pool.query "INSERT INTO samples (url, clan_place, name, attack1, attack2, total_stars) VALUES ?", [params], (err, res) ->
      console.log err
      console.log res
      process.exit 0
      return
    return
  return
