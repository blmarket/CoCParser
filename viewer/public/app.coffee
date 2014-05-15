angular.module 'cocviewer', [ 'ngResource' ]

SampleListingCtrl = ($scope, $resource) ->
  $scope.samples = []
  $scope.filter = ''

  Samples = $resource '/samples/:id'

  $scope.load = ->
    $scope.samples = Samples.query { filter: $scope.filter }
    return

  $scope.submit = (sample) ->
    sample.$save()
    return
  return
