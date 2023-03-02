const userNameSystem = document.querySelector("#username_login").innerHTML;
const btnSubmitProfileFish = document.getElementById("btn_submit_profile");
const wrapProfileCarousel = document.getElementById("wrap_my_carousel");

const loadingProfile = document.querySelector(".loading_profile");
const loadingUpdateInfoDetail = document.querySelector(
    "#loading_update_info_detail"
);

const btnInfoProfile = document.querySelectorAll(".info_profile");
const modalProfileDetail = document.getElementById("modalProfileFish");

const btnAllProfileFish = document.querySelector(".btn_all_profile");

btnInfoProfile.forEach((btn) => {
    btn.onclick = () => {
        let idInfo = btn.getAttribute("data-id_info");
        console.log(idInfo);
        $("#modalProfileFish").modal("show");

        $.ajax({
            type: "GET",
            url: `/profile_fish/get_detail/${idInfo}`,
            dataType: "json",
            success: function ({ data }) {
                let [profileFishData] = JSON.parse(data);

                modalProfileDetail.querySelector("#avatar_info").src =
                    profileFishData.avatar;
                modalProfileDetail.querySelector(".username_info").value =
                    profileFishData.username;
                modalProfileDetail.querySelector(".fish_type_info").value =
                    profileFishData.fish_type;
                modalProfileDetail.querySelector(".fish_name_info").innerHTML =
                    profileFishData.fish_name;
                modalProfileDetail.querySelector(".start_date_info").value =
                    profileFishData.time_start_farming;
                modalProfileDetail.querySelector(".note_info").value =
                    profileFishData.note ||
                    "Không có ghi chú nào cho cư dân này";

                const btnEditProfile =
                    modalProfileDetail.querySelector(".edit_info");
                const btnDeleteProfile =
                    modalProfileDetail.querySelector(".delete_info");

                // update profile
                btnEditProfile.onclick = (e) => {
                    const askConfirm = confirm(
                        "Chắc chắn muốn cập nhật thông tin co cư dân"
                    );

                    if (askConfirm == true) {
                        btnEditProfile.disable = true;
                        btnEditProfile.innerHTML = "Waiting...";
                        const username =
                            modalProfileDetail.querySelector(
                                ".username_info"
                            ).value;
                        const fish_type =
                            modalProfileDetail.querySelector(
                                ".fish_type_info"
                            ).value;

                        const start_date =
                            modalProfileDetail.querySelector(
                                ".start_date_info"
                            ).value;
                        const note =
                            modalProfileDetail.querySelector(
                                ".note_info"
                            ).value;

                        var bodyFormData = new FormData(
                            $("#update_profile")[0]
                        );

                        bodyFormData.append("username", username);
                        bodyFormData.append("fish_type", fish_type);
                        bodyFormData.append("time_start_farming", start_date);
                        bodyFormData.append("note", note);
                        bodyFormData.append("avatar", profileFishData.avatar);
                        // bodyFormData.append("fish_name", fishName);

                        $.ajax({
                            type: "POST",
                            url: `/profile_fish/update/${idInfo}`,
                            data: bodyFormData,
                            contentType: false,
                            cache: false,
                            processData: false,
                            success: function (data) {
                                // console.log({ data });
                                location.reload();
                            },
                        });
                    } else {
                        return;
                    }
                };
                // delete info
                btnDeleteProfile.onclick = (e) => {
                    const askConfirm = confirm(
                        "Chắc chắn muốn xóa cư dân này ra khỏi thành phố"
                    );
                    if (askConfirm == true) {
                        btnDeleteProfile.disable = true;
                        btnDeleteProfile.innerHTML = "Waiting...";
                        var bodyFormData = new FormData();
                        bodyFormData.append("avatar", profileFishData.avatar);
                        $.ajax({
                            type: "POST",
                            url: `/profile_fish/delete/${idInfo}`,
                            data: bodyFormData,
                            contentType: false,
                            cache: false,
                            processData: false,
                            success: function (data) {
                                // console.log({ data });
                                location.reload();
                            },
                        });
                    } else {
                        return;
                    }
                };
            },
        });
    };
});

btnSubmitProfileFish.onclick = (e) => {
    const userSubmitProfile = document.getElementById("input_username").value;
    const fishType = document.getElementById("input_fish_type").value;
    const timeStartFarm = document.getElementById("input_time_start").value;
    const fishName = document.getElementById("input_fish_name").value;
    const noteFish = document.getElementById("input_not_fish").value;

    if (!userSubmitProfile || !fishType || !fishName || !timeStartFarm) {
        toastFail("Vui lòng điền dây đủ thông tin trước khi lưu hồ sơ");
        return;
    }
    loadingProfile.classList.remove("hide_element");
    btnSubmitProfileFish.style.display = "none";
    let note = noteFish;

    if (!noteFish) {
        note = "Không có ghi chú gì về cư dân này trong thành phố";
    }
    // var bodyFormData = new FormData();

    var bodyFormData = new FormData($("#upload_profile")[0]);
    bodyFormData.append("username", userSubmitProfile);
    bodyFormData.append("fish_type", fishType);
    bodyFormData.append("time_start_farming", timeStartFarm);
    bodyFormData.append("fish_name", fishName);
    bodyFormData.append("user_system", userNameSystem);
    bodyFormData.append("note", note);

    $.ajax({
        type: "POST",
        url: "/profile_fish/add",
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == "EXIST_FISH_NAME") {
                toastFail("Tên đã tồn tại");
                return;
            } else if (data == "OK") {
                location.reload();
                loadingProfile.classList.add("hide_element");
                btnSubmitProfileFish.style.display = "block";
            }
        },
    });
};

const getProfileFish = () => {
    if (!userNameSystem) {
        toastFail("Có lỗi !. Vui lòng đăng nhập lại");
        return;
    }

    $.ajax({
        type: "GET",
        url: `/profile_fish/get/${userNameSystem}`,
        dataType: "json",
        success: function (data) {
            const { data: profileFish, success } = data;
            localStorage.setItem("profile_fish", profileFish);
            let profileFishData = JSON.parse(profileFish);
            // location.reload();
            console.log({ profileFishData });
            if (success === 1 && profileFishData.length > 0) {
                const profileFishRender = profileFishData.map((v, index) => {
                    let id = v._id.$oid;

                    let style =
                        v.status === "WAITING"
                            ? "#e8733b"
                            : v.status === "COMPLETE"
                            ? "#54B435"
                            : "#8B7E74";
                    return `
                    
                        <div class="item">
                            <div class="avatar">
                                <img src=${v.avatar} alt="" cl>
                            </div>
                            <div class="content_profile">
                                <h4>${v.fish_name}</h4>
                                <p class="fish_name_origin">${v.fish_type}</p>
                                <p class="note_profile">${
                                    v.note
                                        ? v.note
                                        : "Không có ghi chú cho cư dân này"
                                }</p>
                                <button>XEM THÊM THÔNG TIN</button>
                        </div>

                    </div>
                    `;
                });
                wrapProfileCarousel.innerHTML = profileFishRender.join("");
            } else {
                toastFail("Tên đã tồn tại");
                return;
            }
        },
    });
};

$("#datePicker").on("change", function (e) {
    displayDateFormat($(this), "#datePickerLbl", $(this).val());
});

function displayDateFormat(thisElement, datePickerLblId, dateValue) {
    $(thisElement)
        .css("color", "rgba(0,0,0,0)")
        .siblings(`${datePickerLblId}`)
        .css({
            position: "absolute",
            left: "10px",
            top: "8px",
        })
        .text(
            dateValue.length == 0 ? "" : `${getDateFormat(new Date(dateValue))}`
        );
}

function getDateFormat(dateValue) {
    let d = new Date(dateValue);

    // this pattern dd/mm/yyyy
    // you can set pattern you need
    let dstring = `${("0" + d.getDate()).slice(-2)}/${(
        "0" +
        (d.getMonth() + 1)
    ).slice(-2)}/${d.getFullYear()}`;

    return dstring;
}
