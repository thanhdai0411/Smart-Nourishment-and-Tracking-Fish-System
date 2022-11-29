//! get coordinates
let result = document.querySelector('.result'),
    img_result = document.querySelector('.img-result'),
    img_w = document.querySelector('.img-w'),
    img_h = document.querySelector('.img-h'),
    options = document.querySelector('.options'),
    cropped = document.querySelector('.cropped'),
    dwn = document.querySelector('.download'),
    upload = document.querySelector('#file-input'),
    cropper = '';

let coorDinates = document.querySelector('.coordinates');
let x, y, w, h;

// const getData = async () => {
//     let data = await axios.get('https://jsonplaceholder.typicode.com/todos/1');
// };

//========================zz===================================================
let imgUploadName = '';
$('.box-2').hide();

upload.addEventListener('change', (e) => {
    $('.box-2').show();
    if (e.target.files.length) {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (e.target.result) {
                let img = document.createElement('img');
                img.id = 'image';
                img.src = e.target.result;
                result.innerHTML = '';
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

//! save label into storage
const btnSaveLabel = document.querySelector('#btn_save_label');
const btnSubmitLabel = document.querySelector('.save');
const inputLabel = document.querySelector('#input_label');
const labelPresent = document.querySelector('#label_present');
labelPresent.innerHTML = localStorage.getItem('label');
btnSaveLabel.onclick = (e) => {
    const valueInputLabel = inputLabel.value;

    localStorage.setItem('label', valueInputLabel);
    labelPresent.innerHTML = localStorage.getItem('label');

    console.log(valueInputLabel);
};

//! end save label into storage

//! post label
const userNameLogin = document.querySelector('#username_login').innerHTML;

const toastUploadSuccess = document.querySelector('#toastUploadLabel');
const toastUploadFail = document.querySelector('#toastUploadLabelFail');

const timeUpload = document.querySelector('.time_upload');
const timeUploadFail = document.querySelector('.time_upload_fail');

const toastContentFail = document.querySelector('#toast_fail_body');

const getTimePresent = () => {
    let today = new Date();
    let timePresent = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();
    var datePresent = today.getDate() + '/' + (today.getMonth() + 1);
    return { timePresent, datePresent };
};

btnSubmitLabel.addEventListener('click', (e) => {
    const labelStorage = localStorage.getItem('label');

    let check = $('#file-input').val();
    if (check == '') {
        const { datePresent, timePresent } = getTimePresent();

        timeUploadFail.innerHTML = timePresent + ' - ' + datePresent;
        toastContentFail.innerHTML = 'Vui lòng chọn ảnh và khoanh vùng cá trước khi lưu dữ liệu';
        const toast = new bootstrap.Toast(toastUploadFail);
        toast.show();
        return;
    }
    const coordinatesBox = `${x.toFixed(6)} ${y.toFixed(6)} ${w.toFixed(6)} ${h.toFixed(6)}`;

    imgUploadName = imgUploadName.split('.')[0];
    // coorDinates.innerHTML = 0 + ' ' + coordinatesBox;

    var bodyFormData = new FormData($('#upload_file')[0]);

    bodyFormData.append('coordinates', 0 + ' ' + coordinatesBox);
    bodyFormData.append('label', labelStorage);
    bodyFormData.append('image_name', imgUploadName);
    bodyFormData.append('username', userNameLogin);

    // var form_data = new FormData();
    // bodyFormData.append('file', $('#upload_file').prop('files')[0]);

    // if()
    $.ajax({
        type: 'POST',
        url: '/upload/labels',
        data: bodyFormData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            console.log({ data });
            if (data == 'FAIL') {
                const { datePresent, timePresent } = getTimePresent();
                timeUploadFail.innerHTML = timePresent + ' - ' + datePresent;
                toastContentFail.innerHTML = 'Ảnh đã tồn tại';
                const toast = new bootstrap.Toast(toastUploadFail);
                toast.show();
            } else {
                $('#file-input').val('');
                $('.box-2').hide();

                // console.log(a);
                const { datePresent, timePresent } = getTimePresent();

                timeUpload.innerHTML = timePresent + ' - ' + datePresent;
                const toast = new bootstrap.Toast(toastUploadSuccess);
                toast.show();
            }
        },
    });

    // const postDataToServer = async () => {
    //     const res = await axios.post('http://127.0.0.1:5000/upload/labels', bodyFormData);
    //     console.log('Upload label to server');
    //     console.log(res);
    // if (res.data.success == 1) {
    //     bodyFormData.append('coordinates', null);
    //     bodyFormData.append('label', null);
    // } else {
    //     alert('error');
    // }
    // };
    // postDataToServer();
});
//! end post label
