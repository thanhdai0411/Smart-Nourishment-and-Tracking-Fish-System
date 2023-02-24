const amountFood = document.querySelector("#amount_food");
const timeSet = document.querySelector("#set_time");
const btnSaveSettingFood = document.querySelector("#button_save_food");
const btnCompleteSetting = document.querySelector("#btn_complete_setting");
const labelSettingFood = document.querySelector("#label_btn_setting_food");

const chartElement = document.querySelector(".highcharts-figure");

const valueRenderSetting = document.querySelector(".value_setting");
const tableBodyFood = document.querySelector("#table_body_food");

//!util

// const toastUploadFailFood = document.querySelector("#toastUploadLabelFail");
// const toastUploadSuccessFood = document.querySelector("#toastUploadLabel");

// const timeUploadFood = document.querySelector(".time_upload");
// const toastContentSuccessFood = document.querySelector("#toast_success_body");

// const timeUploadFailFood = document.querySelector(".time_upload_fail");
// const toastContentFailFail = document.querySelector("#toast_fail_body");

const getTimeSettingFood = () => {
    let today = new Date();
    let timePresent = today.getHours() + ":" + today.getMinutes();
    var datePresent = today.getDate() + "/" + (today.getMonth() + 1);
    const datePresentReverse = moment(today).format("MM/DD/YYYY");

    return { timePresent, datePresent, datePresentReverse };
};
// const toastFailFood = (message) => {
//     const { datePresent, timePresent } = getTimePresentFood();
//     timeUploadFailFood.innerHTML = timePresent + " - " + datePresent;
//     toastContentFailFail.innerHTML = message;
//     const toast = new bootstrap.Toast(toastUploadFailFood);
//     toast.show();
// };

// const toastSuccessFood = (message) => {
//     const { datePresent, timePresent } = getTimePresentFood();
//     timeUploadFood.innerHTML = timePresent + " - " + datePresent;
//     toastContentSuccessFood.innerHTML = message;
//     const toast = new bootstrap.Toast(toastUploadSuccessFood);
//     toast.show();
// };

const userNameLogin = document.querySelector("#username_login").innerHTML;

// edit setting food
const modalEditFood = document.getElementById("modalEditFood");
const modalDeleteFood = document.getElementById("modalDeleteFood");
const timeFoodEdit = document.getElementById("time_food_edit");
const amountFoodEdit = document.getElementById("amount_food_edit");

const btnCompleteEdit = document.getElementById("btn_complete_edit");
const btnCompleteDelete = document.getElementById("btn_complete_delete");

const loadingDeleteFood = document.getElementById("loading_delete_food");
const loadingEditFood = document.getElementById("loading_edit_food");

// edit food

$("#loading_delete_food").hide();
$("#loading_edit_food").hide();

modalEditFood.addEventListener("show.bs.modal", (event) => {
    const button = event.relatedTarget;

    const id = button.getAttribute("data-id-food");
    const time = button.getAttribute("data-time-food");
    const amount = button.getAttribute("data-amount-food");
    const settingFoods = JSON.parse(localStorage.getItem("setting_food"));

    timeFoodEdit.value = time;
    amountFoodEdit.value = amount;

    const { datePresentReverse } = getTimePresentFood();

    btnCompleteEdit.onclick = (e) => {
        $("#loading_edit_food").show();
        btnCompleteEdit.classList.add("d-none");
        const completeTimeEdit = timeFoodEdit.value;
        const completeAmountEdit = amountFoodEdit.value;

        if (completeTimeEdit === time) {
            toastFailFood("Sửa đổi thất bại. Bạn không có sự thay đổi nào");
            $("#modalEditFood").modal("hide");
            $("#loading_edit_food").hide();
            btnCompleteEdit.classList.remove("d-none");

            return;
        }

        // check time set

        let checkData = [];
        settingFoods.forEach((value) => {
            if (value.time != time) {
                var date2 = new Date(`${datePresentReverse} ${value.time}`);
                var date1 = new Date(
                    `${datePresentReverse} ${completeTimeEdit}`
                );
                const { hh, mm } = checkTimeSet(date1, date2);
                if (hh == 0 && mm < 30) {
                    // let data = `${hh}:${mm}`
                    checkData.push(1);
                } else {
                    checkData.push(2);
                }
            } else if (value.time == time && settingFoods.length == 1) {
                checkData.push(2);
            }
        });
        console.log(checkData);

        // end check time set

        if (checkData.length && !checkData.includes(1)) {
            var bodyFormData = new FormData();

            bodyFormData.append("time", completeTimeEdit);
            bodyFormData.append("amount_food", completeAmountEdit);
            bodyFormData.append("username", userNameLogin);
            $.ajax({
                type: "POST",
                url: `/food/update/${id}`,
                data: bodyFormData,
                contentType: false,
                cache: false,
                processData: false,
                success: function (data) {
                    if (data === "OK") {
                        getValue();
                        toastSuccessFood("Sửa đổi thành công");

                        btnCompleteEdit.classList.remove("d-none");
                        $("#loading_edit_food").hide();
                        $("#modalEditFood").modal("hide");
                    } else {
                        toastFailFood("Sửa đổi thất bại");
                        $("#modalEditFood").modal("hide");
                    }
                },
            });
        } else {
            toastFailFood(
                "Sửa thất bại. Các mốc thời gian phải cách nhau 30 phút"
            );
            $("#modalEditFood").modal("hide");
            $("#loading_edit_food").hide();
            btnCompleteEdit.classList.remove("d-none");
        }
    };
});
// end edit setting food

// delete food
modalDeleteFood.addEventListener("show.bs.modal", (event) => {
    const button = event.relatedTarget;

    const id = button.getAttribute("data-id-food");

    btnCompleteDelete.onclick = (e) => {
        $("#loading_delete_food").show();
        btnCompleteDelete.classList.add("d-none");

        $.ajax({
            type: "DELETE",
            url: `/food/delete/${id}`,
            dataType: "json",
            success: function (data) {
                if (data.success == 1) {
                    getValue();
                    toastSuccessFood("Xóa thành công");

                    btnCompleteDelete.classList.remove("d-none");
                    $("#loading_delete_food").hide();
                    $("#modalDeleteFood").modal("hide");
                } else {
                    $("#modalDeleteFood").modal("hide");
                    toastFailFood("Xóa thất bại");
                }
            },
        });
    };
});
// end delete setting food

// get render value when reload
const modeAI = localStorage.getItem("switchAIForFishEat");

const getValue = () => {
    const modeAI = localStorage.getItem("switchAIForFishEat");
    const settingFoodLocal = JSON.parse(localStorage.getItem("setting_food"));
    const settingFoodLength = localStorage.getItem("length_setting_food");

    if (modeAI == 1) {
        tableBodyFood.innerHTML = `<td colspan="5">Bạn đang trong chế đố cho ăn tự động bằng AI</td>`;
        chartElement.classList.add("d-none");

        return;
    }

    if (!userNameLogin) {
        tableBodyFood.innerHTML = `<td colspan="5">Có lỗi xảy ra. Vui lòng Logout và đăng nhập lại</td>`;
        return;
    }

    $.ajax({
        type: "GET",
        url: `/food/get/${userNameLogin}`,
        dataType: "json",
        success: function (data) {
            const { data: foods, success } = data;
            localStorage.setItem("setting_food", foods);
            let foodData = JSON.parse(foods);
            localStorage.setItem("length_setting_food", foodData.length);
            // location.reload();
            if (success === 1 && foodData.length > 0) {
                const tableContent = foodData.map((v, index) => {
                    let id = v._id.$oid;

                    let style =
                        v.status === "WAITING"
                            ? "#e8733b"
                            : v.status === "COMPLETE"
                            ? "#54B435"
                            : "#8B7E74";
                    return `
                                    <tr class="text-center">
                                        <th scope="row">${index + 1} </th>
                                        <td id="name_label_show"  >${
                                            v.time
                                        }</td>
                                        <td>${v.amount_food}</td>
                                        <td > <span style="border-radius : 5px ; background-color : ${style}; ">${
                        v.status
                    }</span></td>
                                    <td> <button class="btn_action_food" data-id-food="${id}" data-time-food="${
                        v.time
                    }" data-amount-food="${
                        v.amount_food
                    }" data-bs-toggle="modal" data-bs-target="#modalEditFood">EDIT</button> 
                                    <button class="btn_action_food_delete" data-id-food="${id}" data-bs-toggle="modal" data-bs-target="#modalDeleteFood">DELETE</button></td>
    
                                       
                                    </tr>`;
                });
                tableBodyFood.innerHTML = tableContent.join("");

                chartElement.classList.remove("d-none");
            } else {
                console.log("not data");
                tableBodyFood.innerHTML = `<td colspan="5">Chưa có cài đặt nào</td>`;
                // chartElement.classList.add('d-none');
            }
        },
    });
};

if (modeAI == 1) {
    tableBodyFood.innerHTML = `<td colspan="5">Bạn đang trong chế đố cho ăn tự động bằng AI</td>`;
    chartElement.classList.add("d-none");
} else {
    getValue();
}
// emd get render value when reload

const checkTimeSet = (date1, date2) => {
    var diff = date1.getTime() - date2.getTime();

    if (diff < 0) {
        diff = date2.getTime() - date1.getTime();
    }

    var msec = diff;
    var hh = Math.floor(msec / 1000 / 60 / 60);
    msec -= hh * 1000 * 60 * 60;
    var mm = Math.floor(msec / 1000 / 60);
    msec -= mm * 1000 * 60;

    var ss = Math.floor(msec / 1000);
    msec -= ss * 1000;

    return { hh, mm };
};

btnCompleteSetting.onclick = (e) => {
    const modeAI = localStorage.getItem("switchAIForFishEat");
    const settingFoods = JSON.parse(localStorage.getItem("setting_food"));
    const userNameLogin = document.querySelector("#username_login").innerHTML;
    const { datePresentReverse, timePresent } = getTimeSettingFood();

    const userTimeSet = timeSet.value;
    const userAmountFoodSet = amountFood.value;

    if (!userTimeSet) {
        toastFailFood("Vui lòng cài thời gian cho cá ăn");
        return;
    }

    if (!userAmountFoodSet) {
        toastFailFood("Vui lòng cài lượng thức ăn cho cá");
        return;
    }

    if (settingFoods.length > 10) {
        toastFailFood("Tối đa chỉ được 10 cài đặt");
        return;
    }

    if (modeAI == 1) {
        toastFailFood("Bạn đang trong chế độ cho ăn bằng AI không thể cài đặt");
        return;
    }

    //

    if (settingFoods && settingFoods.length > 0) {
        let checkData = [];
        settingFoods.forEach((value) => {
            var date2 = new Date(`${datePresentReverse} ${value.time}`);
            var date1 = new Date(`${datePresentReverse} ${userTimeSet}`);
            const { hh, mm } = checkTimeSet(date1, date2);
            console.log(hh + " : " + mm);
            if (hh == 0 && mm < 30) {
                // let data = `${hh}:${mm}`
                checkData.push(1);
            } else {
                checkData.push(2);
            }
        });
        console.log(checkData);

        if (checkData.length && !checkData.includes(1)) {
            var bodyFormData = new FormData();

            bodyFormData.append("time", userTimeSet);
            bodyFormData.append("amount_food", userAmountFoodSet);
            bodyFormData.append("username", userNameLogin);

            $.ajax({
                type: "POST",
                url: "/food/add",
                data: bodyFormData,
                contentType: false,
                cache: false,
                processData: false,
                success: function (data) {
                    if (data === "OK") {
                        getValue();
                        toastSuccessFood("Cài đặt thời gian cho ăn thành công");
                    } else if (data == "LIMIT") {
                        toastFailFood("Cài đặt tối đa là 10");
                    } else if (data == "EXIST_TIME") {
                        toastFailFood("Thời gian cài đặt đã tồn tại");
                    } else {
                        toastFailFood("Cài đặt thời gian cho ăn thất bại");
                    }
                },
            });
        } else {
            return toastFailFood("Các môc thời gian phải cách nhau 30 phút");
        }
    } else {
        var bodyFormData = new FormData();

        bodyFormData.append("time", userTimeSet);
        bodyFormData.append("amount_food", userAmountFoodSet);
        bodyFormData.append("username", userNameLogin);

        $.ajax({
            type: "POST",
            url: "/food/add",
            data: bodyFormData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (data === "OK") {
                    getValue();
                    toastSuccessFood("Cài đặt thời gian cho ăn thành công");
                } else if (data == "LIMIT") {
                    toastFailFood("Cài đặt tối đa là 10");
                } else if (data == "EXIST_TIME") {
                    toastFailFood("Thời gian cài đặt đã tồn tại");
                } else {
                    toastFailFood("Cài đặt thời gian cho ăn thất bại");
                }
            },
        });
    }
};
