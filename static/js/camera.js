const btnStopCamera = document.querySelector(".btn_stop_camera");
const btnStartCamera = document.querySelector(".btn_start_camera");
const btnDetectCamera = document.querySelector(".btn_detect_camera");

const shapeCameraNone = document.querySelector("#shape_camera_none");

const camera = document.querySelector("#camera_open");
const cameraFishDie = document.querySelector("#camera_fish_die");

// $('#shape_camera_none').show();
shapeCameraNone.style.display = "flex";
$("#loading_open_camera").hide();
$("#shape_camera").hide();
// $("#shape_camera_fish_die").hide();
// console.log(camera.src);
let check_cam = camera.src.split("/");

if (check_cam[3] == "camera" && check_cam[4] == "fish_die") {
    $("#shape_camera_none").show();
    $("#shape_camera").hide();
    $("#loading_open_camera").hide();
    $(".camera-btn_group").show();
}

const callOpenCamera = (url) => {
    $.ajax({
        timeout: 100000,
        type: "GET",
        url: url,
        dataType: "json",
        success: function ({ data }) {},
        error: function (jqXHR, textStatus, errorThrown) {
            if (textStatus === "timeout") {
                console.log({
                    jqXHR,
                    textStatus,
                    errorThrown,
                });
                //do something on timeout / show appropriate message.
            }
        },
    });
};

const hideCamera = () => {
    camera.setAttribute("src", "");
    $("#shape_camera").hide();
    shapeCameraNone.style.display = "flex";
    $(".camera-btn_group").hide();
    $("#loading_open_camera").show();
};

const stopCamera = () => {
    hideCamera();
    $("#loading_open_camera").hide();
    $(".camera-btn_group").show();
};

const showCamera = (src) => {
    $("#shape_camera_none").hide();
    $("#shape_camera").show();
    // $("#loading_open_camera").hide();
    // $(".camera-btn_group").show();
    camera.setAttribute("src", src);
};
const showCameraNoteFrame = (src) => {
    // $("#shape_camera_none").show();
    $("#shape_camera").hide();
    // $("#loading_open_camera").hide();
    // $(".camera-btn_group").show();
    camera.setAttribute("src", src);
};

btnStartCamera.onclick = (e) => {
    // $("#opacity_loading_page").show();
    hideCamera();
    // callOpenCamera("/camera/play");
    setTimeout(() => {
        showCamera("/camera/video");
    }, 1000);
};

btnStopCamera.onclick = (e) => {
    stopCamera();

    // hideCamera();

    // setTimeout(() => {
    //     showCamera("/camera/count_fish");
    // }, 1000);
};

btnDetectCamera.onclick = (e) => {
    // $("#opacity_loading_page").show();
    hideCamera();
    setTimeout(() => {
        showCamera("/camera/detect");
    }, 1000);
};
