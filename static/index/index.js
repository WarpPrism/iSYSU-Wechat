/**
 * Created by zhoujihao on 15-9-28.
 */
$(document).ready(function() {
    var imgs = $('.item-img');
    setTimeout(function() {
        imgs.animate({
            left: '-=20px'
        }, 500);
        imgs.animate({
            left: '+=20px'
        }, 500);
    }, 1000);
});