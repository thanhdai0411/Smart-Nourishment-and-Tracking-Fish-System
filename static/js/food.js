const amountFood = document.querySelector('#amount_food');
const timeSet = document.querySelector('#set_time');
const btnSaveSettingFood = document.querySelector('#button_save_food');
const btnCompleteSetting = document.querySelector('#btn_complete_setting');

const chartElement = document.querySelector('.highcharts-figure');

const valueRenderSetting = document.querySelector('.value_setting');
const tableBodyFood = document.querySelector('#table_body_food');

//!util
const toastUploadFail = document.querySelector('#toastUploadLabelFail');
const toastUploadSuccess = document.querySelector('#toastUploadLabel');

const timeUpload = document.querySelector('.time_upload');
const toastContentSuccess = document.querySelector('#toast_success_body');

const timeUploadFail = document.querySelector('.time_upload_fail');
const toastContentFail = document.querySelector('#toast_fail_body');
const getTimePresent = () => {
    let today = new Date();
    let timePresent = today.getHours() + ':' + today.getMinutes();
    var datePresent = today.getDate() + '/' + (today.getMonth() + 1);
    return { timePresent, datePresent };
};
const toastFail = (message) => {
    const { datePresent, timePresent } = getTimePresent();
    timeUploadFail.innerHTML = timePresent + ' - ' + datePresent;
    toastContentFail.innerHTML = message;
    const toast = new bootstrap.Toast(toastUploadFail);
    toast.show();
};

const toastSuccess = (message) => {
    const { datePresent, timePresent } = getTimePresent();
    timeUpload.innerHTML = timePresent + ' - ' + datePresent;
    toastContentSuccess.innerHTML = message;
    const toast = new bootstrap.Toast(toastUploadSuccess);
    toast.show();
};

const userNameLogin = document.querySelector('#username_login').innerHTML;

// edit setting food
const modalEditFood = document.getElementById('modalEditFood');
const modalDeleteFood = document.getElementById('modalDeleteFood');
const timeFoodEdit = document.getElementById('time_food_edit');
const amountFoodEdit = document.getElementById('amount_food_edit');
const btnCompleteEdit = document.getElementById('btn_complete_edit');
const btnCompleteDelete = document.getElementById('btn_complete_delete');

// edit food

modalEditFood.addEventListener('show.bs.modal', (event) => {
    const button = event.relatedTarget;

    console.log(button);

    const id = button.getAttribute('data-id-food');
    const time = button.getAttribute('data-time-food');
    const amount = button.getAttribute('data-amount-food');

    timeFoodEdit.value = time;
    amountFoodEdit.value = amount;

    btnCompleteEdit.onclick = (e) => {
        const completeTimeEdit = timeFoodEdit.value;
        const completeAmountEdit = amountFoodEdit.value;
        var bodyFormData = new FormData();

        bodyFormData.append('time', completeTimeEdit);
        bodyFormData.append('amount_food', completeAmountEdit);
        bodyFormData.append('username', userNameLogin);
        $.ajax({
            type: 'POST',
            url: `/food/update/${id}`,
            data: bodyFormData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (data === 'OK') {
                    getValue();
                    toastSuccess('Sửa đổi thành công');
                    $('#modalEditFood').modal('hide');
                } else {
                    toastFail('Sửa đổi thất bại');
                    $('#modalEditFood').modal('hide');
                }
            },
        });
    };
});
// end edit setting food

// delete food
modalDeleteFood.addEventListener('show.bs.modal', (event) => {
    const button = event.relatedTarget;

    const id = button.getAttribute('data-id-food');

    btnCompleteDelete.onclick = (e) => {
        $.ajax({
            type: 'DELETE',
            url: `/food/delete/${id}`,
            dataType: 'json',
            success: function (data) {
                if (data.success == 1) {
                    getValue();
                    toastSuccess('Xóa thành công');
                    $('#modalDeleteFood').modal('hide');
                } else {
                    $('#modalDeleteFood').modal('hide');
                    toastFail('Xóa thất bại');
                }
            },
        });
    };
});
// end delete setting food

// get render value when reload
const modeAI = localStorage.getItem('switchAIForFishEat');

const getValue = () => {
    const modeAI = localStorage.getItem('switchAIForFishEat');

    if (modeAI == 1) {
        tableBodyFood.innerHTML = `<td colspan="5">Bạn đang trong chế đố cho ăn tự động bằng AI</td>`;
        chartElement.classList.add('d-none');
        return;
    }
    $.ajax({
        type: 'GET',
        url: `/food/get/${userNameLogin}`,
        dataType: 'json',
        success: function (data) {
            const { data: foods, success } = data;
            localStorage.setItem('setting_food', foods);
            let foodData = JSON.parse(foods);
            // location.reload();
            if (success === 1 && foodData.length > 0) {
                const tableContent = foodData.map((v, index) => {
                    let id = v._id.$oid;

                    let style =
                        v.status === 'WAITING'
                            ? '#e8733b'
                            : v.status === 'COMPLETE'
                            ? '#54B435'
                            : '#8B7E74';
                    return `
                                    <tr class="text-center">
                                        <th scope="row">${index + 1} </th>
                                        <td id="name_label_show"  >${v.time}</td>
                                        <td>${v.amount_food}</td>
                                        <td > <span style="border-radius : 5px ; background-color : ${style}; padding : 3px 10px; font-weight: 500 ; font-size: 14px ; ">${
                        v.status
                    }</span></td>
                                    <td> <button class="btn_action_food" data-id-food="${id}" data-time-food="${
                        v.time
                    }" data-amount-food="${
                        v.amount_food
                    }" data-bs-toggle="modal" data-bs-target="#modalEditFood">EDIT</button> 
                                    <button class="btn_action_food_delete" data-id-food="${id}" data-bs-toggle="modal" data-bs-target="#modalDeleteFood">DELETE</button></td>
    
                                       
                                    </tr>`;
                });
                tableBodyFood.innerHTML = tableContent.join('');

                chartElement.classList.remove('d-none');
            } else {
                console.log('not data');
                tableBodyFood.innerHTML = `<td colspan="5">Chưa có cài đặt nào</td>`;
                chartElement.classList.add('d-none');
            }
        },
    });
};

if (modeAI == 1) {
    tableBodyFood.innerHTML = `<td colspan="5">Bạn đang trong chế đố cho ăn tự động bằng AI</td>`;
    chartElement.classList.add('d-none');
} else {
    getValue();
}
// emd get render value when reload

btnCompleteSetting.onclick = (e) => {
    const modeAI = localStorage.getItem('switchAIForFishEat');

    const userNameLogin = document.querySelector('#username_login').innerHTML;

    const userTimeSet = timeSet.value;
    const userAmountFoodSet = amountFood.value;
    // const { timePresent } = getTimePresent();
    // if (timePresent.split(':')[0] > userTimeSet.split(':')[0]) {
    //     toastFail('Đã qua mốc thời gian này trong ngày hôm nay');

    //     return;
    // }

    if (modeAI == 1) {
        toastFail('Bạn đang trong chế độ cho ăn bằng AI không thể cài đặt');
        return;
    }
    if (!userTimeSet || !userAmountFoodSet) {
        toastFail('Cài đặt thời gian cho ăn thất bại');
        return;
    }

    var bodyFormData = new FormData();

    bodyFormData.append('time', userTimeSet);
    bodyFormData.append('amount_food', userAmountFoodSet);
    bodyFormData.append('username', userNameLogin);

    $.ajax({
        type: 'POST',
        url: '/food/add',
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data === 'OK') {
                getValue();
                toastSuccess('Cài đặt thời gian cho ăn thành công');
            } else if (data == 'LIMIT') {
                toastFail('Cài đặt tối đa là 10');
            } else if (data == 'EXIST_TIME') {
                toastFail('Thời gian cài đặt đã tồn tại');
            } else {
                toastFail('Cài đặt thời gian cho ăn thất bại');
            }
        },
    });
};

// chart count fish ate
Highcharts.theme = {
    colors: [
        'orange',
        '#25f192',
        '#91D8E4',
        '#90ee7e',
        '#f45b5b',
        // '#ff0066',
        // '#eeaaee',
        // '#55BF3B',
        // '#DF5353',
        // '#7798BF',
        // '#aaeeee',
    ],
    chart: {
        backgroundColor: {
            linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
            stops: [
                [0, '#38604e'],
                // [1, '#3e3e40'],
            ],
        },
        style: {
            fontFamily: "'Unica One', sans-serif",
        },
        plotBorderColor: '#606063',
    },
    title: {
        style: {
            color: '#ffff',
            textTransform: 'uppercase',
            fontSize: '17px',
        },
    },
    subtitle: {
        style: {
            color: '#E0E0E3',
            textTransform: 'uppercase',
        },
    },
    xAxis: {
        gridLineColor: '#ccc',
        labels: {
            style: {
                color: '#E0E0E3',
                fontSize: '15px',
            },
        },
        lineColor: '#ccc',
        minorGridLineColor: '#505053',
        tickColor: '#ccc',
        title: {
            style: {
                color: '#ffff',
            },
        },
    },
    yAxis: {
        gridLineColor: '#ccc',
        labels: {
            style: {
                color: '#E0E0E3',
                fontSize: '15px',
            },
        },
        lineColor: '#ccc',
        minorGridLineColor: '#505053',
        tickColor: '#ccc',
        tickWidth: 1,
        title: {
            style: {
                color: '#ffff',
            },
        },
    },
    tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        style: {
            color: '#F0F0F0',
        },
    },
    plotOptions: {
        series: {
            dataLabels: {
                color: '#F0F0F3',
                style: {
                    fontSize: '13px',
                },
            },
            marker: {
                lineColor: '#333',
            },
        },
        boxplot: {
            fillColor: '#505053',
        },
        candlestick: {
            lineColor: 'white',
        },
        errorbar: {
            color: 'white',
        },
    },
    legend: {
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        itemStyle: {
            color: '#E0E0E3',
        },
        itemHoverStyle: {
            color: '#FFF',
        },
        itemHiddenStyle: {
            color: '#606063',
        },
        title: {
            style: {
                color: '#C0C0C0',
            },
        },
    },
    credits: {
        style: {
            color: '#666',
        },
    },
    labels: {
        style: {
            color: '#707073',
        },
    },
    drilldown: {
        activeAxisLabelStyle: {
            color: '#F0F0F3',
        },
        activeDataLabelStyle: {
            color: '#F0F0F3',
        },
    },
    navigation: {
        buttonOptions: {
            symbolStroke: '#DDDDDD',
            theme: {
                fill: '#505053',
            },
        },
    },
    // scroll charts
    rangeSelector: {
        buttonTheme: {
            fill: '#505053',
            stroke: '#000000',
            style: {
                color: '#CCC',
            },
            states: {
                hover: {
                    fill: '#707073',
                    stroke: '#000000',
                    style: {
                        color: 'white',
                    },
                },
                select: {
                    fill: '#000003',
                    stroke: '#000000',
                    style: {
                        color: 'white',
                    },
                },
            },
        },
        inputBoxBorderColor: '#505053',
        inputStyle: {
            backgroundColor: '#333',
            color: 'silver',
        },
        labelStyle: {
            color: 'silver',
        },
    },
    navigator: {
        handles: {
            backgroundColor: '#666',
            borderColor: '#AAA',
        },
        outlineColor: '#CCC',
        maskFill: 'rgba(255,255,255,0.1)',
        series: {
            color: '#7798BF',
            lineColor: '#A6C7ED',
        },
        xAxis: {
            gridLineColor: '#505053',
        },
    },
    scrollbar: {
        barBackgroundColor: '#808083',
        barBorderColor: '#808083',
        buttonArrowColor: '#CCC',
        buttonBackgroundColor: '#606063',
        buttonBorderColor: '#606063',
        rifleColor: '#FFF',
        trackBackgroundColor: '#404043',
        trackBorderColor: '#404043',
    },
};
// Apply the theme
Highcharts.setOptions(Highcharts.theme);

Highcharts.chart('chart_food', {
    chart: {
        type: 'spline',
    },
    title: {
        useHTML: true,
        text: 'Biều đồ số lượng cá ăn theo giờ gian',
    },
    time: {
        useUTC: false,
    },
    exporting: {
        enabled: false,
    },
    accessibility: {
        point: {
            valueDescriptionFormat: '{index}. {point.category}, {point.y:,.1f}',
        },
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150,
        title: {
            text: 'Thời gian',
        },
    },

    yAxis: {
        title: {
            text: 'Số lượng',
        },
        // labels: {
        //     format: '{value}',
        // },
        plotLines: [
            {
                value: 0,
                width: 1,
                color: '#808080',
            },
        ],
    },

    tooltip: {
        pointFormat:
            '<span style="color:{series.color}">{series.name}</span>: {point.y:,f} con<br/>',
        split: true,
    },

    series: [
        {
            name: 'Day 1',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = new Date().getTime(),
                    i;

                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.floor(Math.random() * 10),
                    });
                }
                return data;
            })(),
        },
        {
            name: 'Day 2',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = new Date().getTime(),
                    i;

                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.floor(Math.random() * 10),
                    });
                }
                return data;
            })(),
        },
        {
            name: 'Day 3',
            data: (function () {
                // generate an array of random data
                var data = [],
                    time = new Date().getTime(),
                    i;

                for (i = -19; i <= 0; i += 1) {
                    data.push({
                        x: time + i * 1000,
                        y: Math.floor(Math.random() * 10),
                    });
                }
                return data;
            })(),
        },
    ],
});
