/**
 * Created by zhoujihao on 15-10-20.
 */

var PlayLayer = cc.Layer.extend({
    bgSprite:null,
    leafSprites: null,
    ctor: function() {
        this._super();
        this.leafSprites = [];
        var size = cc.winSize;


        // add bg
        this.bgSprite = new cc.Sprite(res.BackGround_png);
        this.bgSprite.attr({
            x: size.width / 2,
            y: size.height / 2
            // rotation: 180
        });
        this.addChild(this.bgSprite, 0);

        // 设置定时器,
        this.schedule(this.update,1,16*1024,1);
        return true;
    },

    addLeaf: function() {
        var leaf = new cc.Sprite(res.Leaf_png);
        var size = cc.winSize;

        var x = leaf.width/2+size.width/2*cc.random0To1();

        leaf.attr({
            x: x,
            y: size.height - 30,
            scale: 0.5
        });

        var dropAction = cc.MoveTo.create(4, cc.p(leaf.x,-30));
        leaf.runAction(dropAction);

        this.addChild(leaf, 5);

        this.leafSprites.push(leaf);
    },

    removeLeaf : function() {
        //移除到屏幕底部的leaf
        for (var i = 0; i < this.leafSprites.length; i++) {
            cc.log("removeSushi.........");
            if(0 == this.leafSprites[i].y) {
                cc.log("==============remove:"+i);
                this.leafSprites[i].removeFromParent();
                this.leafSprites[i] = undefined;
                this.leafSprites.splice(i,1);
                i= i-1;
            }
        }
    },

    update: function() {
        this.addLeaf();
        this.removeLeaf();
    }

});

var PlayScene = cc.Scene.extend({
   onEnter: function() {
       this._super();
       var layer = new PlayLayer();

       this.addChild(layer);
   }
});
