const amountFood = document.querySelector("#amount_food");
const timeSet = document.querySelector("#set_time");
const btnSaveSettingFood = document.querySelector("#button_save_food");
const btnCompleteSetting = document.querySelector("#btn_complete_setting");
const labelSettingFood = document.querySelector("#label_btn_setting_food");

const chartElement = document.querySelector(".highcharts-figure");

const valueRenderSetting = document.querySelector(".value_setting");
const tableBodyFood = document.querySelector("#table_body_food");

//!util

const getTimeSettingFood = () => {
    let today = new Date();
    let timePresent = today.getHours() + ":" + today.getMinutes();
    var datePresent = today.getDate() + "/" + (today.getMonth() + 1);
    const datePresentReverse = moment(today).format("MM/DD/YYYY");

    return { timePresent, datePresent, datePresentReverse };
};
const userNameLogin = document.querySelector("#username_login").innerHTML;
console.log({ userNameLogin });
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
                        toastSuccessFood("Successful modification");

                        btnCompleteEdit.classList.remove("d-none");
                        $("#loading_edit_food").hide();
                        $("#modalEditFood").modal("hide");
                    } else {
                        toastFailFood("Modification failed");
                        $("#modalEditFood").modal("hide");
                    }
                },
            });
        } else {
            toastFailFood(
                "Fix failure. Timelines must be spaced 30 minutes apart"
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

                    btnCompleteDelete.classList.remove("d-none");
                    $("#loading_delete_food").hide();
                    $("#modalDeleteFood").modal("hide");
                    toastSuccessFood("Delete successfully");
                } else {
                    $("#modalDeleteFood").modal("hide");
                    toastFailFood("Delete failed");
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
        tableBodyFood.innerHTML = `<td colspan="5">You are in AI Auto Feeding</td>`;
        chartElement.classList.add("d-none");

        return;
    }

    if (!userNameLogin) {
        tableBodyFood.innerHTML = `<td colspan="5">An error occurred. Please Logout and login again</td>`;
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
                tableBodyFood.innerHTML = `<td colspan="5">No settings yet</td>`;
                // chartElement.classList.add('d-none');
            }
        },
    });
};

if (modeAI == 1) {
    tableBodyFood.innerHTML = `<td colspan="5">You are in AI Auto Feeding</td>`;
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
        toastFailFood("Please set the fish feeding time");
        return;
    }

    if (userTimeSet <= 0) {
        toastFailFood("Please setting food greater 0");
        return;
    }

    if (!userAmountFoodSet) {
        toastFailFood("Please set the amount of fish food");
        return;
    }

    if (settingFoods.length > 10) {
        toastFailFood("Only 10 settings max");
        return;
    }

    if (modeAI == 1) {
        toastFailFood("You are in AI feeding mode that cannot be set");
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
                        toastSuccessFood("Successful feeding time setting");
                    } else if (data == "LIMIT") {
                        toastFailFood("Max setting is 10");
                    } else if (data == "EXIST_TIME") {
                        toastFailFood("Setup time already exists");
                    } else {
                        toastFailFood("Feeding time setting failed");
                    }
                },
            });
        } else {
            return toastFailFood(
                "The timestamps must be spaced 30 minutes apart."
            );
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
                    toastSuccessFood("Successful feeding time setting");
                } else if (data == "LIMIT") {
                    toastFailFood("Max setting is 10");
                } else if (data == "EXIST_TIME") {
                    toastFailFood("Setup time already exists");
                } else {
                    toastFailFood("Feeding time setting failed");
                }
            },
        });
    }
};
