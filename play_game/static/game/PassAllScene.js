/**
 * Created by zhoujihao on 15-11-28.
 */
/**
 * Created by zhoujihao on 15-11-28.
 */
var PassAllLayer = cc.Layer.extend({
    ctor: function() {
        this._super();

        var size = cc.winSize;

        this.bgSprite = new cc.Sprite(res.begin_bg);
        this.bgSprite.attr({
            x: size.width / 2,
            y: size.height / 2
        });
        this.addChild(this.bgSprite, 0);
        var menu = new cc.Menu(getPassLabel(size));
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 2);

        return true;
    }
});


var getPassLabel = function(size) {
    this.item = new cc.MenuItemImage(
            res.pass,
            res.pass,
            function () {
                /*cc.director.runScene(new RuleScene());*/
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height / 2
        });
    return this.item;
};

var getCloseLabel = function(size) {
    this.item = new cc.MenuItemImage(
            res.close,
            res.close,
            function () {
                cc.director.runScene(new BeginScene());
            }, this);
    this.item.attr({
            x: size.width / 1.08,
            y: size.height / 1.39,
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};



var PassAllScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var layer = new PassAllLayer();

        layer.rotation = 90;

        this.addChild(layer);

        /*cc.audioEngine.playMusic(res.backgroundMP3, true);*/

        this.scheduleUpdate();
    }
});
