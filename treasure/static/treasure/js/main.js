"use strict";
// The tiles in the sprite sheet as well as our map are identical
var TILE_SIZE = 24 ;

// TODO
// * Integrate the site CSS
// * Add scoreboard.
// * Solving the last clue should present cup with options to
//   quit or replay
// * Add loading indicator
// * Refactor assets url
// * Add django models and inject clues/image urls to game

// Constructor for the map object. It encapsulates everything related
// to the map
function GameMap()
{
    var map_ = [
        '111111111111111111111111', 
        '1........23334.........1', 
        '1.234...234*...........1', 
        '1.234...234....EF234...1', 
        '1.......234...EF..2334.1', 
        '1...*........EF...*....1', 
        '1567....EF..EF.......241', 
        '189A...EF..EF..234...241', 
        '1BCCCD..EF...233334....1', 
        '1.........*..233333334.1', 
        '1.233334.....57..*..24.1', 
        '1.233334.....8A........1', 
        '1.*..234..566CD.....24.1', 
        '1....234.599D...23334..1', 
        '1........BCD...23334...1', 
        '1....234...............1', 
        '111111111111111111111111'
    ];

    // Public interface
    return {
        rows : map_.length,
        columns : map_[0].length,
        height : map_.length * TILE_SIZE,
        width : map_[0].length * TILE_SIZE,
        getItemAt : function(rowNum, colNum) {
            if ((rowNum < 0) || (rowNum >= map_.length)) {
                return null;
            }

            var row = map_[rowNum];
            if ((colNum < 0) || (colNum >= row.length)) {
                return null;
            }

            // 9 is an treasure clue. So make that also a none
            if (row[colNum] == '*') {
                return '.';
            }
            return row[colNum];
        },
        isLocationFree : function(rowNum, colNum) {
            if ((rowNum < 0) || (rowNum >= map_.length)) {
                return false;
            }

            var row = map_[rowNum];
            if ((colNum < 0) || (colNum >= row.length)) {
                return false;
            }
            return this.getItemAt(rowNum, colNum) == '.';
        },
        getTreasureItemLocations : function() {
            var locations = [];
            for (var r=0; r<map_.length; r++) {
                var row=map_[r];
                for (var c=0; c<row.length; c++) {
                    if (row[c] == '*') {
                        locations.push({ column : c, row : r});
                    }
                }
            }
            return locations;
        }
    };
}

function MapImage(imageSource, imagePreloadFn, layerContext, map)
{
    var img_ = imagePreloadFn(imageSource);
    var ctx_ = layerContext;
    var map_ = map;

    function drawTile(row, col)
    {
        var item = map_.getItemAt(row, col);
        if (item == '.') {
            return;
        }

        // Lookup for each tile in the map. If the map references tile 1,
        // we use this table to get the tile from the sprite sheet. We
        // only store the top,left coordinates.
        var tileItems = {
            '1' : {x:24, y:0},  // wall
            '2' : {x:48, y:24}, // trees-left
            '3' : {x:0,  y:24}, // trees-mid
            '4' : {x:24, y:24}, // trees-right
            '5' : {x:0,  y:48}, // pond-left-top
            '6' : {x:24, y:48}, // pond-top
            '7' : {x:48, y:48}, // pond-right-top
            '8' : {x:0,  y:96}, // pond-left
            '9' : {x:24, y:96}, // pond-mid
            'A' : {x:48, y:96}, // pond-right
            'B' : {x:0,  y:72}, // pond-left-bottom
            'C' : {x:24, y:72}, // pond-bottom
            'D' : {x:48, y:72}, // pond-right-bottom
            'E' : {x:48, y:0}, // hills-left
            'F' : {x:72, y:0}, // hills-right
            'G' : {x:72, y:24}, // lone-tree
        };

        var tile_x = tileItems[item].x;
        var tile_y = tileItems[item].y;
        ctx_.drawImage(img_, 
                tile_x, tile_y, TILE_SIZE, TILE_SIZE, 
                col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE);
    }

    return {
        render : function(container) {
            container.style.height = map_.height + "px";
            container.style.width = map_.width + "px";
            for (var row = 0; row < map_.rows; row++) {
                for (var col = 0; col < map_.columns; col++) {
                    drawTile(row, col);
                }
            }
        }
    }
}

function CharacterImage(imageSource, imagePreloadFn, layerContext)
{
    var img = imagePreloadFn(imageSource);
    var southTiles = [0, 1];
    var westTiles = [2, 3];
    var northTiles = [4, 5];
    var eastTiles = [6, 7];
    var tileIndex = 0;
    var direction = southTiles;
    var framesPerMove = 8;
    var framesLeft = framesPerMove;
    var moving = false;
    var ctx_ = layerContext;

    img.src = imageSource;

    this.clear = function(x, y) {
        ctx_.clearRect(x, y, TILE_SIZE, TILE_SIZE);
    };

    this.render = function(x, y) {
        var tile_x = TILE_SIZE * direction[tileIndex];
        ctx_.drawImage(img, tile_x, 0, TILE_SIZE, TILE_SIZE, 
                x, y, TILE_SIZE, TILE_SIZE);

        framesLeft--;
        if (!framesLeft) {
            framesLeft = framesPerMove;

            if (moving) {
                tileIndex = (tileIndex + 1) % northTiles.length;
            }
        }
    };

    this.faceNorth = function() {
        direction = northTiles;
    };

    this.faceSouth = function() {
        direction = southTiles;
    };

    this.faceWest = function() {
        direction = westTiles;
    };

    this.faceEast = function() {
        direction = eastTiles;
    };

    this.stopMovement = function() {
        moving = false;
    };

    this.startMovement = function() {
        moving = true;
    };
}

function sign(value)
{
    if (!value) {
        return 0;
    }
    return (value > 0) ? 1 : -1;
}

function Hero(gameMap, clues, image)
{
    var gameMap_ = gameMap;
    var img = image;
    var row_ = 1;
    var col_ = 1;
    var dRow_ = 0;
    var dCol_ = 0;
    var dx_ = 0;
    var dy_ = 0;
    var ticksLeft_ = 0;
    var ticksPerMove_ = 1;
    var clues_ = clues;
    // Queued actions are performed when the character has finished
    // moving into a square
    var queuedAction = null;

    this.onFrameUpdate = function() {
        this.render();
    };

    this.render = function() {
        var x = (col_ * TILE_SIZE) + dx_;
        var y = (row_ * TILE_SIZE) + dy_;
        img.clear(x, y);

        // Check if we've finished moving between tiles (or stationary)
        if (!dx_ && !dy_ ) {
            // Perform any queued actions
            if (queuedAction) {
                queuedAction();
                queuedAction = null;
            }
            // Check if we should be moving
            if (dRow_ || dCol_) {
                // Start moving if possible
                if (gameMap.isLocationFree(row_ + dRow_, col_ + dCol_)) {
                    row_ = row_ + dRow_;
                    col_ = col_ + dCol_;
                    dx_ = -(dCol_ * TILE_SIZE);
                    dy_ = -(dRow_ * TILE_SIZE);
                } else {
                    img.stopMovement();
                    dRow_ = 0;
                    dCol_ = 0;
                }
            }
        }

        // Update the position of the character image
        if (ticksLeft_) {
            ticksLeft_--;
        }
        if (!ticksLeft_) {
            ticksLeft_ = ticksPerMove_;
            dx_ -= sign(dx_);
            dy_ -= sign(dy_);
        }

        x = (col_ * TILE_SIZE) + dx_;
        y = (row_ * TILE_SIZE) + dy_;
        img.render(x, y);
    };

    this.onKey = function(keyCode) {
        switch(keyCode) {
            case 38:
                queuedAction = function() {
                    img.faceNorth();
                    img.startMovement();
                    dRow_ = -1;
                    dCol_ = 0;
                }
                break;
            case 40:
                queuedAction = function() {
                    img.faceSouth();
                    img.startMovement();
                    dRow_ = 1;
                    dCol_ = 0;
                }
                break;
            case 37:
                queuedAction = function() {
                    img.faceWest();
                    img.startMovement();
                    dRow_ = 0;
                    dCol_ = -1;
                }
                break;
            case 39:
                queuedAction = function() {
                    img.faceEast();
                    img.startMovement();
                    dRow_ = 0;
                    dCol_ = 1;
                }
                break;
            case 190:   // .
                queuedAction = function() {
                    img.stopMovement();
                    dRow_ = 0;
                    dCol_ = 0;
                }
                break;
            case 32:    // Space
            case 13:    // Enter
                queuedAction = function() {
                    img.stopMovement();
                    dRow_ = 0;
                    dCol_ = 0;
                    clues_.checkClue(row_, col_);
                }
                break;
            default:
                break;
        }
    };
}

// event.type must be keypress
function getChar(event) {
    if (event.which == null) {
        return String.fromCharCode(event.keyCode) // IE
    } else if (event.which!=0 && event.charCode!=0) {
        return String.fromCharCode(event.which)   // the rest
    } else {
        return null // special key
    }
}

function shuffle(items)
{
    for (var i=0; i<items.length; i++) {
        var swapWith = Math.floor(Math.random() * items.length);
        var tmp = items[i];
        items[i] = items[swapWith];
        items[swapWith] = tmp;
    }
    return items;
}

function TreasureClues(imagePreloadFn, map, clues, clueText, keyListener)
{
    var clues_ = clues;
    var currentClue_ = 0;
    var treasures_ = [];
    var locations_ = map.getTreasureItemLocations();
    var maxTreasures = (locations_.length < clues_.length) ? locations_.length : clues_.length;

    for (var i=0; i<maxTreasures; i++) {
        clues_[i].img = imagePreloadFn(clues_[i].src);
        treasures_.push({
            loc : locations_[i],
            item: clues_[i]

        });
    }
    treasures_ = shuffle(treasures_);

    return {
        render : function (layerCtx) {
            clueText.innerHTML=treasures_[0].item.clue;
            for (var i=0; i<treasures_.length; i++) {
                var x = treasures_[i].loc.column * TILE_SIZE;
                var y = treasures_[i].loc.row * TILE_SIZE;
                var img = treasures_[i].item.img;

                layerCtx.drawImage(img, x, y,
                        TILE_SIZE * 3, TILE_SIZE *3);
            }
        }, 

        checkClue : function(row, column) {
            if (currentClue_ >= treasures_.length) {
                return ;
            }

            var loc = treasures_[currentClue_].loc;
            if ((column >= loc.column) && (column < (loc.column + 3))
                    && (row >= loc.row) && (row < loc.row + 3)) {
                        keyListener.disable();
                        alertify.alert("Great!", function() {
                            keyListener.enable();
                        });
                        currentClue_++;
                if (currentClue_ < treasures_.length) {
                    clueText.innerHTML=treasures_[currentClue_].item.clue;
                }
               // TODO possible end of game
            } else {
                alertify.error("Wrong. Try again");
            }
        }
    };
}

function getLayerContext(canvasName, gameMap) 
{
    function initCanvas(canvas, gm)
    {
        canvas.setAttribute('width', gm.width);
        canvas.setAttribute('height', gm.height);
    }

    var canvas = document.getElementById(canvasName);
    initCanvas(canvas, gameMap);
    return canvas.getContext("2d");
}

function ImagePreloader(progress)
{
    var images_=[];
    var loaded_ = 0;
    var doneCallback_ = null;

    function onload()
    {
        loaded_++;
        progress.value = loaded_;
        if (loaded_ >= images_.length) {
            if (doneCallback_) {
                doneCallback_();
            }
        }
    }

    // Public interface
    return {
        // This function can be called by those who
        // need to preload images
        queuePreloadImage : function(imageSource) {
            var item = { img : new Image(), src : imageSource };
            images_.push(item);
            progress.max = images_.length;

            return item.img;
        },
        // Begin the process of preloading images. Invoke callback
        // when done
        start : function(doneCallback) {
            doneCallback_ = doneCallback;
            for (var i=0; i<images_.length; i++) {
                var item = images_[i];
                item.img.onload = onload;
                item.img.src = item.src;
            }
        }
    };
}

function KeyListener()
{
    var observer_ = null;
    var eventEnabled = false;

    function handler(event) {
        if (observer_) {
            if (eventEnabled) {
                observer_.onKey(event.keyCode);
            }
        }
    }

    document.addEventListener('keydown', handler, false);

    return {
        registerObserver(observer) {
            observer_ = observer;
        },

        enable : function() {
            eventEnabled = true;
        },

        disable : function() {
            eventEnabled = false;
        }
    };
}

function gameStart(params)
{
    var preloader = new ImagePreloader(document.getElementById(params.progressElem));

    var gm = new GameMap();
    var mapLayer = getLayerContext(params.mapLayerElem, gm);
    var heroLayer = getLayerContext(params.characterLayerElem, gm);
    var heroImage = new CharacterImage(params.assets + "img/sf2-characters.png", 
            preloader.queuePreloadImage, 
            heroLayer);
    var clueText = document.getElementById(params.clueTextElem);
    var mapImage = new MapImage(params.assets + "img/sf2-map.png",
            preloader.queuePreloadImage,
            mapLayer, gm);

    var keyListener = new KeyListener();
    var clues = new TreasureClues(preloader.queuePreloadImage, 
            gm, params.clues, clueText, keyListener);

    preloader.start(function() {
        mapImage.render(document.getElementById(params.boardElem));
        clues.render(mapLayer);
        var hero = new Hero(gm, clues, heroImage);

        keyListener.registerObserver(hero);
        keyListener.enable();
        function gameLoop()
    {
        var fps = 40;
        setTimeout(function() {
            window.requestAnimationFrame(gameLoop);
            hero.onFrameUpdate();
        }, 1000 / fps);
    }

    gameLoop();
    });
}
