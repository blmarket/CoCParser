_ = require 'underscore'
http = require 'http'
express = require 'express'
cors = require 'cors'
crypto = require 'crypto'

sha1_hash = (str) ->
  sum = crypto.createHash 'sha1'
  sum.update str
  return sum.digest 'hex'

config = require '../config.json'

tags_app = require './lib/tags'

app = express()

app.use cors()

app.use (req, res, next) ->
  res.locals.pretty = true
  next()
  return

# TAGS api
app.use '/tags', tags_app.app

mutt_auth = (name = 'anonymous', admin = false) ->
  ts = Math.round(+new Date / 1000)
  msg = new Buffer(JSON.stringify { user: {
    id: name
    displayname: name
    email: ''
    avatar: ''
    is_admin: admin
  } }).toString('base64')
  signature = sha1_hash("#{config.muut.secret} #{msg} #{ts}")

  return { api: {
    key: config.muut.key
    timestamp: ts
    message: msg
    signature: signature
  } }

app.get '/api/muut', (req, res, next) ->
  res.jsonp mutt_auth()
  return

app.get '/:url(api|app|bower_components|assets)/*', express.static(__dirname + '/dist')

# All other routes should redirect to the index.html
app.get '/*', (req, res) ->
  res.sendFile(__dirname + '/dist/index.html')
  return

port = process.env.PORT || 3000
http.createServer(app).listen(port)
