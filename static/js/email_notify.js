const modalNotify = document.getElementById("modalNoti");

const usernameLoginEmailRegister =
    document.querySelector("#username_login").innerHTML;
const btnConfirmRegisterEmail = modalNotify.querySelector("#btn_confirm_email");
const loadingEmailRegister = modalNotify.querySelector(
    "#loading_email_register"
);

const titleEmail = document.getElementById("title_email");
const subTitleEmail = document.getElementById("subtile_email");
const dotNewNotify2 = document.querySelector(".dot_new_noti");

const newNotifyTick = localStorage.getItem("new_noti");
const contentNotify2 = document.querySelector(".content_notify");

if (newNotifyTick == 1) {
    dotNewNotify2.classList.add("noti_new");
}

const ToastNotify = (txt) => {
    try {
        toastFail(txt);
    } catch (err) {
        toastFailFood(txt);
    }
};

const hideRegister = (emailNotify) => {
    $("#email_already").show();

    $("#email_register").hide();
    $("#subtile_email").hide();
    modalNotify.querySelector("#email_notify_already").value = emailNotify;
    titleEmail.innerHTML = "Email notifying you that you have registered";
};

const showRegister = () => {
    $("#email_already").hide();

    $("#email_register").show();
    $("#subtile_email").show();
    modalNotify.querySelector("#email_notify_already").value = null;
    titleEmail.innerHTML =
        "Please enter the correct email to receive notifications";
};

const renderNotifyMain = () => {
    $.ajax({
        type: "GET",
        url: `/notify/get/${usernameLoginEmailRegister}`,
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
                contentNotify2.innerHTML = contentNotifyLoop.join("");
            } else {
                contentNotify2.innerHTML = "Not notification";
            }
        },
    });
};

modalNotify.addEventListener("show.bs.modal", (event) => {
    let emailNotify = localStorage.getItem("email_notify");

    dotNewNotify2.classList.remove("noti_new");
    localStorage.removeItem("new_noti");

    const btnClearNotify = modalNotify.querySelector("#btn_clear_notify");

    renderNotifyMain();

    if (emailNotify) {
        const btnEditEmail = modalNotify.querySelector("#btn_edit_email");
        const btnDeleteEmail = modalNotify.querySelector("#btn_delete_email");
        // $("#email_register").hide();
        // $("#email_already").show();
        // $("#subtile_email").hide();
        // modalNotify.querySelector("#email_notify_already").value = emailNotify;
        // titleEmail.innerHTML = "Email gửi thông báo bạn đã đăng kí";

        hideRegister(emailNotify);

        // handle edit email
        btnEditEmail.onclick = (e) => {
            const newEmail = modalNotify.querySelector(
                "#email_notify_already"
            ).value;
            if (emailNotify == newEmail) {
                ToastNotify("Please change new email");
            }

            var bodyFormData = new FormData();
            bodyFormData.append("username", usernameLoginEmailRegister);
            bodyFormData.append("email", newEmail);

            $.ajax({
                type: "POST",
                url: `/email_notify/update/${usernameLoginEmailRegister}`,
                data: bodyFormData,
                contentType: false,
                cache: false,
                processData: false,
                success: function (data) {
                    console.log({ update: data });
                    if (data == "EXIST_EMAIL") {
                        ToastNotify("Email exist");
                        loadingEmailRegister.classList.add("hide_element");
                        btnConfirmRegisterEmail.style.disable = false;
                        return;
                    } else if (data == "OK") {
                        localStorage.setItem("email_notify", newEmail);
                        loadingEmailRegister.classList.add("hide_element");
                        btnConfirmRegisterEmail.style.disable = false;
                        $("#modalNoti").modal("hide");
                    }
                },
            });
        };

        // handle delete email
        btnDeleteEmail.onclick = () => {
            $.ajax({
                type: "GET",
                url: `/email_notify/delete/${usernameLoginEmailRegister}`,
                dataType: "json",
                success: function (data) {
                    console.log({ delete: data });
                    $("#modalNoti").modal("hide");
                    localStorage.removeItem("email_notify");
                    showRegister();
                },
            });
        };
    } else {
        $.ajax({
            type: "GET",
            url: `/email_notify/get/${usernameLoginEmailRegister}`,
            dataType: "json",
            success: function ({ data }) {
                const emailNotify = JSON.parse(data);
                if (emailNotify && emailNotify.length > 0) {
                    hideRegister(emailNotify[0].email);
                    localStorage.setItem("email_notify", emailNotify[0].email);
                } else {
                    showRegister();
                }
            },
        });
    }

    btnClearNotify.onclick = () => {
        $.ajax({
            type: "GET",
            url: `/notify/delete/${usernameLoginEmailRegister}`,
            dataType: "json",
            success: function (data) {
                $("#modalNoti").modal("hide");
                renderNotifyMain();
            },
        });
        $("#modalNoti").modal("hide");
    };
});

btnConfirmRegisterEmail.onclick = (e) => {
    const email = modalNotify.querySelector("#email_notify").value;

    if (!usernameLoginEmailRegister || !email) {
        ToastNotify(
            "Please fill in the required information before saving your application."
        );
        return;
    }
    loadingEmailRegister.classList.remove("hide_element");
    btnConfirmRegisterEmail.style.disable = true;

    // var bodyFormData = new FormData();

    var bodyFormData = new FormData();
    bodyFormData.append("username", usernameLoginEmailRegister);
    bodyFormData.append("email", email);

    $.ajax({
        type: "POST",
        url: "/email_notify/add",
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == "EXIST_EMAIL") {
                ToastNotify("Email đã tồn tại");
                loadingEmailRegister.classList.add("hide_element");
                btnConfirmRegisterEmail.style.disable = false;
                return;
            } else if (data == "OK") {
                localStorage.setItem("email_notify", email);
                loadingEmailRegister.classList.add("hide_element");
                btnConfirmRegisterEmail.style.disable = false;
                $("#modalNoti").modal("hide");
            }
        },
    });
};

//

// check load

$.ajax({
    type: "GET",
    url: `/check_load_start`,
    success: function (data) {
        if (data == "OK") {
            $("#opacity_loading_page").hide();
        } else {
            setTimeout(() => {
                $.ajax({
                    type: "GET",
                    url: `/check_load_start`,
                    success: function (data) {
                        if (data == "OK") {
                            $("#opacity_loading_page").hide();
                        }
                    },
                });
            }, 1000);
        }
    },
    error: function (jqXHR, textStatus, errorThrown) {
        setTimeout(() => {
            $.ajax({
                type: "GET",
                url: `/check_load_start`,
                success: function (data) {
                    if (data == "OK") {
                        $("#opacity_loading_page").hide();
                    }
                },
            });
        }, 1000);
    },
});
