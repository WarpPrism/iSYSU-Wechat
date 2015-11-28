/**
 * Created by zhoujihao on 15-10-20.
 */

var PlayLayer1 = cc.Layer.extend({
    bgSprite: null,
    runnerSprite: null,
    win_size: null,
    center_pos: null,
    start_time : null,
    mission_complete: false,
    request_time: 20,

    // Initial function of play layer.
    ctor: function() {
        this._super();

        this.win_size = cc.winSize;
        this.center_pos = cc.p(this.win_size.width / 2, this.win_size.height / 2);
        console.log(this.win_size.width, this.win_size.height);

        this.addBackground();
        this.addRunner();
        this.addTimeLabel();

        this.ready_go = new cc.LabelTTF("Ready?", "Symbol", 120);
        this.ready_go.setColor(cc.color(255,120,0));
        this.ready_go.setPosition(cc.p(this.win_size.width / 2, this.win_size.height / 2));
        this.addChild(this.ready_go, 1);

        this.mission_info = new cc.LabelTTF("第一关", "Symbol", 40);
        this.mission_info.setColor(cc.color(255,120,0));
        this.mission_info.setPosition(cc.p(-150, this.win_size.height/2 + 300));
        this.addChild(this.mission_info, 1);


        // Closure ??!!
        var layer = this;
        setTimeout(function () {
            layer.ready_go.setString("Go!");

            // Count Time! Game Start!
            // The start time of this mission.
            layer.start_time = new Date().getTime();
            layer.schedule(layer.updateTime, 0.5, 50, 0);
            layer.addTouchEventListener();
        }, 1000);
        setTimeout(function () {
            layer.ready_go.setString("");
        }, 1500);

        return true;
    },

    addBackground: function() {
        // add background of this layer
        this.bgSprite = new backgroundSprite(res.mission1);
        this.bgSprite.attr({
            x: this.win_size.width  + 950,
            y: this.win_size.height / 2
        });
        this.addChild(this.bgSprite, 0);
    },

    addRunner: function() {
          // add runner
        this.runnerSprite = new runnerSprite(res.runner_Ready);
        /*console.log(this.runnerSprite.texture.url);*/
        this.runnerSprite.attr({
            x: 0,
            y: this.win_size.height / 4 + 100
        });
        this.addChild(this.runnerSprite, 1);
    },

    addTouchEventListener: function() {
        this.touchListener = cc.EventListener.create({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            // When "swallow touches" is true, then returning 'true' from the onTouchBegan
            // method will "swallow" the touch event, preventing other listeners from using it.
            swallowTouches: true,
            //onTouchBegan event callback function
            onTouchBegan: function(touch, event) {
                /*var pos = touch.getLocation();*/
                var target = event.getCurrentTarget();
                var x = target.bgSprite._position.x;
                /*console.log(x);*/
                if (x > -900) {
                    target.bgSprite.move();
                    target.runnerSprite.changeTexture();
                } else {
                    if(target.runnerSprite.move()) {
                        target.endMissionSuccessfully();
                    }
                    target.runnerSprite.changeTexture();
                }
                return false;
            }
        });
        cc.eventManager.addListener(this.touchListener, this);
    },

    addTimeLabel: function() {
        this.labelTime = new cc.LabelTTF("剩余时间：" + this.request_time + " s", "Symbol", 40);
        this.labelTime.setColor(cc.color(255,120,0));
        this.labelTime.setPosition(cc.p(this.win_size.width / 2 + 400, this.win_size.height / 2 + 300));
        this.addChild(this.labelTime, 1);
    },

    updateTime: function() {

        if (this.mission_complete) {
            return;
        }
        var now_time = new Date().getTime();
        var delta_t = Math.floor((now_time - this.start_time) / 1000);
        var remain = this.request_time - delta_t;
        if (remain <= 0) {
            this.labelTime.setString("计时完毕");
            this.endWithTimeout();
            return;
        }
        this.labelTime.setString("剩余时间：" + remain + ' s');
    },

    endMissionSuccessfully: function() {
        // send info to server
        $.post(
            "/winGame",
            {mission_id: server_data.mission_id, open_id: server_data.open_id},
            function(res){
                console.log(res);
            }
        );
        this.mission_complete = true;
        cc.eventManager.removeListener(this.touchListener);
        var tipSprite = new cc.Sprite(res.success1);
        tipSprite.setPosition(this.center_pos);
        this.addChild(tipSprite, 2);

        var inviteFriends = new cc.MenuItemImage(
            res.invite_friends,
            res.invite_friends,
            function() {
                alert("Invite Friends!");
            }, this);

        inviteFriends.attr({
            x: this.win_size.width / 2 - 120,
            y: this.win_size.height / 2 - 230
        });

        var run_again = new cc.MenuItemImage(
            res.run_again_small,
            res.run_again_small,
            function() {
                cc.director.runScene(new BeginScene());
            }, this);

        run_again.attr({
            x: this.win_size.width / 2 + 120,
            y: this.win_size.height / 2 - 230
        });

        var menu = new cc.Menu(run_again, inviteFriends);
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 2);
    },

    endWithTimeout: function() {
        cc.eventManager.removeListener(this.touchListener);
        this.mission_complete = false;
        var tipSprite = new cc.Sprite(res.failure1);
        tipSprite.setPosition(this.center_pos);
        this.addChild(tipSprite, 2);

        var runAgain = new cc.MenuItemImage(
            res.run_again,
            res.run_again,
            function() {
                cc.director.runScene(new BeginScene());
            }, this);

        runAgain.attr({
            x: this.win_size.width / 2,
            y: this.win_size.height / 2 - 200
        });

        var menu = new cc.Menu(runAgain, getCloseLabel(this.win_size));
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 2);
    }

});

var getCloseLabel = function(size) {
    this.item = new cc.MenuItemImage(
            res.close,
            res.close,
            function () {
                cc.director.runScene(new BeginScene());
            }, this);
    this.item.attr({
            x: size.width*3/4-58,
            y: size.height - 90 ,
            anchorX: 0.5,
            anchorY: 0.5
        });
    return this.item;
};

var Mission1 = cc.Scene.extend({
   onEnter: function() {
       this._super();
       var layer = new PlayLayer1();
       // change landscape to portrait.
       layer.rotation = 90;
       this.addChild(layer);
   }
});

