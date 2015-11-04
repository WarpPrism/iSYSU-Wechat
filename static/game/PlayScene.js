/**
 * Created by zhoujihao on 15-10-20.
 */

var PlayLayer = cc.Layer.extend({
    bgSprite: null,
    runnerSprite: null,
    win_size: null,
    center_pos: null,
    start_time : null,
    mission_complete: false,

    // Initial function of play layer.
    ctor: function() {
        this._super();
        // The start time of this mission.
        this.start_time = new Date().getTime();

        this.win_size = cc.winSize;
        this.center_pos = cc.p(this.win_size.width / 2, this.win_size.height / 2);

        this.addBackground();
        this.addRunner();
        this.addTouchEventListener();
        this.addTimeLabel();

        // Count Time!
        this.schedule(this.updateTime, 0.5, 100, 0);

        return true;
    },

    addBackground: function() {
        // add background of this layer
        this.bgSprite = new backgroundSprite(res.back1);
        this.bgSprite.attr({
            x: this.win_size.width + 500,
            y: this.win_size.height / 2
        });
        this.addChild(this.bgSprite, 0);
    },

    addRunner: function() {
          // add runner
        this.runnerSprite = new runnerSprite(res.runner_Ready);
        /*console.log(this.runnerSprite.texture.url);*/
        this.runnerSprite.attr({
            x: this.win_size.width / 3,
            y: 80
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
                if (x > -(2000 - target.win_size.width)) {
                    target.bgSprite.move();
                    target.runnerSprite.changeTexture();
                } else {
                    if(target.runnerSprite.move()) {
                        target.endMissionSuccessfully();
                        cc.eventManager.removeListener(this);
                    }
                    target.runnerSprite.changeTexture();
                }
                return false;
            }
        });
        cc.eventManager.addListener(this.touchListener, this);
    },

    addTimeLabel: function() {
        this.labelTime = new cc.LabelTTF("剩余时间：20 s", "Helvetica", 40);
        this.labelTime.setPosition(cc.p(this.win_size.width - 200, this.win_size.height - 50));
        this.addChild(this.labelTime, 1);
    },

    updateTime: function() {
        if (this.mission_complete) {
            return;
        }
        var now_time = new Date().getTime();
        var delta_t = Math.floor((now_time - this.start_time) / 1000);
        var remain = 20 - delta_t;
        if (remain < 0) {
            this.labelTime.setString("计时完毕");
            this.endWithTimeout();
            return;
        }
        this.labelTime.setString("剩余时间：" + remain + ' s');
    },

    endMissionSuccessfully: function() {
        this.mission_complete = true;
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
            x: this.win_size.width / 2,
            y: this.win_size.height / 2
        });

        var menu = new cc.Menu(inviteFriends);
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 2);
    },

    endWithTimeout: function() {
        this.mission_complete = false;
        var tipSprite = new cc.Sprite(res.failure1);
        tipSprite.setPosition(this.center_pos);
        this.addChild(tipSprite, 2);

        var runAgain = new cc.MenuItemImage(
            res.run_again,
            res.run_again,
            function() {
                alert("Run Again!");
                cc.director.runScene(new PlayScene());
            }, this);

        runAgain.attr({
            x: this.win_size.width / 2,
            y: this.win_size.height / 2
        });

        var menu = new cc.Menu(runAgain);
        menu.x = 0;
        menu.y = 0;
        this.addChild(menu, 2);
    }

});

var PlayScene = cc.Scene.extend({
   onEnter: function() {
       this._super();
       var layer = new PlayLayer();
       this.addChild(layer);
   }
});

