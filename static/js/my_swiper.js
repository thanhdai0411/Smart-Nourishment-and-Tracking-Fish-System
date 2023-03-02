// var swiper = new Swiper('.mySwiper', {
//     slidesPerView: 1,
//     spaceBetween: 30,
//     pagination: {
//         el: '.swiper-pagination',
//         clickable: true,
//     },
//     navigation: {
//         nextEl: '.swiper-button-next',
//         prevEl: '.swiper-button-prev',
//     },
// });

// var swiper = new Swiper('.mySwiper', {
//     slidesPerView: 1,
//     spaceBetween: 30,
//     centeredSlides: true,
//     loop: true,
//     grabCursor: true,

//     keyboard: {
//         enabled: true,
//     },
//     autoplay: {
//         delay: 3000,
//         disableOnInteraction: false,
//     },
//     breakpoints: {
//         769: {
//             slidesPerView: 1,
//             slidesPerGroup: 1,
//         },
//     },

//     navigation: {
//         nextEl: '.swiper-button-next',
//         prevEl: '.swiper-button-prev',
//     },
//     pagination: {
//         el: '.swiper-pagination',
//         clickable: true,
//     },
// });

// var swiper = new Swiper(".mySwiper", {
//     slidesPerView: 3,
//     centeredSlides: true,
//     spaceBetween: 30,
//     pagination: {
//         el: ".swiper-pagination",
//         type: "fraction",
//     },
//     navigation: {
//         nextEl: ".swiper-button-next",
//         prevEl: ".swiper-button-prev",
//     },
// });

// var appendNumber = 4;
// var prependNumber = 1;
// document
//     .querySelector(".prepend-2-slides")
//     .addEventListener("click", function (e) {
//         e.preventDefault();
//         swiper.prependSlide([
//             '<div class="swiper-slide">Slide ' + --prependNumber + "</div>",
//             '<div class="swiper-slide">Slide ' + --prependNumber + "</div>",
//         ]);
//     });
// document
//     .querySelector(".prepend-slide")
//     .addEventListener("click", function (e) {
//         e.preventDefault();
//         swiper.prependSlide(
//             '<div class="swiper-slide">Slide ' + --prependNumber + "</div>"
//         );
//     });
// document.querySelector(".append-slide").addEventListener("click", function (e) {
//     e.preventDefault();
//     swiper.appendSlide(
//         '<div class="swiper-slide">Slide ' + ++appendNumber + "</div>"
//     );
// });
// document
//     .querySelector(".append-2-slides")
//     .addEventListener("click", function (e) {
//         e.preventDefault();
//         swiper.appendSlide([
//             '<div class="swiper-slide">Slide ' + ++appendNumber + "</div>",
//             '<div class="swiper-slide">Slide ' + ++appendNumber + "</div>",
//         ]);
//     });

$(".owl-carousel").owlCarousel({
    loop: true,
    margin: 20,
    nav: false,
    autoplay: true,
    autoplayTimeout: 3000,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 2,
        },
        1000: {
            items: 3,
        },
        1200: {
            items: 4,
        },
    },
});
