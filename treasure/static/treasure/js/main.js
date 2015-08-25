"use strict";
// The tiles in the sprite sheet as well as our map are identical
var TILE_SIZE = 24 ;

// TODO
// * Inject the element names to startup function
// * Inject clues/images, etc to startup function
// * Shuffle clues
// * Inject canvas names to startup function (search for all
//   get element by name/id calls)
// * Enlarge the map, with more detail
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
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,3,4,0,0,0,2,3,4,9,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,3,4,0,0,0,2,3,4,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,2,3,4,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
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
            if (row[colNum] == 9) {
                return 0;
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
            return this.getItemAt(rowNum, colNum) == 0;
        },
        getTreasureItemLocations : function() {
            var locations = [];
            for (var r=0; r<map_.length; r++) {
                var row=map_[r];
                for (var c=0; c<row.length; c++) {
                    if (row[c] == 9) {
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
        if (!item) {
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
                if (dx_ == 0 && dy_ == 0) {
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

function TreasureClues(imagePreloadFn, map, clueText)
{
    var images_ = [
        {   // tiger
            img : null, 
            src : "http://drive.google.com/uc?export=view&id=0B7u1shV_Qm31aWdCNzBHbkItcm8",
            clue : 'තැඹිළි ඇඟේ මගෙ කළු ඉරි ඇත්තේ'
        },
        {   // snake
            img : null, 
            src : "http://drive.google.com/uc?export=view&id=0ByUA_i3XjaSzQ1Y0VFdWVWRRekk",
            clue : 'අත් පා නැති මා කඹයක් වගේ යි.'
        },
        {   // pig
            img : null, 
            src : "http://drive.google.com/uc?export=view&id=0B7u1shV_Qm31SjdKc3B0blNGdmM",
            clue : 'Oink! Oink! I love the mud!!'
        },
        {   // tortoise
            img : null, 
            src : "http://drive.google.com/uc?export=view&id=0ByUA_i3XjaSzdkxmQWJ1LXcwRE0",
            clue : 'I travel slowly with a shell on my back'
        },
        {   // butterfly
            img : null, 
            src : "http://drive.google.com/uc?export=view&id=0BwUXAWP3Z657dVlxM25GRTVMWXM",
            clue : 'I have colourful wings and drink nectar from flowers'
        },
        {   // lion
            img : null, 
            src : "http://drive.google.com/uc?export=view&id=0B7u1shV_Qm31QTgwVGFHTkRpdDQ",
            clue : 'I am the king of the jungle. Hear me roar!'
        },
    ];

    var currentClue_ = 0;
    var treasures_ = [];
    var locations_ = map.getTreasureItemLocations();
    var maxTreasures = (locations_.length < images_.length) ? locations_.length : images_.length;
    for (var i=0; i<maxTreasures; i++) {
        images_[i].img = imagePreloadFn(images_[i].src);
        treasures_.push({
            loc : locations_[i],
            item: images_[i]

        });
    }
    clueText.innerHTML=treasures_[0].item.clue;

    return {
        render : function (layerCtx) {
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
                        alert("Great!");
                        currentClue_++;
                        if (currentClue_ < treasures_.length) {
                            clueText.innerHTML=treasures_[currentClue_].item.clue;
                        }
                        // TODO possible end of game
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

function ImagePreloader()
{
    var images_=[];
    var loaded_ = 0;
    var doneCallback_ = null;

    function onload()
    {
        loaded_++;
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

function resetGame(params)
{
    var preloader = new ImagePreloader();

    var gm = new GameMap();
    var mapLayer = getLayerContext("mapLayer", gm);
    var heroLayer = getLayerContext("heroLayer", gm);
    var heroImage = new CharacterImage(params.assets + "img/sf2-characters.png", preloader.queuePreloadImage, heroLayer);
    var clueText = document.getElementById("clue");
    var clues = new TreasureClues(preloader.queuePreloadImage, gm, clueText);
    var mapImage = new MapImage(params.assets+"img/sf2-map.png", preloader.queuePreloadImage, mapLayer, gm);

    preloader.start(function() {
        mapImage.render(document.getElementById(params.boardElem));
        //renderMap(gm, mapLayer, document.getElementById(params.boardElem));
        clues.render(mapLayer);

        var hero = new Hero(gm, clues, heroImage);

        document.addEventListener('keydown', function(event) {
            hero.onKey(event.keyCode);
        }, false);

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
