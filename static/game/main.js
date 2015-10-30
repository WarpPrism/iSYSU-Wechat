/**
 * Created by zhoujihao on 15-10-20.
 */

window.onload = function() {
    cc.game.onStart = function() {
        //load resources
        cc.LoaderScene.preload(["{{static_url('res/game/HelloWorld.png')}}"], function () {
            cc.director.runScene(new StartScene());
        }, this);
    };
    cc.game.run("gameCanvas");
};
