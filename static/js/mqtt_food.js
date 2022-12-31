const toastStart = document.getElementById('toastStart');
const toastEnd = document.getElementById('toastEnd');

const timeStartToast = document.querySelector('.time_start_toast');
const timeEndToast = document.querySelector('.time_end_toast');

const toastBodyStart = document.querySelector('.toast-body-start');
const toastBodyEnd = document.querySelector('.toast-body-end');
// !================================
const toastFoodFail = document.querySelector('#toastUploadLabelFail');
const toastFoodSuccess = document.querySelector('#toastUploadLabel');

const timeFoodUpload = document.querySelector('.time_upload');
const toastContentSuccessFood = document.querySelector('#toast_success_body');

const timeFoodFail = document.querySelector('.time_upload_fail');
const toastContentFailFood = document.querySelector('#toast_fail_body');
const getTimePresentFood = () => {
    let today = new Date();
    let timePresent = today.getHours() + ':' + today.getMinutes();
    var datePresent = today.getDate() + '/' + (today.getMonth() + 1);
    return { timePresent, datePresent };
};
const toastFailFood = (message) => {
    const { datePresent, timePresent } = getTimePresentFood();
    timeFoodFail.innerHTML = timePresent + ' - ' + datePresent;
    toastContentFailFood.innerHTML = message;
    const toast = new bootstrap.Toast(toastFoodFail);
    toast.show();
};

const toastSuccessFood = (message) => {
    const { datePresent, timePresent } = getTimePresentFood();
    timeFoodUpload.innerHTML = timePresent + ' - ' + datePresent;
    toastContentSuccessFood.innerHTML = message;
    const toast = new bootstrap.Toast(toastFoodSuccess);
    toast.show();
};

let text = localStorage.getItem('complete_train');

function makeid() {
    var text = '';
    var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (var i = 0; i < 5; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

const BROKER_URL = 'e9b685676e514fb18a77577bc6449f0c.s1.eu.hivemq.cloud';
const PORT = 8884;
const USER_NAME = 'thanhdai0411';
const PASSWORD = 'thanhdai0411';
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

console.log('Waiting Connect to broker....');
client.connect(options_);

function doFail(e) {
    console.log(e);
}

function onConnect() {
    console.log('Connect page Monitor successful');
    client.subscribe('food_complete');
    client.subscribe('Train_model');
}

function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log(responseObject.errorMessage);
    }
}

function onMessageArrived(message) {
    console.log('>>>>>>>>>  ' + message.destinationName + ': ' + message.payloadString);

    let stateTrain = message.payloadString;
    let id = stateTrain.split('=')[0];
    let status = stateTrain.split('=')[1];

    var bodyFormData = new FormData();

    bodyFormData.append('status', status);

    $.ajax({
        type: 'POST',
        url: `/food/update_status/${id}`,
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data === 'OK') {
                getValue();
                toastSuccessFood(`Cho cá ăn thành công`);
                $('#modalEditFood').modal('hide');
            }
        },
    });

    let state = stateTrain.split('/')[0];
    let time = stateTrain.split('/')[1];

    if (state == 'Start') {
        timeStartToast.innerHTML = time;
        const toast = new bootstrap.Toast(toastStart);
        toast.show();

        setTimeout(function () {
            location.reload();
        }, 5000);
    }
    if (state == 'End') {
        timeEndToast.innerHTML = time;
        let content = `Hoàn thành đặt tên cho cá gần đây nhất vào lúc ${time}`;
        localStorage.setItem('complete_train', content);

        const toast = new bootstrap.Toast(toastEnd);
        toast.show();
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

//! handle control

const switchForFishEat = document.getElementById('for_fish_eat');
const textForFishEat = document.getElementById('text-for_fish_eat');
const stateForFishEat = document.querySelector('.state-for_fish_eat');

const switchAIForFishEat = document.getElementById('ai_fish_eat');
const textAI = document.getElementById('text-ai_fish_eat');
const stateAI = document.querySelector('.state-ai_fish_eat');

const onOffDevice = document.getElementById('on_off_device');
const textDevice = document.getElementById('text-on_off_device');
const stateDevice = document.querySelector('.state-on_off_device');

const stateOff = (input, text, state) => {
    input.removeAttribute('checked');
    text.innerHTML = 'OFF';
    state.classList.add('control_switch-off');
    state.classList.remove('control_switch');
};
const stateOn = (input, text, state) => {
    input.setAttribute('checked', true);
    text.innerHTML = 'ON';
    state.classList.add('control_switch');
    state.classList.remove('control_switch-off');
};

const stateSwitch = (input, text, state, local) => {
    let isAttributeCheck = input.getAttribute('checked');
    if (isAttributeCheck === 'true') {
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
        if (v == 'switchAIForFishEat' && localState == 1) {
            stateOn(switchAIForFishEat, textAI, stateAI);
        } else if (v == 'switchForFishEat' && localState == 1) {
            stateOn(switchForFishEat, textForFishEat, stateForFishEat);
        } else if (v == 'onOffDevice' && localState == 1) {
            stateOn(onOffDevice, textDevice, stateDevice);
        }
    });
};
stateSave(['switchAIForFishEat', 'switchForFishEat', 'onOffDevice']);

// ai for fish eat
switchAIForFishEat.onchange = (e) => {
    let state = stateSwitch(switchAIForFishEat, textAI, stateAI, 'switchAIForFishEat');
    getValue();
    public_message('control_ai_food', state.toString());
};

// for fish eat
switchForFishEat.onchange = (e) => {
    let state = stateSwitch(switchForFishEat, textForFishEat, stateForFishEat, 'switchForFishEat');
    console.log({ state_food: state });
    public_message('control_food', state.toString());
};

// control device
onOffDevice.onchange = (e) => {
    let state = stateSwitch(onOffDevice, textDevice, stateDevice, 'onOffDevice');
    console.log({ state });
    public_message('control_lamp', state.toString());
};

//! end handle control
