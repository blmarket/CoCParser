angular.module 'cocviewer', [ 'ngResource' ]

RecentCtrl = ($scope, $resource) ->
  Entries = $resource '/tags/recent'
  Search = $resource '/tags/search/:name'

  $scope.entries = []

  $scope.load = ->
    $scope.entries = Entries.query {}
    return

  $scope.search = (entry) ->
    name = ->
      return it.value for it in entry.tags when it.name == 'name'
    $scope.entries = Search.query { name: name() }
    return

  return

TagsViewerCtrl = ($scope, $resource) ->
  Samples = $resource '/tags/:id'

  $scope.samples = []

  $scope.load = ->
    $scope.samples = Samples.query { filter: '' }, (data) ->
      $scope.samples = data.sort (a, b) ->
        if a.name != b.name
          return if (a.name < b.name) then 1 else -1
        if a.value != b.value
          return if (a.value < b.value) then 1 else -1
        return 0
      console.log $scope.samples
      return
    return

  $scope.submit = (tag) ->
    Samples.save( { id: tag.id }, tag)
    return
  return

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
  $scope.pid = 1

  Samples = $resource '/db/get/:id', { pid: null }

  $scope.load = ->
    $scope.samples = Samples.query { pid: $scope.pid }, ->
      $scope.labels = (it for it of $scope.samples[0] when it[0] != '$' and it != 'src_id')
      return
    return

  $scope.submit = (sample) ->
    sample.$save()
    return
  return
