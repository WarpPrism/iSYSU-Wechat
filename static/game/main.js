/**
 * Created by zhoujihao on 15-10-20.
 */

window.onload = function() {
    var canvas = document.getElementById("gameCanvas");
    /*alert(window.orientation);
    if (window.orientation == 0) {
        /!*canvas.addClass('rotate');*!/
    }*/
    cc.game.onStart = function() {
        // Cross Screen
        cc.view.setDesignResolutionSize(1500, 750, cc.ResolutionPolicy.NO_BORDER);
        cc.view.setResolutionPolicy(cc.ResolutionPolicy.NO_BORDER);
        cc.view.resizeWithBrowserSize(true);

        // Full Screen
        /*cc.screen.requestFullScreen(canvas);*/
        cc.view.enableAutoFullScreen(true)

        //load resources
        cc.LoaderScene.preload(g_resources, function () {
            cc.director.runScene(new BeginScene());
        }, this);
    };
    cc.game.run("gameCanvas");


};
