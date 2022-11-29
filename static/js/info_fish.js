const modalInfoFish = document.getElementById('modal_element');
const imageFish = document.querySelector('#img_info_fish');
modalInfoFish.addEventListener('show.bs.modal', (event) => {
    const button = event.relatedTarget;

    const recipient = button.getAttribute('data-bs-whatever');

    let result = JSON.parse(recipient);

    const modalTitle = modalInfoFish.querySelector('.modal-title');
    const modalBodyInput = modalInfoFish.querySelector('.modal-body input');

    modalTitle.textContent = `Thông tin ${result.name}`;
    imageFish.src = result.img;
});
