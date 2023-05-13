const toastStart = document.getElementById("toastStart");
const toastEnd = document.getElementById("toastEnd");

const timeStartToast = document.querySelector(".time_start_toast");
const timeEndToast = document.querySelector(".time_end_toast");

const toastBodyStart = document.querySelector(".toast-body-start");
const toastBodyEnd = document.querySelector(".toast-body-end");
// !================================
const toastFoodFail = document.querySelector("#toastUploadLabelFail");
const toastFoodSuccess = document.querySelector("#toastUploadLabel");

const timeFoodUpload = document.querySelector(".time_upload");
const toastContentSuccess2 = document.querySelector("#toast_success_body");

const timeFoodFail = document.querySelector(".time_upload_fail");
const toastContentFailFood = document.querySelector("#toast_fail_body");

const usernameMqtt = document.querySelector("#username_login").innerHTML;

const chartShow = document.querySelector(".highcharts-figure");

const dotNewNotify = document.querySelector(".dot_new_noti");
const contentNotify = document.querySelector(".content_notify");

// !==============================================================================================

let chart;

const id_time_count_fish = localStorage.getItem("id_time_count_fish");
const time_count_fish = localStorage.getItem("time_count_fish");
const modeAIOFF = localStorage.getItem("switchAIForFishEat");

// chart count fish ate
Highcharts.theme = {
    colors: ["#FFB100", "#25f192", "#91D8E4", "#90ee7e", "#f45b5b"],
    chart: {
        backgroundColor: {
            linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
            stops: [
                [0, "#377D71"],
                // [1, '#3e3e40'],
            ],
        },
        style: {
            fontFamily: "'Unica One', sans-serif",
        },
        plotBorderColor: "#606063",
    },
    title: {
        style: {
            color: "#ffff",
            textTransform: "uppercase",
            fontSize: "17px",
        },
    },
    subtitle: {
        style: {
            color: "#E0E0E3",
            textTransform: "uppercase",
        },
    },
    xAxis: {
        gridLineColor: "#ccc",
        labels: {
            style: {
                color: "#E0E0E3",
                fontSize: "15px",
            },
        },
        lineColor: "#ccc",
        minorGridLineColor: "#505053",
        tickColor: "#ccc",
        title: {
            style: {
                color: "#ffff",
            },
        },
    },
    yAxis: {
        gridLineColor: "#ccc",
        labels: {
            style: {
                color: "#E0E0E3",
                fontSize: "15px",
            },
        },
        lineColor: "#ccc",
        minorGridLineColor: "#505053",
        tickColor: "#ccc",
        tickWidth: 1,
        title: {
            style: {
                color: "#ffff",
            },
        },
    },
    tooltip: {
        backgroundColor: "rgba(0, 0, 0, 0.85)",
        style: {
            color: "#F0F0F0",
        },
    },
    plotOptions: {
        series: {
            dataLabels: {
                color: "#F0F0F3",
                style: {
                    fontSize: "13px",
                },
            },
            marker: {
                lineColor: "#333",
            },
        },
        boxplot: {
            fillColor: "#505053",
        },
        candlestick: {
            lineColor: "white",
        },
        errorbar: {
            color: "white",
        },
    },
    legend: {
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        itemStyle: {
            color: "#E0E0E3",
        },
        itemHoverStyle: {
            color: "#FFF",
        },
        itemHiddenStyle: {
            color: "#606063",
        },
        title: {
            style: {
                color: "#C0C0C0",
            },
        },
    },
    credits: {
        style: {
            color: "#666",
        },
    },
    labels: {
        style: {
            color: "#707073",
        },
    },
    drilldown: {
        activeAxisLabelStyle: {
            color: "#F0F0F3",
        },
        activeDataLabelStyle: {
            color: "#F0F0F3",
        },
    },
    navigation: {
        buttonOptions: {
            symbolStroke: "#DDDDDD",
            theme: {
                fill: "#505053",
            },
        },
    },
    // scroll charts
    rangeSelector: {
        buttonTheme: {
            fill: "#505053",
            stroke: "#000000",
            style: {
                color: "#CCC",
            },
            states: {
                hover: {
                    fill: "#707073",
                    stroke: "#000000",
                    style: {
                        color: "white",
                    },
                },
                select: {
                    fill: "#000003",
                    stroke: "#000000",
                    style: {
                        color: "white",
                    },
                },
            },
        },
        inputBoxBorderColor: "#505053",
        inputStyle: {
            backgroundColor: "#333",
            color: "silver",
        },
        labelStyle: {
            color: "silver",
        },
    },
    navigator: {
        handles: {
            backgroundColor: "#666",
            borderColor: "#AAA",
        },
        outlineColor: "#CCC",
        maskFill: "rgba(255,255,255,0.1)",
        series: {
            color: "#7798BF",
            lineColor: "#A6C7ED",
        },
        xAxis: {
            gridLineColor: "#505053",
        },
    },
    scrollbar: {
        barBackgroundColor: "#808083",
        barBorderColor: "#808083",
        buttonArrowColor: "#CCC",
        buttonBackgroundColor: "#606063",
        buttonBorderColor: "#606063",
        rifleColor: "#FFF",
        trackBackgroundColor: "#404043",
        trackBorderColor: "#404043",
    },
};
// Apply the theme
Highcharts.setOptions(Highcharts.theme);

chart = new Highcharts.Chart({
    chart: {
        // spacingRight: 30,
        spacingTop: 20,
        defaultSeriesType: "spline",
        renderTo: "chart_food",
        events: {
            load: dataChart,
        },
    },
    title: {
        useHTML: true,
        text: `Chart of the amount of fish eaten on ${time_count_fish}`,
        style: { color: "white", fontSize: "18px", fontWeight: "600" },
    },
    time: {
        useUTC: true,
    },
    exporting: {
        enabled: true,
    },
    accessibility: {
        point: {
            valueDescriptionFormat: "{index}. {point.category}, {point.y:,.1f}",
        },
    },
    xAxis: {
        title: {
            text: "Time",
        },

        type: "datetime",
        plotLines: [
            {
                value: new Date("2023-01-23T22:37:38.945+00:00").getTime(),
                dashStyle: "dash",
                width: 4,
                color: "white",
            },
        ],
    },

    yAxis: {
        title: {
            text: "Amount",
        },
    },

    tooltip: {
        pointFormat:
            '<span style="color:{series.color}">{series.name}</span>: {point.y:,f} con<br/>',
        split: true,
    },

    series: [
        {
            name: "Count Fish",
            data: [],
        },
    ],
    responsive: {
        rules: [
            {
                condition: {
                    maxWidth: 1000,
                },
                chartOptions: {
                    legend: {
                        align: "center",
                        verticalAlign: "bottom",
                        layout: "horizontal",
                    },
                    exporting: {
                        enabled: false,
                    },

                    title: {
                        useHTML: true,
                        text: `Chart of the amount of fish eaten on ${time_count_fish}`,
                        style: {
                            color: "white",
                            fontSize: "14px",
                            fontWeight: "600",
                            textAlign: "center",
                        },
                    },
                    subtitle: {
                        text: null,
                    },
                    credits: {
                        enabled: false,
                    },
                },
            },
        ],
    },
});

let i = 0;
async function dataChart(data, realtime = false) {
    if (realtime) {
        let start = null;
        var addMlSeconds = 7 * 60 * 60 * 1000;
        if (i === 0) {
            i = 1;
            console.log(
                ">>>>>>>>>>>>>>>>>>>>>>>>>>>> set title <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
            );

            chart.series[0].update({
                data: [],
            });

            start = new Date(String(data.time)).getTime() + addMlSeconds;
            let timeStart = moment(data.time).format("DD/MM/YYYY, HH:mm:ss");

            console.log({ timeStart });

            chart.setTitle({
                text: `Chart of the amount of fish eaten on ${timeStart}`,
            });
            chart.series[0].update({
                name: String(timeStart),
            });
            localStorage.setItem("time_count_fish", timeStart);
        }
        const time = new Date(String(data.time)).getTime() + addMlSeconds;
        const point = [time, Number(data.count)];

        chart.series[0].addPoint(point, true, false);
        chart.xAxis[0].options.plotLines[0].value = start;
    } else {
        chart.series[0].update({
            data: [],
        });

        data.fish_count.forEach((v) => {
            const time = new Date(String(v.time)).getTime();
            const start = new Date(String(data.fish_count[0].time)).getTime();
            const point = [time, Number(v.amount)];

            chart.series[0].addPoint(point, true, false);
            chart.xAxis[0].options.plotLines[0].value = start;
            const timeCount = localStorage.getItem("time_count_fish");
            chart.series[0].update({
                name: String(data.fish_count[0].time),
            });
            chart.setTitle({
                text: `Chart of the amount of fish eaten on ${timeCount}`,
            });
        });
    }
}

// !==============================================================================================

const getTimePresentFood = () => {
    let today = new Date();
    let timePresent = today.getHours() + ":" + today.getMinutes();
    var datePresent = today.getDate() + "/" + (today.getMonth() + 1);

    return { timePresent, datePresent };
};
const toastFailFood = (message) => {
    const { datePresent, timePresent } = getTimePresentFood();
    timeFoodFail.innerHTML = timePresent + " - " + datePresent;
    toastContentFailFood.innerHTML = message;
    const toast = new bootstrap.Toast(toastFoodFail);
    toast.show();
};

const toastSuccessFood = (message) => {
    const { datePresent, timePresent } = getTimePresentFood();
    timeFoodUpload.innerHTML = timePresent + " - " + datePresent;
    toastContentSuccess2.innerHTML = message;
    const toast = new bootstrap.Toast(toastFoodSuccess);
    toast.show();
};

let text = localStorage.getItem("complete_train");

function makeid() {
    var text = "";
    var possible =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}
// /etc/mosquitto/mosquitto.conf
function getCurrentURL() {
    return window.location.href;
}

// Example

var ip = location.host;
ip = ip.split(":")[0];
console.log({ ip });

if (!ip) {
    location.reload();
}

const BROKER_URL = ip;
const PORT = 9001;
const USER_NAME = "aquarium123";
const PASSWORD = "aquarium123@";
var client = new Paho.MQTT.Client(BROKER_URL, PORT, makeid());

// const BROKER_URL = "e9b685676e514fb18a77577bc6449f0c.s1.eu.hivemq.cloud";
// const PORT = 8884;
// const USER_NAME = "thanhdai0411";
// const PASSWORD = "thanhdai0411";
// var client = new Paho.MQTT.Client(BROKER_URL, PORT, makeid());

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

var options_ = {
    onSuccess: onConnect,
    onFailure: doFail,
};

console.log("Waiting Connect to broker....");
client.connect(options_);

function doFail(e) {
    console.log(e);
    location.reload();
}

const getStateLedOnDB = () => {
    $.ajax({
        type: "GET",
        url: `/state_device/get/led`,
        contentType: false,
        cache: false,
        processData: false,
        success: function ({ success, data }) {
            if (success == 1) {
                let stateDeviceGet = JSON.parse(data)[0];

                if (stateDeviceGet.device == "led") {
                    const rgbCode = stateDeviceGet.state;
                    const checkOff = rgbCode.match(/\d+/g);
                    console.log(checkOff);
                    if (
                        checkOff[0] != "0" &&
                        checkOff[1] != "0" &&
                        checkOff[2] != "0"
                    ) {
                        stateOn(onOffDevice, textDevice, stateDevice);
                        localStorage.setItem("onOffDevice", 1);
                    }
                    public_message("rgb_control", rgbCode);
                }
            }
        },
    });
};

const getStatePumpOnDB = () => {
    $.ajax({
        type: "GET",
        url: `/state_device/get/pump`,
        contentType: false,
        cache: false,
        processData: false,
        success: function ({ success, data }) {
            if (success == 1) {
                let statePump = JSON.parse(data)[0];

                if (statePump.device == "pump" && statePump.state == "0") {
                    stateOn(switchForFishEat, textForFishEat, stateForFishEat);
                    public_message("relay_control", "L1E");
                }
            }
        },
    });
};

function onConnect() {
    console.log("Connect MQTT server");
    client.subscribe("food_complete");
    client.subscribe("Train_model");
    client.subscribe("feed_fish");
    client.subscribe("count_fish");
    client.subscribe("fish_die");
    client.subscribe("start_eat");
    client.subscribe("load_model_stream");

    getStatePumpOnDB();

    getStateLedOnDB();
}

function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log(responseObject.errorMessage);
    }
}

const valueRange = document.getElementById("value_range");

// $('[type="range"]').on("mouseup input", function () {
//     let rangePercent = $('[type="range"]').val();
//     // console.log({ rangePercent: Math.round((rangePercent * 255) / 100) });

//     function debounce(func, timeout = 300) {
//         let timer;
//         return (...args) => {
//             clearTimeout(timer);
//             timer = setTimeout(() => {
//                 func.apply(this, args);
//             }, timeout);
//         };
//     }
//     let a = 0;
//     function saveInput() {
//         const brightNess = Math.round((rangePercent * 255) / 100);
//         valueRange.innerHTML = brightNess;
//     }
//     const processChange = debounce(() => saveInput(), 1000);

//     processChange();
// });

const renderNotify = () => {
    $.ajax({
        type: "GET",
        url: `/notify/get/${usernameMqtt}`,
        dataType: "json",
        success: function ({ data }) {
            const notify = JSON.parse(data);
            if (notify && notify.length > 0) {
                console.log({ notify });
                const contentNotifyLoop = notify.map(
                    (v, index) => `
                
                    <p>${v.text}</p>
                `
                );
                contentNotify.innerHTML = contentNotifyLoop.join("");
            } else {
                contentNotify.innerHTML = "There are no notification yet";
            }
        },
    });
};

const sendMailInit = (email, text) => {
    var bodyFormData = new FormData();
    bodyFormData.append("text", text);
    bodyFormData.append("email", email);
    $.ajax({
        type: "POST",
        url: "/send_mail",
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            console.log({ data });
        },
    });
};

const saveDBNotify = (text) => {
    var bodyFormData = new FormData();
    bodyFormData.append("username", usernameMqtt);
    bodyFormData.append("text", text);

    $.ajax({
        type: "POST",
        url: "/notify/add",
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == "OK") {
                localStorage.setItem("new_noti", 1);
                dotNewNotify.classList.add("noti_new");
                renderNotify();
            }
        },
    });
};

const apiSendMail = (text) => {
    let emailNotify = localStorage.getItem("email_notify");

    if (emailNotify) {
        sendMailInit(emailNotify, text);
        saveDBNotify(text);
    } else {
        $.ajax({
            type: "GET",
            url: `/email_notify/get/${usernameMqtt}`,
            dataType: "json",
            success: function ({ data }) {
                const emailNotify = JSON.parse(data);
                if (emailNotify && emailNotify.length > 0) {
                    sendMailInit(emailNotify[0].email, text);
                    saveDBNotify(text);
                } else {
                    saveDBNotify(text);
                }
            },
        });
    }
};

function onMessageArrived(message) {
    console.log(
        ">>>>>>>>>  " + message.destinationName + ": " + message.payloadString
    );

    const topic = message.destinationName;

    if (topic === "food_complete") {
        let stateTrain = message.payloadString;
        let id = stateTrain.split("=")[0];
        let status = stateTrain.split("=")[1];

        var bodyFormData = new FormData();

        bodyFormData.append("status", status);

        $.ajax({
            type: "POST",
            url: `/food/update_status/${id}`,
            data: bodyFormData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (data === "OK") {
                    getValue();
                    toastSuccessFood(`Feed the fish successfully`);
                    $("#modalEditFood").modal("hide");
                }
            },
        });

        const rgbCode = localStorage.getItem("rgb_code");
        public_message("rgb_control", rgbCode);

        // getValue();
        // toastSuccessFood(`Feed the fish successfully`);
        // $("#modalEditFood").modal("hide");
    } else if (topic === "feed_fish") {
        let payload = message.payloadString.split("=");

        if (Number(payload[0]) === 1) {
            i = 0;
            localStorage.setItem("id_time_count_fish", payload[1]);
        }
        // else {
        //     $("#loading_feeder_fish").hide();
        //     chartShow.style.display = 'block';

        // }
    } else if (topic === "count_fish") {
        const payload = message.payloadString.split("=");
        const time = payload[0];
        const count = payload[1];
        const data = {
            time,
            count,
        };
        dataChart(data, true);
    } else if (topic === "fish_die") {
        let today = new Date();
        const countDie = message.payloadString;

        const dateDie = moment(today).format("DD/MM/YYYY HH:mm:ss");
        const text = `[${dateDie}]: Dead fish found`;
        apiSendMail(text);
    } else if (topic === "start_eat") {
        let payload = message.payloadString;
        if (Number(payload) == 0) {
            document.getElementById("camera_open").src = "";
            localStorage.setItem("id_food_run", id);
        } else if (Number(payload) != 0) {
            // let id = payload.split("=")[0];

            // document.getElementById("camera_open").src = "/camera/fish_die";

            document.getElementById("camera_open").src = "";

            // var bodyFormData = new FormData();
            getValue();
            // bodyFormData.append("status", "COMPLETE");

            // $.ajax({
            //     type: "POST",
            //     url: `/food/update_status/${id}`,
            //     data: bodyFormData,
            //     contentType: false,
            //     cache: false,
            //     processData: false,
            //     success: function (data) {
            //         if (data === "OK") {
            //             getValue();
            //             toastSuccessFood(`Feed the fish successfully`);
            //             $("#modalEditFood").modal("hide");
            //         }
            //     },
            // });

            // getStateLedOnDB();
        }
    } else if (topic == "load_model_stream") {
        const status = message.payloadString;

        if (status == "0") {
            // $("#opacity_loading_page").hide();
            $("#loading_open_camera").hide();
            $(".camera-btn_group").show();
        }
    } else {
        let stateTrain = message.payloadString;
        let state = stateTrain.split("=")[0];
        let time = stateTrain.split("=")[1];
        let name_fish = stateTrain.split("=")[2];

        console.log({ state, time });

        if (state == "Start") {
            toastSuccessFood(`Start training the name ${name_fish} at ${time}`);
        }
        if (state == "End") {
            // let content = `Hoàn thành đặt tên cho cá gần đây nhất vào lúc ${time}`;
            // localStorage.setItem("complete_train", content);
            // document.querySelector(".text_complete_train").innerHTML = content;

            let today = new Date();
            const dateDie = moment(today).format("DD/MM/YYYY HH:mm:ss");
            const text = `[${dateDie}]: Completed name training ${name_fish}`;
            apiSendMail(text);
            toastSuccessFood(`Complete naming ${name_fish} for fish`);
        }
    }
}

function public_message(topic, data) {
    var message = new Paho.MQTT.Message(data);

    message.destinationName = topic;
    client.send(message);
}

//! handle control

const switchForFishEat = document.getElementById("for_fish_eat");
const textForFishEat = document.getElementById("text-for_fish_eat");
const stateForFishEat = document.querySelector(".state-for_fish_eat");

const stateForPreesEat = document.querySelector(".state-for_press_eat");
const textForPreesEat = document.querySelector("#text-for_press_eat");

const switchAIForFishEat = document.getElementById("ai_fish_eat");
const textAI = document.getElementById("text-ai_fish_eat");
const stateAI = document.querySelector(".state-ai_fish_eat");

const onOffDevice = document.getElementById("on_off_device");
const textDevice = document.getElementById("text-on_off_device");
const stateDevice = document.querySelector(".state-on_off_device");

const btnPressFeeder = document.querySelector(".btn_press_food");

//!control press feeder
btnPressFeeder.onmousedown = (e) => {
    const timePress = new Date();
    const startPress = moment(timePress).format("DD/MM/YYYY HH:mm:ss");

    const pressPrevius =
        localStorage.getItem("time_click") ||
        moment(timePress).format("DD/MM/YYYY HH:mm:ss");

    if (startPress >= pressPrevius) {
        const endPress = moment()
            .add(2, "seconds")
            .format("DD/MM/YYYY HH:mm:ss");
        localStorage.setItem("time_click", endPress);

        btnPressFeeder.textContent = "Release";
        stateForPreesEat.classList.remove("control_switch");
        stateForPreesEat.classList.add("control_switch-off");
        textForPreesEat.innerHTML = "ON";

        public_message("motor_control", "M100E");

        // setTimeout(() => {
        //     public_message("rgb_control", "R255G255B255E");
        // }, 1000);

        // $.ajax({
        //     type: "GET",
        //     url: "/camera/cnt_fish_press",
        //     dataType: "json",
        //     success: function ({ data }) {
        //         // localStorage.getItem("rgb");
        //         const rgbCode = localStorage.getItem("rgb_code");
        //         public_message("rgb_control", rgbCode);
        //     },
        // });
    } else {
        toastFailFood(`Between change is 2 second`);
        return;
        // alert("Please betweent 2 click is 5 minutes");
    }

    // btnPressFeeder.textContent = "Release";
    // stateForPreesEat.classList.remove("control_switch");
    // stateForPreesEat.classList.add("control_switch-off");
    // textForPreesEat.innerHTML = "ON";
    // public_message("motor_control", "M100E");
};
btnPressFeeder.onmouseup = (e) => {
    btnPressFeeder.textContent = "Press";
    stateForPreesEat.classList.remove("control_switch-off");
    stateForPreesEat.classList.add("control_switch");
    textForPreesEat.innerHTML = "OFF";
};

//

const stateOff = (input, text, state) => {
    input.removeAttribute("checked");
    text.innerHTML = "OFF";
    state.classList.add("control_switch-off");
    state.classList.remove("control_switch");
};
const stateOn = (input, text, state) => {
    input.setAttribute("checked", true);
    text.innerHTML = "ON";
    state.classList.add("control_switch");
    state.classList.remove("control_switch-off");
};

const stateSwitch = (input, text, state, local) => {
    let isAttributeCheck = input.getAttribute("checked");
    if (isAttributeCheck === "true") {
        stateOff(input, text, state);
        localStorage.setItem(local, 0);
        return 0;
    } else {
        stateOn(input, text, state);
        localStorage.setItem(local, 1);
        return 1;
    }
};

const stateSave = (local) => {
    local.forEach((v) => {
        let localState = localStorage.getItem(v);
        if (v == "switchAIForFishEat" && localState == 1) {
            stateOn(switchAIForFishEat, textAI, stateAI);
        } else if (v == "switchForFishEat" && localState == 1) {
            stateOn(switchForFishEat, textForFishEat, stateForFishEat);
        } else if (v == "onOffDevice" && localState == 1) {
            stateOn(onOffDevice, textDevice, stateDevice);

            // const codeRgb = localStorage.getItem("rgb_code");
            // public_message("rgb_control", codeRgb);
        }
    });
};
stateSave(["switchAIForFishEat", "switchForFishEat", "onOffDevice"]);

// ai for fish eat
// switchAIForFishEat.onchange = (e) => {
//     let state = stateSwitch(
//         switchAIForFishEat,
//         textAI,
//         stateAI,
//         "switchAIForFishEat"
//     );
//     getValue();
//     public_message("control_ai_food", state.toString());
// };

// control relay
switchForFishEat.onchange = (e) => {
    let state = stateSwitch(
        switchForFishEat,
        textForFishEat,
        stateForFishEat,
        "switchForFishEat"
    );

    state = state == 1 ? 0 : 1;

    const relayControl = `L${state}E`;
    public_message("relay_control", relayControl);

    var bodyFormData = new FormData();
    bodyFormData.append("state", String(state));
    $.ajax({
        type: "PUT",
        url: `/state_device/update/pump`,
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {},
    });
};

// control device led rgb
onOffDevice.onchange = (e) => {
    let state = stateSwitch(
        onOffDevice,
        textDevice,
        stateDevice,
        "onOffDevice"
    );

    if (state == 1) {
        $.ajax({
            type: "GET",
            url: `/state_device/get/led`,
            contentType: false,
            cache: false,
            processData: false,
            success: function ({ success, data }) {
                if (success == 1) {
                    let stateDevice = JSON.parse(data)[0];
                    if (stateDevice.device == "led") {
                        const rgbCode = stateDevice.state;
                        public_message("rgb_control", rgbCode);
                    }
                }
            },
        });
    } else if (state == 0) {
        const rgbCode = `R${0}G${0}B${0}E`;

        var bodyFormData = new FormData();
        bodyFormData.append("state", rgbCode);
        $.ajax({
            type: "PUT",
            url: `/state_device/update/led`,
            data: bodyFormData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {},
        });

        public_message("rgb_control", rgbCode);
    }
};

//! end handle control

//!control color food
const colorLamp = document.querySelector("#control_color");

colorLamp.onchange = (ev) => {
    let localState = localStorage.getItem("onOffDevice");
    if (localState == 1) {
        const color = ev.target.value;
        const r = parseInt(color.substr(1, 2), 16);
        const g = parseInt(color.substr(3, 2), 16);
        const b = parseInt(color.substr(5, 2), 16);
        console.log(`red: ${r}, green: ${g}, blue: ${b}`);

        const timePress = new Date();
        const startPress = moment(timePress).format("DD/MM/YYYY HH:mm:ss");

        const pressPrevius =
            localStorage.getItem("rgb_click") ||
            moment(timePress).format("DD/MM/YYYY HH:mm:ss");

        if (startPress >= pressPrevius) {
            const endPress = moment()
                .add(2, "seconds")
                .format("DD/MM/YYYY HH:mm:ss");
            localStorage.setItem("rgb_click", endPress);

            const rgbCode = `R${r}G${g}B${b}E`;
            public_message("rgb_control", rgbCode);

            //! save rgb code
            var bodyFormData = new FormData();
            bodyFormData.append("state", rgbCode);
            $.ajax({
                type: "PUT",
                url: `/state_device/update/led`,
                data: bodyFormData,
                contentType: false,
                cache: false,
                processData: false,
                success: function (data) {},
            });

            //! end save rgb code
        } else {
            toastFailFood(`Between change is 2 second`);
            return;
            // alert("Please betweent 2 click is 5 minutes");
        }

        // const rgbCode = `R${r}G${g}B${b}E`;
        // localStorage.setItem("rgb_code", rgbCode);
        // public_message("rgb_control", rgbCode);
    } else {
        toastFailFood(`Please open to control`);
    }
};

//!end control color food

// ! handle call data for chart

const btnReloadChart = document.querySelector("#btn_reload_chart");
const btnSearchChart = document.querySelector("#btn_search_chart");
const inputChart = document.querySelector("#input_date_chart");

const textDateEat = document.querySelector("#date_eat");
const tableBodyChart = document.querySelector("#table_body_chart");
const loadingChart = document.querySelector("#loading_chart");
const tableChart = document.querySelector("#table_chart");

// const loadingFeedFish = document.querySelector('#loading_feeder_fish')

// const tableBodyFood = document.querySelector('#table_body_food');

// $(document).ready(function () {
//     if (chartShow.style.display == 'block') {
//         $('#opacity_loading_page').show()
//     }
// })

$("#loading_chart").hide();
$("#table_chart").hide();
// $("#loading_feeder_fish").hide();

// chartShow.style.display = 'none';

const getFishCount = () => {
    $.ajax({
        type: "GET",
        url: `/count_fish/get`,
        dataType: "json",
        success: function (data) {
            dataChart(data);
        },
    });
};

const getFishCountDetail = (id) => {
    console.log({ id });
    $.ajax({
        type: "GET",
        url: `/count_fish/get_detail/${id}`,
        dataType: "json",
        success: function (data) {
            console.log({ data_reload: data });
            localStorage.setItem("data_count_fish", JSON.stringify(data));
            $("#opacity_loading_page").hide();
            $("#loading_chart").hide();
            $("#table_chart").show();
            $("#modalChart").modal("hide");
            dataChart(data);
        },
    });
};

const getFishCountByDate = (date) => {
    // 26-01-2023
    // const formatDateQuery = moment(date).format("MM-DD-YYYY");
    // console.log({ formatDateQuery });
    $.ajax({
        type: "GET",
        url: `/count_fish/get_date/${date}`,
        dataType: "json",
        success: function (data) {
            console.log({ data_chart: data });
            if (data.length <= 0) {
                textDateEat.innerHTML = null;
                tableBodyChart.innerHTML = `No data on date ${date}`;
                $("#btn_search_chart").show();
                $("#table_chart").show();
                $("#loading_chart").hide();
                return;
            }
            $("#btn_search_chart").show();
            $("#table_chart").show();
            $("#loading_chart").hide();
            textDateEat.innerHTML = `
Feeding timelines for the day ${date}`;
            let content;
            content = data.map((item, index) => {
                return `
                                <tr class="text-center">
                                    <th scope="row">${index}</th>
                                    <td id="time_count_fish" data-time_original="${
                                        item._id
                                    }">${moment(item.time_start).format(
                    "DD/MM/YYYY, HH:mm:ss"
                )}</td>
                                    <td>
                                        <button id="btn_chart_choose"
                                            style="border: none; background-color: orange ; border-radius: 5px;color : white;">Watch</button>
                                    </td>
                                </tr>`;

                // console.log({ data })
            });
            console.log({ content });
            tableBodyChart.innerHTML = content.join("");

            const btnChartChoose =
                document.querySelectorAll("#btn_chart_choose");
            const timeCountFish = document.querySelectorAll("#time_count_fish");
            btnChartChoose.forEach((btn, index) => {
                btn.onclick = (e) => {
                    const timeCount = timeCountFish[index].innerHTML;
                    const id =
                        timeCountFish[index].getAttribute("data-time_original");

                    localStorage.setItem("time_count_fish", timeCount);
                    localStorage.setItem("id_time_count_fish", id);

                    $("#loading_chart").show();
                    $("#table_chart").hide();
                    getFishCountDetail(id);
                };
            });
        },
    });
};

btnSearchChart.onclick = (e) => {
    if (!inputChart.value) {
        toastFailFood(`Please select the date you want to query`);
        return;
    }
    $("#btn_search_chart").hide();
    $("#loading_chart").show();
    const inputDateValue = inputChart.value.split("-");
    console.log(inputDateValue);
    const date = `${inputDateValue[2]}-${inputDateValue[1]}-${inputDateValue[0]}`;
    getFishCountByDate(date);
};

// default call

// const updateFoodSettingDaily = () => {
//     console.log("call update daily");
//     $.ajax({
//         type: "GET",
//         url: `/food/update_daily`,
//         contentType: false,
//         cache: false,
//         processData: false,
//         success: function (data) {
//             if (data === "OK") {
//                 getValue();
//                 // toastSuccessFood('Update daily food');
//             } else {
//                 toastFail("Update fail");
//             }
//         },
//     });
// };
$("#opacity_loading_page").hide();

// $(document).ready(function () {
//     console.log("reload page");
//     const date = new Date();

//     const dateCurrent = moment(date).format("DD/MM/YYYY");
//     const dateSave = localStorage.getItem("date_current");

//     if (dateSave != dateCurrent) {
//         updateFoodSettingDaily();
//         localStorage.setItem("date_current", dateCurrent);
//     }
// });

// test camera brower
