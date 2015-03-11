(function () {

  'use strict';

  angular.module('EnteDemoApp', [])

  .controller('EnteDemoController', ['$scope', '$log', '$http', '$timeout', function($scope, $log, $http, $timeout) {
    $scope.getResults = function() {
      $log.log("test");

      // get the URL from the input
      var userInput = $scope.input_node_id;
      // fire the API request
      $http.post('/start', {"node_id": userInput}).
        success(function(results) {
          $log.log(results);
          getJobResult(results);
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    function getJobResult(jobID) {
      var timeout = "";
      var poller = function() {
        // fire another request
        $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $timeout.cancel(timeout);
              $scope.parent_node = data["result"][0];
              $scope.child_nodes = data["result"][1];
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          });
      };
      poller();
    };
  }

  ]);

}());
