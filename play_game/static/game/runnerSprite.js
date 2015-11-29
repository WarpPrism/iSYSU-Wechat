/**
 * Created by zhoujihao on 15-10-31.
 */

var runnerSprite = cc.Sprite.extend({
    jump: 0,
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

        // And Jump
        if (this.jump == 0) {
            this.runAction(new cc.moveBy(0.05, 0, 20));
            cc.audioEngine.playEffect(res.jumpMP3);
            this.jump = 1;
        } else {
            this.runAction(new cc.moveBy(0.05, 3, -20));
            this.jump = 0;
        }

    },

    move: function() {
        /*console.log(this._position);*/
        if (this._position.x >= 593) {
            return true;
        } else {
            this.runAction(new cc.moveBy(0.2, 50, 0));
            return false;
        }
    }
});