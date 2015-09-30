/**
 * Created by zhoujihao on 15-9-28.
 */
$(document).ready(function() {
    var imgs = $('.item-img');
    var carousel = $('#img-carousel');
    var page_header = $('.page-header');
    setTimeout(function() {
        imgs.animate({
            left: '-=100px'
        }, 500);
        imgs.animate({
            left: '+=100px'
        }, 500);
    }, 1000);

    setTimeout(function() {
        carousel.slideDown(1000);
        /*page_header.fadeIn(2000);*/
    }, 4000)
});