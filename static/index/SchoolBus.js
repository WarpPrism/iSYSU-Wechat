/**
 * Created by zhoujihao on 15-12-6.
 */
$(function() {

    var u = navigator.userAgent, app = navigator.appVersion;
    //var isAndroid = u.indexOf('Android') > -1 || u.indexOf('Linux') > -1; //android终端或者uc浏览器
    var isiOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/); //ios终端

    if (navigator.userAgent.toLowerCase().match('chrome') == 'chrome' || isiOS) {
        $('#svg-div').css('display', 'block');

        var vivus = new Vivus('svg', {
            duration:200,
            type: 'oneByOne',
            animTimingFunction: Vivus.EASE
        }, function() {
            $('#svg-div').slideUp('7000');
        });
    } else {
        $('#svg-div').remove();
    }

    console.log("SchoolBus!");
    var all_tables = $("div.table-div");
    $("div.option").click(function(e) {
        var data_id = $(this).attr('data-id');

        $("div.option-div").hide();
        $(".btn-div").css('display', 'block');

        for (var i = 0; i < all_tables.length; i++) {
            if (($(all_tables[i]).attr('data-id')) == data_id) {
                $(all_tables[i]).fadeIn();
            }
        }
    });

    $("#return-btn").click(function() {
        for (var i = 0; i < all_tables.length; i++) {
            $(all_tables[i]).hide();
        }
        $("div.option-div").fadeIn();
        $(".btn-div").css('display', 'none');
    });
});
