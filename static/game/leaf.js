/**
 * Created by zhoujihao on 15-10-30.
 */
var LeafSprite = cc.Sprite.extend({
    onEnter: function() {
        this._super();
    },

    onExit: function() {

    },

    addTouchEventLitener: function() {
        this.touchListener = cc.EventListener.create({
            event: cc.EventListener.TOUCH_ONE_BY_ONE,
            // When "swallow touches" is true, then returning 'true' from the onTouchBegan method will "swallow" the touch event, preventing other listeners from using it.
            swallowTouches: true,
            //onTouchBegan event callback function
            onTouchBegan: function (touch, event) {
                var pos = touch.getLocation();
                var target = event.getCurrentTarget();
                if ( cc.rectContainsPoint(target.getBoundingBox(),pos)) {
                    cc.log("touched");
                    return true;
                }
                return false;
            }
        });
        cc.eventManager.addListener(this.touchListener,this);
    }
});