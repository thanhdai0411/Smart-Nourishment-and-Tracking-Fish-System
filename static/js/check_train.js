const toastStart = document.getElementById("toastStart");
const toastEnd = document.getElementById("toastEnd");

const timeStartToast = document.querySelector(".time_start_toast");
const timeEndToast = document.querySelector(".time_end_toast");

const toastBodyStart = document.querySelector(".toast-body-start");
const toastBodyEnd = document.querySelector(".toast-body-end");

let text = localStorage.getItem("complete_train");
document.querySelector(".text_complete_train").innerHTML = text;

function makeid() {
    var text = "";
    var possible =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

const BROKER_URL = "e9b685676e514fb18a77577bc6449f0c.s1.eu.hivemq.cloud";
const PORT = 8884;
const USER_NAME = "thanhdai0411";
const PASSWORD = "thanhdai0411";
var client = new Paho.MQTT.Client(BROKER_URL, PORT, makeid());

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

var options_ = {
    useSSL: true,
    userName: USER_NAME,
    password: PASSWORD,
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
                    toastFail("Vui lòng đăng kí email để nhạn được thông báo");
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
    if (topic == "fish_die") {
        let today = new Date();
        const countDie = message.payloadString;

        const dateDie = moment(today).format("DD/MM/YYYY HH:mm:ss");
        const text = `[${dateDie}]: Phát hiện ${countDie} cá chết`;
        console.log({ text });
        apiSendMail(text);
    } else if (topic === "start_eat") {
        let payload = message.payloadString;
        if (Number(payload) != 0) {
            let stateTrain = message.payloadString;
            let id = stateTrain.split("=")[0];

            document.getElementById("camera_open").src = "/camera/count_fish";
            localStorage.setItem("id_food_run", id);
        } else if (Number(payload) == 0) {
            document.getElementById("camera_open").src = "/camera/fish_die";

            let id = localStorage.getItem("id_food_run");

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
                        toastSuccessFood(`Cho cá ăn thành công`);
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
        console.log({ state, time });

        if (state == "Start") {
            toastSuccess(`Bắt đầu tiến hành huấn luyện vào lúc ${time}`);

            setTimeout(function () {
                location.reload();
            }, 2000);
        }
        if (state == "End") {
            let content = `Hoàn thành đặt tên cho cá gần đây nhất vào lúc ${time}`;
            localStorage.setItem("complete_train", content);
            document.querySelector(".text_complete_train").innerHTML = content;
            toastSuccess(`Hoàn thành đặt tên cho cá`);
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
