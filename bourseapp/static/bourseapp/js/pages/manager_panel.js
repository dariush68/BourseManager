
// Tooltips Initialization
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});



function newsApproveByManager(news_id) {

    let url_newsApprove = $("#url-news-approve").attr("data-url");
    url_newsApprove = url_newsApprove.replace('1234', news_id);
     // alert(url_newsApprove);
     // return
    $("#modalNewsApprove").modal("hide");

    $.ajax({
        url: url_newsApprove,
        type: 'GET',
        // dataType: 'json',
        // data: query,
        success: function (data) {
            // alert(data)
            if(data.indexOf("news approved") > -1){
                let news_tile = "#news-awaitForCheck-" + news_id;
                $(news_tile).addClass("d-none");
            }
        }
    })

}


function userApproveByManager(user_id) {

    let url_userApprove = $("#url-user-approve").attr("data-url");
    url_userApprove = url_userApprove.replace('1234', user_id);
     // alert(url_newsApprove);
     // return

    $.ajax({
        url: url_userApprove,
        type: 'GET',
        // dataType: 'json',
        // data: query,
        success: function (data) {
            // alert(data)
            if(data.indexOf("user activated") > -1){
                let user_tile = "#user-awaitForCheck-" + user_id;
                $(user_tile).addClass("d-none");
            }
        }
    })

}


function userVIPByManager(user_id, status, user, first_name, last_name) {

    let url_userVip = $("#url-user-vip").attr("data-url");
    url_userVip = url_userVip.replace('1234', user_id);
    url_userVip = url_userVip.replace('5678', status);
     // alert(url_newsApprove);
     // return

    $.ajax({
        url: url_userVip,
        type: 'GET',
        // dataType: 'json',
        // data: query,
        success: function (data) {
            // alert(data)
            if(data.indexOf("remove user vip") > -1) {
                let user_tile = "#user-VIP-" + user_id;
                $(user_tile).remove();

                $("#card-all-users").append(
                    `<div id="user-awaitForVIP-${ user_id }" class="media white z-depth-1 rounded mb-1" dir="ltr">` +
                        `<div class="media-body p-1">` +
                            `<a href="{% url 'admin:auth_user_change' user.id %}" target="_blank">` +
                                `<p class="text-uppercase text-muted mb-1">` +
                                   `<a class="float-left" target="_blank" onclick="userVIPByManager(${ user_id }, '1', '${ user }', '${ first_name }', '${last_name }' )" data-toggle="tooltip" title="ارتقاع سطح به VIP"><i class="small" style="color: #c69500">VIP</i></a>` +
                                    `<a class="float-left" target="_blank" href="/admin/auth/user/${ user_id }/change/" data-toggle="tooltip" title="تغییر اطلاعات کاربر"><i class="fa fa-edit ml-1 small" style="color: #a0a0a0"></i></a>` +
                                    `<a class="float-left" target="_blank" href="/admin/auth/user/${ user_id }/delete/" data-toggle="tooltip" title="حذف کاربر"><i class="fa fa-trash-alt ml-1 small" style="color: #a0a0a0"></i></a>` +
                                    `<small>${ user }</small>` +
                                `</p>` +
                            `</a>` +
                            `<h7 class="font-weight-bold mb-0">${first_name } ${last_name }</h7>` +
                        `</div>` +
                        `<i class="blue-grey z-depth-1 p-3 rounded-right text-white small" style="height: 54px; width: 70px">کاربر</i>` +
                    `</div>`
                );
            }
            else{
                let user_tile = "#user-awaitForVIP-" + user_id;
                $(user_tile).remove();

                $("#card-vip-users").append(
                    `<div id="user-VIP-${ user_id }" class="media white z-depth-1 rounded mb-1" dir="ltr">` +
                        `<div class="media-body p-1">` +
                            `<a href="{% url 'admin:auth_user_change' user.id %}" target="_blank">` +
                                `<p class="text-uppercase text-muted mb-1">` +
                                    `<a class="float-left" target="_blank" onclick="userVIPByManager(${ user_id }, '0', '${ user }', '${ first_name }', '${ last_name }' )" data-toggle="tooltip" title="حذف سطح VIP">` +
                                        `<i class="fa fa-times small" style="color: #9f105c"></i><i class="small" style="color: #9f105c">VIP</i></a>` +
                                    `<a class="float-left" target="_blank" href="/admin/auth/user/${ user_id }/change/" data-toggle="tooltip" title="تغییر اطلاعات کاربر"><i class="fa fa-edit ml-1 small" style="color: #a0a0a0"></i></a>` +
                                    `<a class="float-left" target="_blank" href="/admin/auth/user/${ user_id }/delete/" data-toggle="tooltip" title="حذف کاربر"><i class="fa fa-trash-alt ml-1 small" style="color: #a0a0a0"></i></a>` +
                                    `<small>${ user }</small>` +
                                `</p>` +
                            `</a>` +
                            `<h7 class="font-weight-bold mb-0">${first_name } ${last_name }</h7>` +
                        `</div>` +
                        `<i class="fa fa-user-alt yellow z-depth-1 p-3 rounded-right text-black" style="height: 54px; width: 54px"></i>` +
                    `</div>`
                );
            }
        }
    })

}