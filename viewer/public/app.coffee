angular.module 'cocviewer', [ 'ngResource' ]

SampleListingCtrl = ($scope, $resource) ->
  $scope.samples = []
  $scope.labels = []
  $scope.filter = ''

  Samples = $resource '/samples/:id'

  $scope.load = ->
    $scope.samples = Samples.query { filter: $scope.filter }, ->
      $scope.labels = (key for key of $scope.samples[0] when key[0] != '$' and key != 'src_id' and key != 'category')
      console.log $scope.labels
      return
    return

  $scope.submit = (sample) ->
    sample.$save()
    return
  return

CCBSummaryCtrl = ($scope, $resource) ->
  $scope.samples = []
  $scope.labels = []

  Samples = $resource '/db/get/:id', { pid: null }

  $scope.load = ->
    $scope.samples = Samples.query { pid: 2 }, ->
      $scope.labels = (it for it of $scope.samples[0] when it[0] != '$' and it != 'src_id')
      return
    return

  $scope.submit = (sample) ->
    sample.$save()
    return
  return
