const toastUploadSuccess = document.querySelector('#toastUploadLabel');
const toastUploadFail = document.querySelector('#toastUploadLabelFail');

const timeUpload = document.querySelector('.time_upload');
const toastContentSuccess = document.querySelector('#toast_success_body');

const timeUploadFail = document.querySelector('.time_upload_fail');
const toastContentFail = document.querySelector('#toast_fail_body');

const toastFail = (message) => {
    const { datePresent, timePresent } = getTimePresent();
    timeUploadFail.innerHTML = timePresent + ' - ' + datePresent;
    toastContentFail.innerHTML = message;
    const toast = new bootstrap.Toast(toastUploadFail);
    toast.show();
};

const toastSuccess = (message) => {
    const { datePresent, timePresent } = getTimePresent();
    timeUpload.innerHTML = timePresent + ' - ' + datePresent;
    toastContentSuccess.innerHTML = message;
    const toast = new bootstrap.Toast(toastUploadSuccess);
    toast.show();
};
