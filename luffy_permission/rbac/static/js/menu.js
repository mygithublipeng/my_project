$('.item .title').click(function () {
    // $(this).next().toggleClass('hide')
    $(this).next().removeClass('hide');   // 当前一级菜单下的二级菜单展开
    $(this).parent().siblings().find('.body').addClass('hide') ;  // 其他菜单下的二级菜单闭合

    // $(this).next().removeClass('hide').parent().siblings().find('.body').addClass('hide');
});
