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
                cc.director.runScene(new Mission4());
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height / 4+200,
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
            y: size.height / 4 + 50 ,
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
                cc.director.runScene(new RuleScene());
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height*(3/4),
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};



var BeginScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var layer = new BeginLayer();
        this.addChild(layer);
    }
});
