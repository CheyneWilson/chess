'use strict';

var app = angular.module('chess', ['ngAnimate', 'ngSanitize', 'mgcrea.ngStrap']);


angular.module('chess').controller('Login', ["$scope", "myService",
    function($scope, myService) {
        $scope.formData = {};

        $scope.login = function() {
            var username = $scope.formData.username;
            var password = $scope.formData.password;
            var promise = myService.login(username, password);
            promise.then(function() {
                location.reload()
            });
        }
        $scope.logout = function() {
            var promise = myService.logout();
            promise.then(function() {
                location.reload()
            });
        }
    }
]);

angular.module('chess').controller('ChangeGame', ["$rootScope", "$scope", "$select", "myService",
    function($rootScope, $scope, $select, myService) {
        var reloadGameList = function(selectNew) {
            myService.listGames().then(function() {
                $scope.icons = myService.allGames;
                if (selectNew == true) {
                    var item = $scope.icons[$scope.icons.length - 1];
                    $scope.selected = item.value;
                    $scope.selectedIcon = item.value;
                }
            });
        };

        $rootScope.$on('chess.newGame', function() {
            reloadGameList(true);
        });

        $scope.$on('$select.select', function(event, value, index) {
            var gameId = value;
            var promise = myService.loadGame(gameId);
            promise.then(function() {
                $rootScope.$emit('chess.gameLoaded');
            });
        });

        reloadGameList();
    }
]);

/* This controller supports the modals for new game */
angular.module("chess").controller("NewGameOptions", ["$rootScope", "$scope",  "$select", "$modal", "myService",
    function($rootScope, $scope, $select, $modal, myService) {

        $scope.selectChallenge = function() {
            $scope.gameMode = "challenge";
        };

        $scope.selectAi = function() {
            $scope.gameMode = "ai";
        };

        var reloadActivePlayers = function() {
            myService.listActivePlayers().then(function(data) {
                $scope.players = myService.activePlayers;
                // $scope.players = data.players;
            });
        };

        var reloadAgents = function() {
            myService.listAgents().then(function(data) {
                $scope.agents = data.agents;
            });
        };

        reloadAgents();
        reloadActivePlayers();

        $scope.createGame = function() {
            if ($scope.gameMode == "hotseat") {
                myService.hotseat().then(function(data) {
                    // $scope.board = data.board;
                    $rootScope.$emit('chess.newGame');
                },
                function(errorMessage) {
                    $scope.error = errorMessage; // TODO: This isn't displayed
                });
            }
            if ($scope.gameMode == "challenge") {
                // TODO: Create periodic service
            }
            if ($scope.gameMode == "ai") {
                alert("Not implemented yet sorry :'(");
            }

            $scope.$hide();
        };
    }
]);

angular.module("chess").controller("DrawBoard", ["$rootScope", "$scope", "$http", "myService",
    function($rootScope, $scope, $http, myService) {
        $scope.board = {}

        var reloadBoard = function() {
            $scope.gameId = myService.gameId;
            $scope.board = myService.board;
            $scope.winner = myService.winner;
            $scope.currentPlayer = myService.currentPlayer;
            $scope.promotablePieces = myService.promotablePieces;
            $scope.moves = myService.moves;
            $scope.code = myService.code;
        };

        // var realoadMoves = function(){
        //     $scope.previousMoves = myService.previousMoves
        // }

        $rootScope.$on('chess.boardChanged', reloadBoard);
        $rootScope.$on('chess.newGame', reloadBoard);
        $rootScope.$on('chess.gameLoaded', reloadBoard);

        $scope.promote = function(piece) {
            promise = myService.promote(piece);
            promise.then(function() {
                $rootScope.$emit('chess.boardChanged');
            });
        };

        $scope.highlight = function(loc){
            if (currentPlayerPiece($scope, loc)){
                return ['occupied'];
            } else {
                return [];
            }
        };

        $scope.showGameOver = function(){
            if ($scope.winner == "BLACK" || $scope.winner == "WHITE" || $scope.winner == "DRAW"){
                return true;
            } else {
                return false;
            }
        };
        /*
         * This function highlights all the moves the selected piece can make.
         * It clears the highlighting on previously highlighted squares
         * It is attached to each piece
         */
        $scope.selectPiece = function(loc){
            // Highlight piece
            if ($scope.from != null) {
                // We already have a piece highlighed, try and move it to the location chosen
                if ($scope.highlight[loc]) {
                    // Deselect square if clicked on
                    if ($scope.from == loc) {
                        clearHighlight($scope);
                        return;
                    }

                    var promise = myService.movePiece($scope.gameId, $scope.from, loc);
                    promise.then(function(data) {
                        // $scope.board = myService.board;
                        //$rootScope.$emit('chess.moveTaken');
                        clearHighlight($scope);
                        $rootScope.$emit('chess.boardChanged');
                    },
                    function(errorMessage) {
                        $scope.error = errorMessage; // TODO: This isn't displayed
                    });
                    return;
                }
            }

            $scope.from = loc;
            highlightPiece($scope, loc);
        }
    }
]);


angular.module('chess').factory('myService', ["$http", "$q",
    function($http, $q) {
        // Call our ajax, construct the data
        var gameInfo = {};
        var allGames = {};

        var BASE_URL = '/chess/'
        var USER_URL = '/chess/user/' + _USERNAME + '/';

        var restCall2 = function(url, method){
            // TODO: Take in the method
            var deferred = $q.defer();
            var promise = deferred.promise;
            var config = {
                "xsrfHeaderName": "X-CSRFToken",
                "xsrfCookieName": "csrftoken"
            }

            $http.get(url, {}, config).success(function(data, status, headers, config) {
                deferred.resolve(data);
            }).error(function(data, status, headers, config) {
                deferred.reject("An error occured retriving moves");
            });
            return deferred.promise;
        };

        return {
            hotseat: function() {
                var thisService = this;
                var url = USER_URL + 'game/'
                // var deferred = $q.defer();
                // var promise = deferred.promise;
                // var config = {
                //     "xsrfHeaderName": "X-CSRFToken",
                //     "xsrfCookieName": "csrftoken"
                // }

                // $http.post(url, {}, config).success(function(data, status, headers, config) {
                //     deferred.resolve(data);
                // }).error(function(data, status, headers, config) {
                //     deferred.reject("An error occured while fetching items");
                // });
                var promise = restCall2(url, 'post');
                promise.then(function(data) {
                    thisService.gameId = data.id;
                    thisService.winner = data.winner;
                    thisService.currentPlayer = data.active_player;
            // $scope.promotablePieces = thisService.promotablePieces;

                    thisService.code = data.board_code;
                    thisService.board = data.board;
                });
                return promise;
            },
            movePiece: function(gameId, from, to) {
                var thisService = this;
                var url = USER_URL + 'game/' + gameId + '/move/' + from + '/' + to;
                var deferred = $q.defer();
                var promise = deferred.promise;
                var config = {
                    "xsrfHeaderName": "X-CSRFToken",
                    "xsrfCookieName": "csrftoken"
                }

                $http.post(url, {}, config).success(function(data, status, headers, config) {
                    deferred.resolve(data);
                }).error(function(data, status, headers, config) {
                    deferred.reject("An error occured retriving board");
                });

                promise.then(function(data) {
                    thisService.board = data.board;
                    thisService.currentPlayer = data.active_player;
                    thisService.gameId = data.id;
                    thisService.winner = data.winner;
                });
                return promise;
            },
            listMoves: function(gameId) {
                var thisService = this;
                var url = USER_URL + 'game/' + gameId + '/previous/'
                var promise = restCall2(url, 'get');

                promise.then(function(data) {
                    thisService.previousMoves = data;
                });
                return promise;
            },
            loadGame: function(gameId) {
                var thisService = this;
                var url = USER_URL + 'game/' + gameId;
                // var deferred = $q.defer();
                // var promise = deferred.promise;
                // var config = {
                //     "xsrfHeaderName": "X-CSRFToken",
                //     "xsrfCookieName": "csrftoken"
                // }

                // $http.get(url, {}, config).success(function(data, status, headers, config) {
                //     deferred.resolve(data);
                // }).error(function(data, status, headers, config) {
                //     deferred.reject("An error occured while fetching items");
                // });
                var promise = restCall2(url, 'get');
                promise.then(function(data) {
                    thisService.board = data.board;
                    thisService.currentPlayer = data.active_player;
                    thisService.gameId = data.id;
                    // thisService.code = data.board_code;
                    thisService.winner = data.winner;
                });
                return promise;
            },
            listGames: function() {
                var url = USER_URL + 'game/';
                var deferred = $q.defer();
                var thisService = this;
                $http.get(url).success(function(data, status, headers, config) {
                    var allGames = [];
                    // TODO: Move this formatting server side instead?
                    // JSON data is a bit heavy
                    for (var i = 0; i < data.length; i++) {
                        allGames.push({
                            "value": "" + data[i].id,
                            "label": "Game " + data[i].id
                        });
                    }
                    deferred.resolve(allGames);
                }).error(function(data, status, headers, config) {
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                    deferred.reject("An error occured while fetching items");
                });
                deferred.promise.then(function(allGames) {
                    thisService.allGames = allGames;
                });
                return deferred.promise;
            },
            promote: function(piece) {
                var thisService = this;
                var url = '//' + BASE_URL + '/rest/game/' + thisService.gameId + '/promote/' + piece;
                promise = restCall(url);
                promise.then(function(gameInfo) {
                    for (var key in gameInfo) {
                        thisService[key] = gameInfo[key]; //copy all the fields
                    }
                });
                return promise;
            },
            login: function(username, password){
                var url = BASE_URL + 'login/';
                var deferred = $q.defer();

                var config = {
                    "xsrfHeaderName": "X-CSRFToken",
                    "xsrfCookieName": "csrftoken"
                }

                var data = {
                    "username": username,
                    "password": password
                };

                $http.post(url, data, config).success(function(data, status, headers, config) {
                    deferred.resolve();
                }).error(function(data, status, headers, config) {
                    deferred.reject("An error occured while logging in.");
                });
                return deferred.promise;
            },
            logout: function(){
                var url = BASE_URL + 'login/';
                var deferred = $q.defer();

                var config = {
                    "xsrfHeaderName": "X-CSRFToken",
                    "xsrfCookieName": "csrftoken"
                }

                var data = {
                    "logout": true
                };

                $http.post(url, data, config).success(function(data, status, headers, config) {
                    deferred.resolve();
                }).error(function(data, status, headers, config) {
                    deferred.reject("An error occured while logging out.");
                });
                return deferred.promise;
            },
            listActivePlayers: function(){
                var url = USER_URL + 'players/';
                var promise = restCall2(url, 'get');
                var thisService = this;

                promise.then(function(data) {
                    var players = [];
                    for (var i = 0; i < data.length; i++) {
                        players.push({
                            "value": "" + data[i],
                            "label": "" + data[i]
                        });
                    }
                    thisService.activePlayers = players;
                });


                // var deferred = $q.defer();
                // var config = {
                //     "xsrfHeaderName": "X-CSRFToken",
                //     "xsrfCookieName": "csrftoken"
                // }

                // $http.get(url, {}, config).success(function(data, status, headers, config) {
                //     var players = [];
                //     for (var i = 0; i < data.length; i++) {
                //         players.push({
                //             "value": "" + data[i],
                //             "label": "" + data[i]
                //         });
                //     }
                //     deferred.resolve({"players": players});
                // }).error(function(data, status, headers, config) {
                //     deferred.reject("An error occured while retriving active players.");
                // });
                return promise;
            },
            listAgents: function(){
                var url = USER_URL + 'agents/';
                var deferred = $q.defer();
                var config = {
                    "xsrfHeaderName": "X-CSRFToken",
                    "xsrfCookieName": "csrftoken"
                }

                $http.get(url, {}, config).success(function(data, status, headers, config) {
                    var agents = [];
                    for (var i = 0; i < data.length; i++) {
                        agents.push({
                            "value": "" + data[i],
                            "label": "" + data[i]
                        });
                    }
                    deferred.resolve({"agents": agents});
                }).error(function(data, status, headers, config) {
                    deferred.reject("An error occured while retriving AI agents.");
                });
                return deferred.promise;
            }
        }
    }
]);


/*
 * Returns true if the piece in the location belongs to the current player
 */
var currentPlayerPiece = function($scope, loc){
    var square = $scope.board[loc];
    if (square  != undefined) {
        var color = square.piece.slice(0,5).toUpperCase();
        if ($scope.currentPlayer == color){
            return true;
        }
    }
    return false;
}

/*
 * Highlight a piece and the moves it can make.
 */
var highlightPiece = function($scope, loc){
    if (currentPlayerPiece($scope, loc) == false){
        // Do not highlight moves when clicking on enemy pieces
        return
    }
    $scope.highlight[loc] = 'yellow';
    $scope.from = loc;

    var moves = $scope.board[loc].moves;
    for (var i = 0; i < moves.length; i++) {
        var to = moves[i].to;
        var isAttack = moves[i].capture;
        if (isAttack) {
            $scope.highlight[to] = 'red';
        } else {
            $scope.highlight[to] = 'yellow';
        }

    }
}

/*
 * Clear all of the highlighting on the chess board squares.
 */
var clearHighlight = function($scope) {
    $scope.highlight = {};
    $scope.from = null;
    return;
}
