const toastStart = document.getElementById("toastStart");
const toastEnd = document.getElementById("toastEnd");

const timeStartToast = document.querySelector(".time_start_toast");
const timeEndToast = document.querySelector(".time_end_toast");

const toastBodyStart = document.querySelector(".toast-body-start");
const toastBodyEnd = document.querySelector(".toast-body-end");

let text = localStorage.getItem("complete_train");
// document.querySelector(".text_complete_train").innerHTML = text;
const usernameMqtt1 = document.querySelector("#username_login").innerHTML;

const dotNewNotify = document.querySelector(".dot_new_noti");
const contentNotify = document.querySelector(".content_notify");

function makeid() {
    var text = "";
    var possible =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}


var ip = location.host;
ip = ip.split(":")[0];
console.log({ ip });


const BROKER_URL = ip;
const PORT = 9001;
const USER_NAME = "aquarium123";
const PASSWORD = "aquarium123@";
var client = new Paho.MQTT.Client(BROKER_URL, PORT, makeid());

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

var options_ = {
    // useSSL: true,
    // userName: USER_NAME,
    // password: PASSWORD,
    onSuccess: onConnect,
    onFailure: doFail,
};

console.log("Waiting Check Train Connect to broker....");
client.connect(options_);

function doFail(e) {
    console.log(e);
}

function onConnect() {
    console.log("Connect successful");
    client.subscribe("Train_model");
    client.subscribe("fish_die");
    client.subscribe("start_eat");
}

function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log(responseObject.errorMessage);
    }
}

const renderNotify = () => {
    $.ajax({
        type: "GET",
        url: `/notify/get/${usernameMqtt1}`,
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
                contentNotify.innerHTML = "Chưa có thông báo nào";
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
    bodyFormData.append("username", usernameMqtt1);
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
            url: `/email_notify/get/${usernameMqtt1}`,
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
        ">>>>>>>>> TOPIC: [" +
            message.destinationName +
            "] : " +
            message.payloadString
    );
    const topic = message.destinationName;
    if (topic == "fish_die") {
        let today = new Date();
        const countDie = message.payloadString;

        const dateDie = moment(today).format("DD/MM/YYYY HH:mm:ss");
        const text = `[${dateDie}]: Dead fish found`;
        apiSendMail(text);
    } else if (topic === "start_eat") {
        let payload = message.payloadString;
        if (Number(payload) != 0) {
            let stateTrain = message.payloadString;
            let id = stateTrain.split("=")[0];

            document.getElementById("camera_open").src = "";
            localStorage.setItem("id_food_run", id);
        } else if (Number(payload) == 0) {
            let id = localStorage.getItem("id_food_run");
            // document.getElementById("camera_open").src = "/camera/fish_die";

            var bodyFormData = new FormData();

            bodyFormData.append("status", "COMPLETE");

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
        }
    } else {
        let stateTrain = message.payloadString;
        let state = stateTrain.split("=")[0];
        let time = stateTrain.split("=")[1];
        let name_fish = stateTrain.split("=")[2];
        let action = stateTrain.split("=")[3];

        if (state == "Start") {
            toastSuccess(`Start ${action}`);
        }
        if (state == "End") {
            // let content = `Hoàn thành đặt tên cho cá gần đây nhất vào lúc ${time}`;
            // localStorage.setItem("complete_train", content);
            // document.querySelector(".text_complete_train").innerHTML = content;

            let today = new Date();
            const dateDie = moment(today).format("DD/MM/YYYY HH:mm:ss");
            const text = `[${dateDie}]: Complete ${action}`;
            apiSendMail(text);
            toastSuccess(text);
        }
    }
}

// timeEndToast.innerHTML = '01/11/2022 - 20:58';
// const toast = new bootstrap.Toast(toastEnd);
// toast.show();

function public_message(topic, data) {
    var message = new Paho.MQTT.Message(data);

    message.destinationName = topic;
    client.send(message);
}
