/**
 * @Author: liaominghao
 * @Date: 2015-11-04
 */

var RuleLayer = cc.Layer.extend({
    ctor: function() {
        this._super();

        var size = cc.winSize;

        this.bgSprite = new cc.Sprite(res.begin_bg);
        this.bgSprite.attr({
            x: size.width / 2,
            y: size.height / 2
        });
        this.addChild(this.bgSprite, 0);

        var menu = new cc.Menu(getBigLabelOfRule(size), getKnowLabel(size), getCloseLabel(size));
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 1);

        return true;
    }
});

var getKnowLabel = function(size) {
    this.item = new cc.MenuItemImage(
            res.rule_know,
            res.rule_know,
            function () {
                cc.director.runScene(new BeginScene());
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height / 4,
            anchorX: 0.5,
            anchorY: 0.5
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
            x: size.width*3/4-58,
            y: size.height-48 ,
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};

var getBigLabelOfRule = function(size) {
    this.item = new cc.MenuItemImage(
            res.rule_label,
            res.rule_label,
            function () {
                //cc.director.runScene(new RuleScene());
            }, this);
    this.item.attr({
            x: size.width / 2,
            y: size.height/2+5,
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};



var RuleScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var layer = new RuleLayer();
        this.addChild(layer);
    }
});
