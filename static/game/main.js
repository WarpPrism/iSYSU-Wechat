/**
 * Created by zhoujihao on 15-10-20.
 */

window.onload = function() {
    var canvas = document.getElementById("gameCanvas");
    console.log(canvas);
    console.log("Run! SYSUer!!");

    cc.game.onStart = function() {
        // Cross Screen
        cc.view.adjustViewPort(true);
        cc.view.enableAutoFullScreen(true);

       /* // 横屏模式
        cc.view.setDesignResolutionSize(1500, 750, cc.ResolutionPolicy.NO_BORDER);
        cc.view.setResolutionPolicy(cc.ResolutionPolicy.NO_BORDER);
        cc.view.resizeWithBrowserSize(true);*/

        /*// 微信竖屏解决方案
        cc.view.setDesignResolutionSize(1000, 1700, cc.ResolutionPolicy.NO_BORDER);
        cc.view.setResolutionPolicy(cc.ResolutionPolicy.NO_BORDER);
        cc.view.resizeWithBrowserSize(true);*/
        cc.view.setDesignResolutionSize(750, 1500, cc.ResolutionPolicy.NO_BORDER);
        cc.view.setResolutionPolicy(cc.ResolutionPolicy.NO_BORDER);
        cc.view.resizeWithBrowserSize(true);

        //load resources
        cc.LoaderScene.preload(g_resources, function () {
            cc.director.runScene(new BeginScene());
        }, this);
    };
    cc.game.run("gameCanvas");


};

