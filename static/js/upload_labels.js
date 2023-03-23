//! get coordinates
let result = document.querySelector(".result"),
    img_result = document.querySelector(".img-result"),
    img_w = document.querySelector(".img-w"),
    img_h = document.querySelector(".img-h"),
    options = document.querySelector(".options"),
    cropped = document.querySelector(".cropped"),
    dwn = document.querySelector(".download"),
    upload = document.querySelector("#file-input"),
    cropper = "";

const toastUploadSuccess = document.querySelector("#toastUploadLabel");
const toastUploadFail = document.querySelector("#toastUploadLabelFail");

const timeUpload = document.querySelector(".time_upload");
const toastContentSuccess = document.querySelector("#toast_success_body");

const timeUploadFail = document.querySelector(".time_upload_fail");
const toastContentFail = document.querySelector("#toast_fail_body");

let coorDinates = document.querySelector(".coordinates");
let x, y, w, h;

// const getData = async () => {
//     let data = await axios.get('https://jsonplaceholder.typicode.com/todos/1');
// };

function getCookie(name) {
    function escape(s) {
        return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, "\\$1");
    }
    var match = document.cookie.match(
        RegExp("(?:^|;\\s*)" + escape(name) + "=([^;]*)")
    );
    return match ? match[1] : null;
}

// const usernameLogin = getCookie("username").split('"')[1];
// document.querySelector("#username_login").innerHTML = usernameLogin;

//========================zz===================================================

let imgUploadName = "";
$(".box-2").hide();
upload.addEventListener("change", (e) => {
    $(".box-2").show();
    if (e.target.files.length) {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (e.target.result) {
                let img = document.createElement("img");

                console.log(img);
                img.id = "image";
                img.src = e.target.result;
                result.innerHTML = "";
                result.appendChild(img);
                // save.classList.remove('hide');

                cropper = new Cropper(img, {
                    aspectRatio: 0,
                    viewMode: 0,
                    zoomOnWheel: false,
                    crop(event) {
                        const widthImage = event.srcElement.naturalWidth;
                        const heightImage = event.srcElement.naturalHeight;

                        const widthBox = event.detail.width;
                        const hightBox = event.detail.height;

                        const xTopLeft = event.detail.x;
                        const yTopLeft = event.detail.y;

                        x = (+xTopLeft + widthBox / 2) / +widthImage;
                        y = (+yTopLeft + hightBox / 2) / +heightImage;

                        w = widthBox / widthImage;
                        h = hightBox / heightImage;
                    },
                });
            }
        };
        imgUploadName = e.target.files[0].name;
        reader.readAsDataURL(e.target.files[0]);
    }
});

//! end get coordinates

//!util
const getTimePresent = () => {
    let today = new Date();
    let timePresent =
        today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var datePresent = today.getDate() + "/" + (today.getMonth() + 1);
    return { timePresent, datePresent };
};

const toastFail = (message) => {
    const { datePresent, timePresent } = getTimePresent();
    timeUploadFail.innerHTML = timePresent + " - " + datePresent;
    toastContentFail.innerHTML = message;
    const toast = new bootstrap.Toast(toastUploadFail);
    toast.show();
};

const toastSuccess = (message) => {
    const { datePresent, timePresent } = getTimePresent();
    timeUpload.innerHTML = timePresent + " - " + datePresent;
    toastContentSuccess.innerHTML = message;
    const toast = new bootstrap.Toast(toastUploadSuccess);
    toast.show();
};

//! end util

//! save label into storage
const btnSaveLabel = document.querySelector("#btn_save_label");
const btnSubmitLabel = document.querySelector(".save");
const inputLabel = document.querySelector("#input_label");
const labelPresent = document.querySelector("#label_present");
const btnShowLabel = document.querySelector("#btn_show_label");
const wrapLabelShow = document.querySelector("#label_show");
const tableBody = document.querySelector("#table_body");

const modalDeleteFishName = document.querySelector("#modalDeleteFishName");

labelPresent.innerHTML = localStorage.getItem("label");

const handleDeleteFishName = (btnDeleteData) => {
    btnDeleteData.forEach((btn, index) => {
        btn.onclick = (e) => {
            // const fishName = btn.getAttribute('data-name-fish');
            // const userNameLogin = document.querySelector('#username_login').innerHTML;
            // $.ajax({
            //     type: 'DELETE',
            //     url: `/label/delete/${userNameLogin}/${fishName}`,
            //     dataType: 'json',
            //     success: function (v) {
            //         const { data } = v;
            //         console.log({ delete: data })
            //     },
            // });
        };
    });
};

modalDeleteFishName.addEventListener("show.bs.modal", (event) => {
    // Button that triggered the modal
    const button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    const recipient = button.getAttribute("data-name-fish");
    const nameFish = localStorage.getItem("label");

    const btnDeleteFishNameComplete = modalDeleteFishName.querySelector(
        "#btn_delete_fish_name"
    );
    const textConfirm = modalDeleteFishName.querySelector(
        "#text_confirm_delete_label"
    );
    textConfirm.innerHTML = `You definitely want to remove the name ${recipient}. When deleting all data about the name ${recipient} will be lost`;
    var bodyFormData = new FormData();

    bodyFormData.append("name_fish", nameFish);
    bodyFormData.append("action", "DELETE");
    btnDeleteFishNameComplete.onclick = () => {
        $.ajax({
            type: "POST",
            url: "/upload/train",
            data: bodyFormData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log({ train: data });

                if (data == "TRAIN_BUSY") {
                    toastFail("The system is busy at the moment");
                } else if (data == "NOT_LABEL_TRAIN") {
                    toastFail("Not data train name");
                }
            },
        });

        $("#modalDeleteFishName").modal("hide");
    };
});

btnShowLabel.onclick = (e) => {
    const userNameLogin = document.querySelector("#username_login").innerHTML;

    $.ajax({
        type: "GET",
        url: `/label/get/${userNameLogin}`,
        dataType: "json",
        success: function (data) {
            const { data: labelFish, success } = data;
            if (success === 1) {
                const labelSave = JSON.parse(labelFish);
                if (labelSave.length) {
                    const tableContent = labelSave.map(
                        (v, index) =>
                            `
                                <tr class="text-center">
                                    <td id="name_label_show"  >${v.name}</td>
                                    <td style="font-size: 14px;">${moment(
                                        v.created_at.$date
                                    ).format("DD/MM/YYYY, HH:mm:ss")}
                                    </td>
                                    <td>
                                        <button id="btn_add_data"
                                            style="border: none; background-color: orange ; border-radius: 5px; font-size: 14px ; font-weight: 500; color : white; ">ADD</button>
                                        <button id="btn_delete_data" data-name-fish="${
                                            v.name
                                        }"
                                            style="border: none; background-color: red ; border-radius: 5px;font-size: 15px ; font-weight: 500; color : white; " data-bs-toggle="modal" data-bs-target="#modalDeleteFishName">DELETE</button>
                                        
                                    </td>
                                </tr>`
                    );
                    tableBody.innerHTML = tableContent.join("");
                    const btnAddData =
                        document.querySelectorAll("#btn_add_data");
                    const btnDeleteData =
                        document.querySelectorAll("#btn_delete_data");
                    const nameLabelShow =
                        document.querySelectorAll("#name_label_show");
                    btnAddData.forEach((btn, index) => {
                        btn.onclick = (e) => {
                            let nameFishAdd = nameLabelShow[index].innerHTML;
                            localStorage.setItem("label", nameFishAdd);
                            labelPresent.innerHTML = nameFishAdd;
                            $("#modalShowLabel").modal("hide");
                        };
                    });

                    handleDeleteFishName(btnDeleteData);
                } else {
                    // khong co
                    wrapLabelShow.innerHTML = "Not train status";
                }
            } else {
                // that bai
                wrapLabelShow.innerHTML = "Not train status";
            }
        },
    });
};

btnSaveLabel.onclick = (e) => {
    const userNameLogin = document.querySelector("#username_login").innerHTML;

    const nameFishTrain = localStorage.getItem("label");

    if (inputLabel.value == "") {
        // alert('Vui lòng nhập tên mới nhấp lưu');
        toastFail("Please enter a new name and click save");
        $("#modalSaveName").modal("hide");

        return;
    }
    const valueInputLabel = inputLabel.value.replace(/\s/g, "");

    if (!valueInputLabel) {
        toastFail("Please enter an invalid name or username");
        $("#modalSaveName").modal("hide");
    }

    if (valueInputLabel == nameFishTrain) {
        toastFail("Tên dã tồn tại");
        $("#modalSaveName").modal("hide");
        return;
    }

    $.ajax({
        type: "GET",
        url: `/label/get/${userNameLogin}`,
        dataType: "json",
        success: function (data) {
            console.log({ data });
            const { data: labelFish, success } = data;
            if (success === 1) {
                const labelSave = JSON.parse(labelFish);

                console.log({ labelSave });

                let exist = false;
                if (labelSave.length > 0) {
                    labelSave.forEach((v) => {
                        if (valueInputLabel == v.name) {
                            toastFail("Tên đã tồn tại");
                            $("#modalSaveName").modal("hide");
                            exist = true;
                            return;
                        }
                    });
                    if (!exist) {
                        localStorage.setItem("label", valueInputLabel);
                        labelPresent.innerHTML = valueInputLabel;
                        toastSuccess(
                            "Save the pet name successfully. Now you can download image data"
                        );

                        $("#modalSaveName").modal("hide");
                    }
                } else {
                    console.log("2");

                    $("#modalSaveName").modal("hide");
                    toastSuccess(
                        "Save the pet name successfully. Now you can download image data"
                    );

                    localStorage.setItem("label", valueInputLabel);
                    labelPresent.innerHTML = valueInputLabel;
                    return;
                }
            } else {
                toastFail("Lỗi");
                $("#modalSaveName").modal("hide");
            }
        },
    });
};

//! end save label into storage

//! post label

btnSubmitLabel.addEventListener("click", (e) => {
    console.log(123);
    const labelStorage = localStorage.getItem("label");

    if (!labelStorage) {
        toastFail("Please name the fish before uploading the image");
        return;
    }

    const userNameLogin = document.querySelector("#username_login").innerHTML;

    let check = $("#file-input").val();
    if (check == "") {
        toastFail("Please select photo and fish area before saving data");
        return;
    }
    const coordinatesBox = `${x.toFixed(6)} ${y.toFixed(6)} ${w.toFixed(
        6
    )} ${h.toFixed(6)}`;

    imgUploadName = imgUploadName.split(".")[0];
    // coorDinates.innerHTML = 0 + ' ' + coordinatesBox;

    var bodyFormData = new FormData($("#upload_file")[0]);

    bodyFormData.append("coordinates", coordinatesBox);
    bodyFormData.append("label", labelStorage);
    bodyFormData.append("image_name", imgUploadName);
    bodyFormData.append("username", userNameLogin);

    // var form_data = new FormData();
    // bodyFormData.append('file', $('#upload_file').prop('files')[0]);

    // if()
    $.ajax({
        type: "POST",
        url: "/upload/labels",
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            console.log({ data });
            if (data == "FAIL") {
                toastFail("Picture already exists");
            } else if (data == "EXIST_LABEL") {
                toastFail("Name already exists");
            } else if (data == "LIMIT_LABEL") {
                toastFail("Name fish maximum is 5");
            } else {
                $("#file-input").val("");
                $(".box-2").hide();

                const { datePresent, timePresent } = getTimePresent();

                timeUpload.innerHTML = timePresent + " - " + datePresent;
                const toast = new bootstrap.Toast(toastUploadSuccess);
                toast.show();
                toastSuccess("Download data successfully");
            }
        },
    });
});
//! end post label
const btnComplete = document.querySelector("#btn_complete");
const viewDataPresentForTrain = document.querySelector(
    "#data_present_for_train"
);

btnComplete.onclick = (e) => {
    const MIN_TRAIN = 2;
    const minTrainLabel = document.querySelector("#min_train_label");
    minTrainLabel.innerHTML = MIN_TRAIN;
    const nameFish = localStorage.getItem("label");
    const btnAgreeTrain = document.querySelector("#btn_agree_train");

    if (!nameFish) {
        $("#modalAuthTrain").modal("hide");
        $("#btn_agree_train").hide();

        // $("#modalAuthTrain").modal("hide");
        toastFail("No name for training yet");
        return;
    }
    $.ajax({
        type: "GET",
        url: `/label/get/data_fish/${nameFish}`,
        dataType: "json",
        success: function (v) {
            const { data } = v;
            let content = "";
            if (data < MIN_TRAIN) {
                content = `Currently the data for the name ${nameFish} is ${v.data} figure. Not enough to train`;
                $("#btn_agree_train").hide();
            } else {
                content = `Currently the data for the name ${nameFish} is ${v.data} image`;
                $("#btn_agree_train").show();
            }

            viewDataPresentForTrain.innerHTML = content;
        },
    });

    var bodyFormData = new FormData();

    bodyFormData.append("name_fish", nameFish);
    bodyFormData.append("action", "TRAIN");

    btnAgreeTrain.onclick = (e) => {
        $.ajax({
            type: "POST",
            url: "/upload/train",
            data: bodyFormData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log({ train: data });
                if (data == "TRAIN_BUSY") {
                    toastFail("The system is busy at the moment");
                } else if (data == "NOT_LABEL_TRAIN") {
                    toastFail("Not data train name");
                }
            },
        });

        $("#modalAuthTrain").modal("hide");
    };
};

//! status train

const btnShowStatusTrain = document.getElementById("show_status_train");
const tableStatusTrain = document.getElementById("table_status_train");
btnShowStatusTrain.onclick = (e) => {
    const userNameLogin = document.querySelector("#username_login").innerHTML;

    $.ajax({
        type: "GET",
        url: `/status_train/get/${userNameLogin}`,
        dataType: "json",
        success: function (data) {
            const { data: statusTrain, success } = data;
            if (success === 1) {
                const status = JSON.parse(statusTrain);
                if (status.length) {
                    const tableContent = status.map((v, index) => {
                        let style =
                            v.status === "WAITING"
                                ? "#e8733b"
                                : v.status === "COMPLETE"
                                ? "#54B435"
                                : "#8B7E74";

                        return `
                                <tr class="text-center">
                                    <td id="name_label_show" style="font-size: 15px;"   >${
                                        v.name_fish
                                    }</td>
                                    <td  style="font-size: 15px;">${
                                        v.dateStart
                                    }</td>
                                    <td  style="font-size: 15px;">${
                                        v.dateEnd ? v.dateEnd : "Process..."
                                    }</td>
                                    <td>
                                        <span style="border-radius : 5px ; padding: 3px;font-size: 15px; background-color : ${style}; color : white ;font-weight : 500 ">${
                            v.status
                        }</span>
                                    </td>
                                    <td  style="font-size: 15px;"> <span>${
                                        v.action
                                    }</span> </td>
                                    
                                </tr>`;
                    });
                    tableStatusTrain.innerHTML = tableContent.join("");
                } else {
                    // khong co
                    tableStatusTrain.innerHTML = "Not train status";
                }
            } else {
                // that bai
                tableStatusTrain.innerHTML = "Not train status";
            }
        },
    });

    const btnClearStatus = document.querySelector("#btn_clear_status_train");
    btnClearStatus.onclick = () => {
        $.ajax({
            type: "GET",
            url: `/status_train/delete/${userNameLogin}`,
            dataType: "json",
            success: function (data) {
                $("#modalNoti").modal("hide");
                renderNotifyMain();
            },
        });
        $("#modalStatusTrain").modal("hide");
    };
};
