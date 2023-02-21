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
const btnDeleteFishNameComplete = document.querySelector(
    "#btn_delete_fish_name"
);

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

    btnDeleteFishNameComplete.onclick = () => {
        console.log({ recipient });
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
                                    <th scope="row">${index}</th>
                                    <td id="name_label_show"  >${v.name}</td>
                                    <td>${moment(v.created_at.$date).format(
                                        "DD/MM/YYYY, HH:mm:ss"
                                    )}
                                    </td>
                                    <td>
                                        <button id="btn_add_data"
                                            style="border: none; background-color: orange ; border-radius: 5px">ADD</button>
                                        <button id="btn_delete_data" data-name-fish=${
                                            v.name
                                        } data-bs-toggle="modal" data-bs-target="#modalDeleteFishName"
                                            style="border: none; background-color: red ; color : white ; border-radius: 5px">DELETE</button>
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
                    wrapLabelShow.innerHTML =
                        "Hiện bạn chưa có tên nào trong hệ thống";
                }
            } else {
                // that bai
                wrapLabelShow.innerHTML =
                    "Hiện bạn chưa có tên nào trong hệ thống";
            }
        },
    });

    const handleClickAddData = (e) => {
        console.log(e);
    };
};

btnSaveLabel.onclick = (e) => {
    const userNameLogin = document.querySelector("#username_login").innerHTML;

    const nameFishTrain = localStorage.getItem("label");

    if (inputLabel.value == "") {
        // alert('Vui lòng nhập tên mới nhấp lưu');
        toastFail("Vui lòng nhập tên mới nhấp lưu");
        $("#modalSaveName").modal("hide");

        return;
    }
    const valueInputLabel = inputLabel.value.replace(/\s/g, "");

    if (!valueInputLabel) {
        toastFail("Vui lòng nhập tên hoặc tên nhập không hợp lệ");
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
                            "Lưu tên thú cưng thành công. Bây giờ bạn có thể tải dữ liệu hình ảnh"
                        );

                        $("#modalSaveName").modal("hide");
                    }
                } else {
                    console.log("2");

                    $("#modalSaveName").modal("hide");
                    toastSuccess(
                        "Lưu tên thú cưng thành công. Bây giờ bạn có thể tải dữ liệu hình ảnh"
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
        toastFail("Vui lòng đặt tên cho cá trước khi upload image");
        return;
    }

    const userNameLogin = document.querySelector("#username_login").innerHTML;

    let check = $("#file-input").val();
    if (check == "") {
        toastFail("Vui lòng chọn ảnh và khoanh vùng cá trước khi lưu dữ liệu");
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
                toastFail("Ảnh đã tồn tại");
            } else {
                $("#file-input").val("");
                $(".box-2").hide();

                const { datePresent, timePresent } = getTimePresent();

                timeUpload.innerHTML = timePresent + " - " + datePresent;
                const toast = new bootstrap.Toast(toastUploadSuccess);
                toast.show();
                toastSuccess("Tải dữ liệu thành công");
            }
        },
    });
});
//! end post label
const btnComplete = document.querySelector("#btn_complete");
const viewDataPresentForTrain = document.querySelector(
    "#data_present_for_train"
);
const btnAgreeTrain = document.querySelector("#btn_agree_train");

btnComplete.onclick = (e) => {
    const nameFish = localStorage.getItem("label");
    $.ajax({
        type: "GET",
        url: `/label/get/data_fish/${nameFish}`,
        dataType: "json",
        success: function (v) {
            const { data } = v;
            let content = "";
            if (data < 10) {
                content = `Hiện tại dữ liệu cho tên ${nameFish} là ${v.data} hình. Chưa đủ để huấn luyện`;
                $("#btn_agree_train").hide();
            } else {
                content = `Hiện tại dữ liệu cho tên ${nameFish} là ${v.data} hình`;
                $("#btn_agree_train").show();
            }

            viewDataPresentForTrain.innerHTML = content;
        },
    });
};
