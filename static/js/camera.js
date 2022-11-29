const btnStopCamera = document.querySelector('.btn_stop_camera');
const btnStartCamera = document.querySelector('.btn_start_camera');
const btnDetectCamera = document.querySelector('.btn_detect_camera');

const camera = document.querySelector('#camera_open');

$('#shape_camera_none').show();
$('#loading_open_camera').hide();
$('#shape_camera').hide();

btnStartCamera.onclick = (e) => {
    var bodyFormData = new FormData();

    bodyFormData.append('start', 1);
    $('#loading_open_camera').show();
    $('.camera-btn_group').hide();

    $.ajax({
        type: 'GET',
        url: '/camera/play',
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            $('#shape_camera').show();
            $('#shape_camera_none').hide();
            $('#loading_open_camera').hide();
            $('.camera-btn_group').show();
            camera.setAttribute('src', '/camera/video');
        },
    });
};

btnStopCamera.onclick = (e) => {
    var bodyFormData = new FormData();

    bodyFormData.append('stop', 1);

    $.ajax({
        type: 'GET',
        url: '/camera/stop',
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            $('#shape_camera').hide();
            $('#shape_camera_none').show();
            camera.setAttribute('src', '');
        },
    });
};

btnDetectCamera.onclick = (e) => {
    var bodyFormData = new FormData();

    bodyFormData.append('detect', 1);

    $('#loading_open_camera').show();
    $('.camera-btn_group').hide();

    $.ajax({
        type: 'GET',
        url: '/camera/play',
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            $('#shape_camera').show();
            $('#shape_camera_none').hide();
            $('#loading_open_camera').hide();
            $('.camera-btn_group').show();
            camera.setAttribute('src', '/camera/detect');
        },
    });
};
