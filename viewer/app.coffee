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

app.get '/:url(api|app|bower_components|assets)/*', express.static(__dirname + '/dist')

# All other routes should redirect to the index.html
app.get '/*', (req, res) ->
  res.sendFile(__dirname + '/dist/index.html')
  return

port = process.env.PORT || 3000
http.createServer(app).listen(port)
