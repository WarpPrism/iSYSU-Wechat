/**
 * Created by zhoujihao on 15-11-4.
 */

var backgroundSprite = cc.Sprite.extend({
    onEnter: function() {
        this._super();
    },

    onExit: function() {},

    move: function() {
        this.runAction(new cc.moveBy(0.1, -50/*-1000*/, 0));
    }
});