/**
 * Created by zhoujihao on 15-10-20.
 */

var StartLayer = cc.Layer.extend({
    ctor: function() {
        this._super();

        var size = cc.winSize;

        /*var helloLabel = new cc.LabelTTF("Hello World", " ", 38);
        helloLabel.x = size.width / 2;
        helloLabel.y = size.Height / 2;
        this.addChild(helloLabel);*/

        this.bgSprite = new cc.Sprite(res.back1);
        this.bgSprite.attr({
            x: size.width / 2,
            y: size.height / 2
        });
        this.addChild(this.bgSprite, 0);

        var startItem = new cc.MenuItemImage(
            res.Start_png,
            res.Start_png,
            function () {
                cc.director.runScene(new PlayScene());
            }, this);

        startItem.attr({
            x: size.width / 2 + 300,
            y: size.height / 4,
            anchorX: 0.5,
            anchorY: 0.5
        });

        var menu = new cc.Menu(startItem);
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 1);

        return true;
    }
});

var StartScene = cc.Scene.extend({
    onEnter: function() {
        this._super();
        var layer = new StartLayer();
        this.addChild(layer);
    }
});
