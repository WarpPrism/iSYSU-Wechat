/**
 * @Author: liaominghao
 * @Date: 2015-11-04
 */

var BeginLayer = cc.Layer.extend({
    ctor: function() {
        this._super();

        var size = cc.winSize;

        this.bgSprite = new cc.Sprite(res.begin_bg);
        this.bgSprite.attr({
            x: size.width / 2,
            y: size.height / 2
        });
        this.addChild(this.bgSprite, 0);

        //var menu = new cc.Menu(getEnterLabel(size));
        var menu = new cc.Menu(getBigLabelOfBegin(size), getRuleLabel(size), getEnterLabel(size));
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 1);

        return true;
    }
});

var getEnterLabel = function(size) {
    this.item = new cc.MenuItemImage(
            res.begin_enter,
            res.begin_enter,
            function () {
                // Select Mission
                var mission = null;
                switch (server_data.mission_id) {
                    case '0':
                        // The Player has passed all missions!
                        cc.director.runScene(new PassAllScene());
                        break;
                    case '1':
                        mission = new Mission1();
                        break;
                    case '2':
                        mission = new Mission2();
                        break;
                    case '3':
                        mission = new Mission3();
                        break;
                    case '4':
                        mission = new Mission4();
                        break;
                    default:
                        break;
                }
                cc.director.runScene(new PassAllScene());
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height / 4 + 300,
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};

var getRuleLabel = function(size) {
    this.item = new cc.MenuItemImage(
            res.begin_rules,
            res.begin_rules,
            function () {
                cc.director.runScene(new RuleScene());
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height / 4 + 150 ,
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};

var getBigLabelOfBegin = function(size) {
    this.item = new cc.MenuItemImage(
            res.begin_label,
            res.begin_label,
            function () {
                /*cc.director.runScene(new RuleScene());*/
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height*(2/3) - 50
        });
    return this.item;
};



var BeginScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var layer = new BeginLayer();

        layer.rotation = 90;

        this.addChild(layer);

        /*cc.audioEngine.playMusic(res.backgroundMP3, true);*/

        this.scheduleUpdate();
    }
});
