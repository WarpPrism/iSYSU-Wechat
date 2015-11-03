/**
 * Created by zhoujihao on 15-10-20.
 */

window.onload = function() {
    cc.game.onStart = function() {
        // cc.view.setDesignResolutionSize(480, 320, cc.ResolutionPolicy.SHOW_ALL);
        cc.view.resizeWithBrowserSize(true);
        //load resources
        cc.LoaderScene.preload(g_resources, function () {
            cc.director.runScene(new StartScene());
        }, this);
    };
    cc.game.run("gameCanvas");
};
