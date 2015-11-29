// wx js sdk

var data ={
    signature: server_data.wx_config.signature
};
wx.config({
    debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
    appId: 'wxb9db0419592dbe7f', // 必填，公众号的唯一标识
    timestamp: server_data.wx_config.timestamp, // 必填，生成签名的时间戳
    nonceStr: server_data.wx_config.nonceStr, // 必填，生成签名的随机串
    signature: server_data.wx_config.signature,// 必填，签名，见附录1
    jsApiList: ['onMenuShareTimeline', 'onMenuShareAppMessage'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
});

wx.ready(function(res) {
    //alert(data.signature);
    // console.log(server_data.wx_config.signature);
    wx.checkJsApi({
        jsApiList: ['onMenuShareTimeline', 'onMenuShareAppMessage'],
        success: function(res) {
            // 以键值对的形式返回，可用的api值true，不可用为false
            // 如：{"checkResult":{"chooseImage":true},"errMsg":"checkJsApi:ok"}
            // console.log(JSON.stringify(res));
        }
    });

    // 分享到朋友圈
    wx.onMenuShareTimeline({
        title: '奔跑吧中大人！', // 分享标题
        link: 'http://isysu.sysu.edu.cn/shareGame/' + server_data.share_id, // 分享链接
        imgUrl: 'http://imgsrc.baidu.com/forum/w%3D580/sign=457f7eb5cfef76093c0b99971edca301/cfa34a540923dd541fc5dd40d509b3de9d824897.jpg', // 分享图标
        success: function () {
            // 用户确认分享后执行的回调函数
            alert("分享成功！你的小伙伴可以帮你过关啦！记得时常来看你的游戏状态哦～");
        },
        cancel: function () {
            // 用户取消分享后执行的回调函数
        }
    });
    // 分享给朋友
    wx.onMenuShareAppMessage({
        title: '奔跑吧中大人！', // 分享标题
        link: 'http://isysu.sysu.edu.cn/shareGame/' + server_data.share_id, // 分享链接
        desc: '在逸仙大道上尽情奔跑吧！', // 分享描述
        imgUrl: 'http://imgsrc.baidu.com/forum/w%3D580/sign=457f7eb5cfef76093c0b99971edca301/cfa34a540923dd541fc5dd40d509b3de9d824897.jpg', // 分享图标
        type: 'link', // 分享类型,music、video或link，不填默认为link
        dataUrl: '', // 如果type是music或video，则要提供数据链接，默认为空
        success: function () {
            // 用户确认分享后执行的回调函数
        },
        cancel: function () {
            // 用户取消分享后执行的回调函数
        }
    });
});

wx.error(function(res) {

});
