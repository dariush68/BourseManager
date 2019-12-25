$("#search-company").on('input',function(e){
    loadSymbols();
});



function loadSymbols() {

    let url_symbols = $("#url-symbol").attr("data-url")
    let url_home = $("#url-base").attr("data-url")
    // alert(url_symbols)
    let searchedText = $("#search-company").val();

    $("#list-company").empty();

    $.ajax({
        url: url_symbols,
        type: 'GET',
        dataType: 'json',
        data: {
            'q': searchedText,
        },
        success: function (data) {
            // console.log(JSON.stringify(data));
            // return;
            let companiesShowTile = $("#list-company");
            let results = data;
            let fullname = [];
            let symbol = [];
            let bourseType = [];
            let tse = [];
            let site = [];
            let isTarget = [];

            results.map(item => {
                fullname.push(item["fullName"]);
                symbol.push(item["symbol"]);
                bourseType.push(item["bourseType"]);
                tse.push(item["tse"]);
                site.push(item["site"]);
                isTarget.push(item["isTarget"]);
            });
            // companiesLoading.removeClass('loading');
            for (let i = 0; i < fullname.length; i++){

              if(isTarget[i]){
                  companiesShowTile.append(
                    `<tr>` +
                        `<input class="companyId" type="hidden" dataId=${results[i]["id"]}>` +
                        `<th scope="row" >${i}</th>` +
                        `<td class="company-symbol" >` +
                            `<a href="${url_home}${results[i]["id"]}/company-detail/"><i class="fa fa-external-link-alt"></i></a>` +
                            `${symbol[i]}` +
                        `</td>` +
                        `<td class="" >${fullname[i]}</td>` +
                        `<td class="d-none" ></td>` +
                        `<td class="" >${bourseType[i]}</td>` +
                        `<td class="d-none"></td>` +
                        `<td class="d-none"></td>` +
                        `<td class=""><a href="${tse[i]}" target="_blank">tse</a></td>` +
                        `<td class=""><a href="${site[i]}" target="_blank"><i class="fa fa-link"></i></a></td>` +
                        `<td class="">` +
                        `<i class="fa fa-star" style="color: #ffc400"></i>` +
                        `</td>` +
                        `<td class="d-none" ><a href="#"></a></td>` +
                      `</tr>`

                )
              }
              else{
                  companiesShowTile.append(
                    `<tr>` +
                        `<input class="companyId" type="hidden" dataId=${results[i]["id"]}>` +
                        `<th scope="row" >${i}</th>` +
                        `<td class="company-symbol" >` +
                            `<a href="${url_home}${results[i]["id"]}/company-detail/"><i class="fa fa-external-link-alt"></i></a>` +
                            `${symbol[i]}` +
                        `</td>` +
                        `<td class="" >${fullname[i]}</td>` +
                        `<td class="d-none" ></td>` +
                        `<td class="" >${bourseType[i]}</td>` +
                        `<td class="d-none"></td>` +
                        `<td class="d-none"></td>` +
                        `<td class=""><a href="${tse[i]}" target="_blank">tse</a></td>` +
                        `<td class=""><a href="${site[i]}" target="_blank"><i class="fa fa-link"></i></a></td>` +
                        `<td class=""></td>` +
                        `<td class="d-none" ><a href="#"></a></td>` +
                      `</tr>`

                )
              }


            }
        }
    })
}