/**
 * Created by zhoujihao on 15-10-20.
 */

window.onload = function() {
    cc.game.onStart = function() {
        var canvas = document.getElementById("gameCanvas");

        // Cross Screen
        cc.view.setDesignResolutionSize(1500, 750, cc.ResolutionPolicy.SHOW_ALL);
        cc.view.setResolutionPolicy(cc.ResolutionPolicy.SHOW_ALL);
        cc.view.resizeWithBrowserSize(true);

        // Full Screen
        /*cc.screen.requestFullScreen(canvas);*/

        //load resources
        cc.LoaderScene.preload(g_resources, function () {
            cc.director.runScene(new StartScene());
        }, this);
    };
    cc.game.run("gameCanvas");
};
