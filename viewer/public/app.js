var CCBSummaryCtrl, RecentCtrl, SampleListingCtrl, TagsViewerCtrl;

angular.module('cocviewer', ['ngResource']);

RecentCtrl = function($scope, $resource) {
  var Entries, Search;
  Entries = $resource('/tags/recent');
  Search = $resource('/tags/search/:name');
  $scope.entries = [];
  $scope.load = function() {
    $scope.entries = Entries.query({});
  };
  $scope.search = function(entry) {
    var name;
    name = function() {
      var it, _i, _len, _ref;
      _ref = entry.tags;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        it = _ref[_i];
        if (it.name === 'name') {
          return it.value;
        }
      }
    };
    $scope.entries = Search.query({
      name: name()
    });
  };
};

TagsViewerCtrl = function($scope, $resource) {
  var Samples;
  Samples = $resource('/tags/:id');
  $scope.samples = [];
  $scope.load = function() {
    $scope.samples = Samples.query({
      filter: ''
    }, function(data) {
      $scope.samples = data.sort(function(a, b) {
        if (a.name !== b.name) {
          if (a.name > b.name) {
            return 1;
          } else {
            return -1;
          }
        }
        if (a.value !== b.value) {
          if (a.value > b.value) {
            return 1;
          } else {
            return -1;
          }
        }
        return 0;
      });
      console.log($scope.samples);
    });
  };
  $scope.submit = function(tag) {
    Samples.save({
      id: tag.id
    }, tag);
  };
  $scope.audit_all = function() {
    var tag, _i, _len, _ref;
    _ref = $scope.samples;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      tag = _ref[_i];
      Samples.save({
        id: tag.id
      }, tag);
    }
  };
};

SampleListingCtrl = function($scope, $resource) {
  var Samples;
  $scope.samples = [];
  $scope.labels = [];
  $scope.filter = '';
  Samples = $resource('/samples/:id');
  $scope.load = function() {
    $scope.samples = Samples.query({
      filter: $scope.filter
    }, function() {
      var key;
      $scope.labels = (function() {
        var _results;
        _results = [];
        for (key in $scope.samples[0]) {
          if (key[0] !== '$' && key !== 'src_id' && key !== 'category') {
            _results.push(key);
          }
        }
        return _results;
      })();
      console.log($scope.labels);
    });
  };
  $scope.submit = function(sample) {
    sample.$save();
  };
};

CCBSummaryCtrl = function($scope, $resource) {
  var Samples;
  $scope.samples = [];
  $scope.labels = [];
  $scope.pid = 1;
  Samples = $resource('/db/get/:id', {
    pid: null
  });
  $scope.load = function() {
    $scope.samples = Samples.query({
      pid: $scope.pid
    }, function() {
      var it;
      $scope.labels = (function() {
        var _results;
        _results = [];
        for (it in $scope.samples[0]) {
          if (it[0] !== '$' && it !== 'src_id') {
            _results.push(it);
          }
        }
        return _results;
      })();
    });
  };
  $scope.submit = function(sample) {
    sample.$save();
  };
};
