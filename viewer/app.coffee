_ = require 'underscore'
http = require 'http'
express = require 'express'
cors = require 'cors'

db = require './lib/db'
tags_app = require './lib/tags'

app = express()

app.use cors()

app.use (req, res, next) ->
  res.locals.pretty = true
  next()
  return

# TAGS api
app.use '/tags', tags_app.app

app.get '/check', (req, res) ->
  res.render 'tags_viewer.jade'
  return

app.use '/', express.static(__dirname + '/dist')

port = process.env.PORT || 3000
http.createServer(app).listen(port)
