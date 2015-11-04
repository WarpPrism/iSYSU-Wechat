/**
 * Created by zhoujihao on 15-10-31.
 */

var runnerSprite = cc.Sprite.extend({
    onEnter: function() {
        this._super();
    },

    onExit: function() {

    },

    changeTexture: function() {
        /*console.log(this.texture.url);*/
        // Animation??
        /*var animation = new cc.Animation();
        for ( var i = 1; i < 3; i ++ ) {
            var frameName = "static/res/game/runner_Run_" + i + ".png" ;
            animation.addSpriteFrameWithFile ( frameName ) ;
        }

        animation.setDelayPerUnit ( 2.8 / 14 ) ;
        animation.setRestoreOriginalFrame ( true ) ;
        var action = new cc.Animate ( animation ) ;
        this.runAction ( new cc.Sequence( action, action.reverse ( ) ) ) ;*/

        var texture;
        // console.log(this.getTexture());
        if (this.getTexture().url == res.runner_Ready) {
            texture = res.runner_Run1;
        }
        if (this.getTexture().url == res.runner_Run1) {
            texture = res.runner_Run2;
        }
        if (this.getTexture().url == res.runner_Run2) {
            texture = res.runner_Run3;
        }
        if (this.getTexture().url == res.runner_Run3) {
            texture = res.runner_Ready;
        }
        this.setTexture(texture);

    },

    move: function() {
        /*console.log(this._position);*/
        if (this._position.x >= 1070) {
            return true;
        } else {
            this.runAction(new cc.moveBy(0.1, 30, 0));
            return false;
        }
    }
});