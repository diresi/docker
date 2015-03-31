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
            $scope.error = false;

            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $timeout.cancel(timeout);

              var result = data["result"];
              $scope.attribs = result["attribs"];
              $scope.node = result["node"];
              $scope.parent_nodes = result["parents"];
              $scope.child_nodes = result["children"];
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          }).
          error(function(data, status, headers, config){
              $log.log(data);
              $scope.error = data;
          });
      };
      poller();
    };

    $scope.showNode = function(node_id) {
        $log.log("showNode", node_id);
        $scope.input_node_id = node_id;
        $scope.getResults();
    };
  }

  ]);

}());
