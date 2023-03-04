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

btnStartCamera.onclick = (e) => {
    $("#shape_camera").show();
    $("#shape_camera_none").hide();
    $(".camera-btn_group").show();
    camera.setAttribute("src", "/camera/video");
    $("#loading_open_camera").hide();
};

btnStopCamera.onclick = (e) => {
    camera.setAttribute("src", "");
    $("#shape_camera").hide();
    shapeCameraNone.style.display = "flex";

    setTimeout(() => {
        $("#shape_camera").show();
        $("#shape_camera_none").hide();
    }, 5000);

    camera.setAttribute("src", "/camera/fish_die");
};

btnDetectCamera.onclick = (e) => {
    $("#shape_camera").show();
    $("#shape_camera_none").hide();
    $("#loading_open_camera").hide();
    $(".camera-btn_group").show();
    camera.setAttribute("src", "/camera/detect");
};
