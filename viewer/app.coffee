# do ->
#   fs = require 'fs'
#   CS = require 'coffee-script'
#   data = fs.readFileSync(__dirname + '/public/app.coffee').toString()
#   fs.writeFileSync(__dirname + '/public/app.js', CS.compile data, { bare: true })
#   return

_ = require 'underscore'
http = require 'http'
express = require 'express'
morgan = require 'morgan'

db = require './lib/db'
tags_app = require './lib/tags'

app = express()

app.use morgan()
app.use (req, res, next) ->
  res.locals.pretty = true
  next()
  return

app.use '/public', express.static(__dirname + '/public')

# TAGS api
app.use '/tags', tags_app.app

app.get '/check', (req, res) ->
  res.render 'tags_viewer.jade'
  return

app.get '/', (req, res) ->
  res.render 'war_index.jade'
  return

port = process.env.PORT || 3000
http.createServer(app).listen(port)
