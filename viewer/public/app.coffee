angular.module 'cocviewer', [ 'ngResource' ]

SampleListingCtrl = ($scope, $resource) ->
  $scope.samples = []
  Samples = $resource '/samples/:id'
  $scope.samples = Samples.query()

  $scope.submit = (sample) ->
    sample.$save()
    return
  return

# ADCtrl = ($scope, $resource) ->
#   $scope.accessKey = ''
#   $scope.uids = ''
#   $scope.getAccessKey = -> $scope.accessKey
#   $scope.messageList = []
# 
#   Users = $resource '/users/:sid', { sid: 84, accessKey: 'thisisaccesskey' }
#   Fetch = $resource '/data', {}, {
#     fetch: { method: 'POST' }
#   }
# 
#   $scope.fetch = ->
#     data = Users.query ->
#       arr = (item.uid for item in data)
#       $scope.uids = JSON.stringify arr
#       params = { accessKey: $scope.accessKey, uids: arr, sids: [ 55, 89, 84 ] }
#       tmp = Fetch.fetch(
#         params
#         (res) ->
#           console.log arguments
#           $scope.messageList.unshift([JSON.stringify(params), JSON.stringify(tmp, 0, 2)])
#           return
#         (err) ->
#           $scope.messageList.unshift([JSON.stringify(params), JSON.stringify(err)])
#           return
#       )
# 
#       return
#     return
#   return
