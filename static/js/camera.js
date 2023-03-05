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

const hideCamera = () => {
    camera.setAttribute("src", "");
    $("#shape_camera").hide();
    shapeCameraNone.style.display = "flex";
    $(".camera-btn_group").hide();
    $("#loading_open_camera").show();
};

const showCamera = (src) => {
    $("#shape_camera_none").hide();
    $("#shape_camera").show();
    $("#loading_open_camera").hide();
    $(".camera-btn_group").show();
    camera.setAttribute("src", src);
};

btnStartCamera.onclick = (e) => {
    hideCamera();
    setTimeout(() => {
        showCamera("/camera/video");
    }, 5000);
};

btnStopCamera.onclick = (e) => {
    hideCamera();
    setTimeout(() => {
        showCamera("/camera/fish_die");
    }, 5000);
};

btnDetectCamera.onclick = (e) => {
    hideCamera();
    setTimeout(() => {
        showCamera("/camera/detect");
    }, 5000);
};
