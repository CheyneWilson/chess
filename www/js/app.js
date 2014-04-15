var app = angular.module('chess', ['ngAnimate', 'ngSanitize', 'mgcrea.ngStrap']);

app.controller('MainCtrl', function($scope) {});


'use strict';


angular.module('chess').controller('ChangeGame', ["$rootScope", "$scope", "$select", "myService",
    function($rootScope, $scope, $select, myService) {
        var reloadGameList = function(selectNew) {
            myService.listGames().then(function() {
                $scope.icons = myService.allGames;
                if (selectNew == true) {
                    item = $scope.icons[$scope.icons.length - 1];
                    $scope.selected = item.value;
                    $scope.selectedIcon = item.value;
                }
            });
        };

        $rootScope.$on('chess.newGame', function() {
            reloadGameList(true);
        });

        $scope.$on('$select.select', function(event, value, index) {
            gameId = value;
            promise = myService.loadGame(gameId);
            promise.then(function() {
                $rootScope.$emit('chess.gameLoaded');
            });
        });

        reloadGameList();
    }
]);

/* This controller supports the modals for new game */
angular.module("chess").controller("NewGameOptions", ["$rootScope", "$scope", "$http", "$modal", "myService",
    function($rootScope, $scope, $http, $modal, myService) {
        $scope.hotSeatGame = function(modal) {
            myService.newGame('HotSeat').then(function() {
                    modal.$hide();
                    $rootScope.$emit('chess.newGame');
                },
                function(errorMessage) {
                    $scope.error = errorMessage; // TODO: This isn't displayed
                });
        };
        $scope.onlineGame = function(modal) {
            myService.newGame('Online').then(function() {
                    modal.$hide();
                    $rootScope.$emit('chess.newGame');
                },
                function(errorMessage) {
                    $scope.error = errorMessage; // TODO: This isn't displayed
                });
        };
        $scope.randomAiGame = function(modal) {
            myService.newGame('RandomAI').then(function() {
                    modal.$hide();
                    $rootScope.$emit('chess.newGame');
                },
                function(errorMessage) {
                    $scope.error = errorMessage; // TODO: This isn't displayed
                });
        };
    }
]);

angular.module("chess").controller("DrawBoard", ["$rootScope", "$scope", "$http", "myService",
    function($rootScope, $scope, $http, myService) {

        var reloadBoard = function() {
            $scope.gameId = myService.gameId;
            $scope.board = myService.board;
            $scope.winner = myService.winner;
            $scope.currentPlayer = myService.currentPlayer;
            $scope.promotablePieces = myService.promotablePieces;
            $scope.moves = myService.moves;
            $scope.code = myService.code;
        };

        $rootScope.$on('chess.boardChanged', reloadBoard);
        $rootScope.$on('chess.newGame', reloadBoard);
        $rootScope.$on('chess.gameLoaded', reloadBoard);


        $scope.promote = function(piece) {
            promise = myService.promote(piece);
            promise.then(function() {
                $rootScope.$emit('chess.boardChanged');
            });
        };

        /*
         * This function highlights all the moves the selected piece can make.
         * It clears the highlighting on previously highlighted squares
         * It is attached to each piece
         */
        $scope.highlightMoves = function(x, y) {
            $scope.x = x;
            $scope.y = y;

            // We already have a piece highlighed, try and move it to the location chosen
            if ($scope.from) {

                toSquare = $scope.board[y][x];
                if (toSquare.highlight || toSquare.attack) {
                    // pass
                } else {
                    // cannot move to square we are not allowed to attack/move to
                    clearHighlight($scope);
                    $scope.from = null;
                    return;
                }

                to = reverseTranslateMove(x, y);
                promise = myService.movePiece($scope.from, to);

                promise.then(function(data) {
                        // $scope.board = myService.board;
                        //$rootScope.$emit('chess.moveTaken');
                        $rootScope.$emit('chess.boardChanged');
                    },
                    function(errorMessage) {
                        $scope.error = errorMessage; // TODO: This isn't displayed
                    });
                // movePiece($scope, $http);
            }

            clearHighlight($scope);

            // Unset selected square, and if the user clicks the previously selected square directly then
            // Returns instead of re-selecting it and re-highlighting
            if ($scope.from != null) {
                if ($scope.from.x == x && $scope.from.y == y) {
                    $scope.from = null;
                    return;
                } else {
                    $scope.from = null;
                }
            }

            // We can only select 'our' pieces
            // Hacky as hackness, checking first piece has the same letter
            if ($scope.board[y][x].piece[0] != $scope.currentPlayer.toUpperCase()[0]) {
                // Not out piece
                return;
            }
            selectSquare($scope);

            moves = $scope.board[y][x].moves;
            for (i = 0; i < moves.length; i++) {
                p = translateMove(moves[i])
                $scope.board[p.y][p.x].highlight = true;
            }

            attacks = $scope.board[y][x].attacks;
            for (i = 0; i < attacks.length; i++) {
                p = translateMove(attacks[i])
                $scope.board[p.y][p.x].attack = true;
            }
        };
    }
]);


angular.module('chess').factory('myService', ["$http", "$q",
    function($http, $q) {
        // Call our ajax, construct the data
        gameInfo = {};
        allGames = {};

        /*
         * Makes a rest call to the URL specified.
         * Formats the response (mainly the board, from being a sparse array, to a full 8x8 array)
         * so that it can be displayed via angular.
         *
         * Designed to work with:
         * /rest/new
         * /rest/game
         * /rest/move
         * /rest/promote
         *
         */
        var restCall = function(url) {
            var deferred = $q.defer();
            $http.get(url).success(function(data, status, headers, config) {
                var gameInfo = formatResponse(data);
                deferred.resolve(gameInfo);
            }).error(function(data, status, headers, config) {
                deferred.reject("An error occured while fetching items");
            });
            return deferred.promise;
        };

        return {
            // gameInfo: {},
            newGame: function(gameType) {
                var thisService = this;
                var url = '//www.chess.dev/rest/new/' + gameType;
                promise = restCall(url);
                promise.then(function(gameInfo) {
                    for (var key in gameInfo) {
                        thisService[key] = gameInfo[key]; //copy all the fields
                    }
                });
                return promise;
            },
            movePiece: function(from, to) {
                var thisService = this;
                var url = '//www.chess.dev/rest/game/' + thisService.gameId + '/from/' + from + '/to/' + to;
                promise = restCall(url);
                promise.then(function(gameInfo) {
                    for (var key in gameInfo) {
                        thisService[key] = gameInfo[key]; //copy all the fields
                    }
                });
                return promise;
            },
            loadGame: function(gameId) {
                var thisService = this;
                var url = '//www.chess.dev/rest/game/' + gameId;
                promise = restCall(url);
                promise.then(function(gameInfo) {
                    for (var key in gameInfo) {
                        thisService[key] = gameInfo[key]; //copy all the fields
                    }
                });
                return promise;
            },
            listGames: function() {
                var url = '//www.chess.dev/rest/list';
                var deferred = $q.defer();
                var thisService = this;
                $http.get(url).success(function(data, status, headers, config) {
                    allGames = [];
                    // TODO: Move this formatting server side instead?
                    // JSON data is a bit heavy
                    for (i = 0; i < data.length; i++) {
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
                var url = '//www.chess.dev/rest/game/' + thisService.gameId + '/promote/' + piece;
                promise = restCall(url);
                promise.then(function(gameInfo) {
                    for (var key in gameInfo) {
                        thisService[key] = gameInfo[key]; //copy all the fields
                    }
                });
                return promise;
            }
        }
    }
]);


/*
  Clear all of the highlighting on the chess board squares.
  Used for display only.
*/
var clearHighlight = function($scope) {
    for (y = 0; y < 8; y++) {
        for (x = 0; x < 8; x++) {
            $scope.board[y][x].highlight = false;
            $scope.board[y][x].attack = false;
            $scope.board[y][x].selected = false;
        }
    }
}

var reverseTranslateMove = function(x, y) {
    x_char = 'ABCDEFGH';
    loc = x_char.charAt(x) + (y + 1);
    return loc;
}

/* Translates move from B6 notation to a object with x and y */
var translateMove = function(loc) {
    point = {};
    point.x = loc.toUpperCase().charCodeAt(0) - "A".charCodeAt(0);
    point.y = loc.charAt(1) - 1;
    return point;
}

/*
 * Highlight the selected square (display), and update the model
 */
var selectSquare = function($scope) {
    $scope.board[$scope.y][$scope.x].selected = true;
    $scope.from = $scope.board[$scope.y][$scope.x].position
}

var formatResponse = function(data) {
    // Format board
    board = []
    for (y = 0; y < 8; y++) {
        board[y] = []
        for (x = 0; x < 8; x++) {
            loc = reverseTranslateMove(x, y);
            if (data.board[loc]) {
                board[y][x] = data.board[loc];
            } else {
                board[y][x] = {
                    "attacks": [],
                    "position": loc,
                    "piece": "empty",
                    "moves": [],
                    "active": false
                }
            }
        }
    }
    gameInfo = {};
    gameInfo.board = board;

    //format moves
    moves = []
    for (i = 0; i < data.moves.length; i++) {
        moves.push({
            "value": data.moves[i]
        })
    }
    gameInfo.gameId = data.game_id;
    gameInfo.code = data.board_serialized;
    gameInfo.turn = data.turn;
    gameInfo.winner = data.winner;
    gameInfo.promotablePieces = data.promotable_pieces;
    gameInfo.moves = moves;
    gameInfo.currentPlayer = data.player;

    return gameInfo
}
