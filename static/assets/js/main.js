(function ($) {
  "use strict";

  // ==========================================
  //      Start Document Ready function
  // ==========================================
  $(document).ready(function () {
    // ============== Mobile Nav Menu Dropdown Js Start =======================
    function toggleSubMenu() {
      if ($(window).width() <= 991) {
        $(".has-submenu")
          .off("click")
          .on("click", function () {
            $(this)
              .toggleClass("active")
              .siblings(".has-submenu")
              .removeClass("active")
              .find(".nav-submenu")
              .slideUp(300);
            $(this).find(".nav-submenu").stop(true, true).slideToggle(300);
          });
      } else {
        $(".has-submenu").off("click");
      }
    }

    toggleSubMenu();
    $(window).resize(toggleSubMenu);
    // ============== Mobile Nav Menu Dropdown Js End =======================

    // ===================== Scroll Back to Top Js Start ======================
    var progressPath = document.querySelector(".progress-wrap path");
    var pathLength = progressPath.getTotalLength();
    progressPath.style.transition = progressPath.style.WebkitTransition =
      "none";
    progressPath.style.strokeDasharray = pathLength + " " + pathLength;
    progressPath.style.strokeDashoffset = pathLength;
    progressPath.getBoundingClientRect();
    progressPath.style.transition = progressPath.style.WebkitTransition =
      "stroke-dashoffset 10ms linear";
    var updateProgress = function () {
      var scroll = $(window).scrollTop();
      var height = $(document).height() - $(window).height();
      var progress = pathLength - (scroll * pathLength) / height;
      progressPath.style.strokeDashoffset = progress;
    };
    updateProgress();
    $(window).scroll(updateProgress);
    var offset = 50;
    var duration = 550;
    jQuery(window).on("scroll", function () {
      if (jQuery(this).scrollTop() > offset) {
        jQuery(".progress-wrap").addClass("active-progress");
      } else {
        jQuery(".progress-wrap").removeClass("active-progress");
      }
    });
    jQuery(".progress-wrap").on("click", function (event) {
      event.preventDefault();
      jQuery("html, body").animate({ scrollTop: 0 }, duration);
      return false;
    });
    // ===================== Scroll Back to Top Js End ======================

    // ========================== add active class to navbar menu current page Js Start =====================
    function dynamicActiveMenuClass(selector) {
      let FileName = window.location.pathname.split("/").reverse()[0];

      // If we are at the root path ("/" or no file name), keep the activePage class on the Home item
      if (FileName === "" || FileName === "index.html" || FileName === "index-2.html" || FileName === "index-3.html" || FileName === "index-4.html" || FileName === "index-5.html" || FileName === "index-6.html" ) {
        // Keep the activePage class on the Home link
        selector
          .find("li.nav-menu__item.has-submenu")
          .eq(0)
          .addClass("activePage");
      } else {
        // Remove activePage class from all items first
        selector.find("li").removeClass("activePage");

        // Add activePage class to the correct li based on the current URL
        selector.find("li").each(function () {
          let anchor = $(this).find("a");
          if ($(anchor).attr("href") == FileName) {
            $(this).addClass("activePage");
          }
        });

        // If any li has activePage element, add class to its parent li
        selector.children("li").each(function () {
          if ($(this).find(".activePage").length) {
            $(this).addClass("activePage");
          }
        });
      }
    }

    if ($("ul").length) {
      dynamicActiveMenuClass($("ul"));
    }
    // ========================== add active class to navbar menu current page Js End =====================

    // ========================== Settings Panel Js Start =====================
    $(".settings-button").on("click", function () {
      $(".settings-panel").toggleClass("active");
      $(this).toggleClass("active");
    });

    $(document).on(
      "click",
      ".settings-panel__buttons .settings-panel__button",
      function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
      }
    );

    // Cursor start
    $(".cursor-animate").on("click", function () {
      $("body").removeClass("remove-animate-cursor");
    });

    $(".cursor-default").on("click", function () {
      $("body").addClass("remove-animate-cursor");
    });
    // Cursor end

    // Direction start
    $(".direction-ltr").on("click", function () {
      $("html").attr("dir", "ltr");
    });

    $(".direction-rtl").on("click", function () {
      $("html").attr("dir", "rtl");
    });
    // Direction end
    // ========================== Settings Panel Js End =====================

    // ********************* Toast Notification Js start *********************
    function toastMessage(messageType, messageTitle, messageText, messageIcon) {
      let $toastContainer = $("#toast-container");

      let $toast = $("<div>", {
        class: `toast-message ${messageType}`,
        html: `
      <div class="toast-message__content">
        <span class="toast-message__icon">
          <i class="${messageIcon}"></i>
        </span>
        <div class="flex-grow-1">
          <div class="d-flex align-items-start justify-content-between mb-1">
            <h6 class="toast-message__title">${messageTitle}</h6>
            <button type="button" class="toast-message__close">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>
          <span class="toast-message__text">${messageText}</span>
        </div>
      </div>
      <div class="progress__bar"></div>
    `,
      });

      $toastContainer.append($toast);

      setTimeout(() => {
        $toast.addClass("active");
      }, 50);

      let totalDuration = 3500;
      let startTime = Date.now();
      let remainingTime = totalDuration;
      let toastTimeout = setTimeout(hideToast, remainingTime);

      function hideToast() {
        $toast.removeClass("active");
        setTimeout(() => {
          $toast.remove();
        }, 500);
      }

      // Remove Toast on Close Button Click
      $toast.find(".toast-message__close").on("click", function () {
        $toast.removeClass("active");
        setTimeout(() => {
          $toast.remove();
        }, 500);
      });

      // Pause Timeout on Hover
      $toast.on("mouseenter", function () {
        remainingTime -= Date.now() - startTime;
        clearTimeout(toastTimeout);
      });

      // Resume Timeout on Mouse Leave
      $toast.on("mouseleave", function () {
        startTime = Date.now();
        toastTimeout = setTimeout(hideToast, remainingTime);
      });
    }
    // ********************* Toast Notification Js End *********************

    // ========================= Form Submit Js Start ===================
    $(document).on("submit", ".form-submit", function (e) {
      let action = ($(this).attr("action") || "").trim();

      if (action && action !== "#") {
        return;
      }

      e.preventDefault();

      $(this).find("input").val("");

      $(this).find("textarea").val("");

      toastMessage(
        "success",
        "Success",
        "Form submitted successfully!",
        "fa-solid fa-circle-check"
      );
    });
    // ========================= Form Submit Js End ===================

    // ========================= Search Popup Js Start ===================
    $(".search-popup__button").on("click", function () {
      $(".search-popup").addClass("active");
      $(".overlay").addClass("show-overlay");
    });
    $(".search-popup__close, .overlay").on("click", function () {
      $(".search-popup").removeClass("active");
      $(".overlay").removeClass("show-overlay");
    });
    // ========================= Search Popup Js End ===================

    // ========================== Add Attribute For Bg Image Js Start ====================
    $(".background-img").css("background", function () {
      var bg = "url(" + $(this).data("background-image") + ")";
      return bg;
    });
    // ========================== Add Attribute For Bg Image Js End =====================

    // ================================= Banner slider Start =========================
    var bannerOne = new Swiper(".banner-slider", {
      slidesPerView: 1,
      grabCursor: true,
      loop: true,
      speed: 1000,
      effect: "fade",
      autoplay: {
        delay: 6000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".banner-slider-pagination",
        clickable: true,
      },
    });
    // ================================= Banner slider End =========================

    // ================================= Brand slider Start =========================
    var brandOneSlider = new Swiper(".brand-one-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 5,
      breakpoints: {
        300: {
          slidesPerView: 3,
        },
        575: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        992: {
          slidesPerView: 5,
        },
        1200: {
          slidesPerView: 5,
        },
      },
    });
    // ================================= Brand slider End =========================

    // ================================= Testimonials One slider Start =========================
    var testimonialsSlider = new Swiper(".testimonials-slider", {
      autoplay: {
        delay: 6000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 1,
      pagination: {
        el: ".testimonials-slider-pagination",
        clickable: true,
      },
    });
    // ================================= Testimonials One slider End =========================

    // ================================= Blog One slider Start =========================
    var blogSlider = new Swiper(".blog-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 1,
      spaceBetween: 24,
      pagination: {
        el: ".blog-slider-pagination",
        clickable: true,
      },
      breakpoints: {
        300: {
          slidesPerView: 1,
        },
        992: {
          slidesPerView: 2,
        },
      },
    });
    // ================================= Blog One slider End =========================

    // ================================= Project Two slider Start =========================
    var projectTwoSlider = new Swiper(".project-two-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 1,
      spaceBetween: 24,
      pagination: {
        el: ".project-two-slider-pagination",
        clickable: true,
      },
      breakpoints: {
        300: {
          slidesPerView: 1,
        },
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
        1200: {
          slidesPerView: 4,
        },
        1350: {
          slidesPerView: 5,
        },
      },
    });
    // ================================= Project Two slider End =========================

    // ================================= service three slider Start =========================
    var serviceThreeSlider = new Swiper(".service-three-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 1,
      spaceBetween: 24,
      pagination: {
        el: ".service-three-slider-pagination",
        clickable: true,
      },
      breakpoints: {
        300: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });
    // ================================= service three slider End =========================

    // ================================= Testimonials three slider Start =========================
    var testimonialsThreeSlider = new Swiper(".testimonials-three-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 1,
      spaceBetween: 24,
      pagination: {
        el: ".testimonials-three-slider-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".testimonials-three-button-next",
        prevEl: ".testimonials-three-button-prev",
      },
      breakpoints: {
        300: {
          slidesPerView: 1,
        },
        992: {
          slidesPerView: 2,
        },
      },
    });
    // ================================= Testimonials three slider End =========================

    // ================================= Category slider Start =========================
    var categorySlider = new Swiper(".category-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 5,
      breakpoints: {
        300: {
          slidesPerView: 2,
        },
        425: {
          slidesPerView: 3,
        },
        575: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        992: {
          slidesPerView: 5,
        },
        1200: {
          slidesPerView: 6,
        },
        1300: {
          slidesPerView: 7,
        },
      },
      navigation: {
        nextEl: ".category-slider-button-next",
        prevEl: ".category-slider-button-prev",
      },
    });
    // ================================= Category slider End =========================

    // ================================= Brand slider Start =========================
    var brandSlider = new Swiper(".brand-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1500,
      grabCursor: true,
      loop: true,
      slidesPerView: 6,
      breakpoints: {
        300: {
          slidesPerView: 2,
        },
        575: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        992: {
          slidesPerView: 5,
        },
        1200: {
          slidesPerView: 6,
        },
      },
    });
    // ================================= Brand slider End =========================

    // ================================= Product Details slider Start =========================
    var mySwiper = new Swiper(".mySwiper", {
      spaceBetween: 10,
      slidesPerView: 3,
      freeMode: true,
      watchSlidesProgress: true,
      direction: "horizontal",
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      breakpoints: {
        450: {
          slidesPerView: 4,
        },
        576: {
          direction: "vertical",
          slidesPerView: 5,
        },
      },
    });
    var mySwiper2 = new Swiper(".mySwiper2", {
      effect: "fade",
      spaceBetween: 10,
      direction: "horizontal",
      thumbs: {
        swiper: mySwiper,
      },
      breakpoints: {
        576: {
          direction: "vertical",
        },
      },
    });
    // ================================= Product Details slider End =========================

    
    // ================================= service Two slider Start =========================
    var serviceThreeSlider = new Swiper(".service-two-slider", {
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      speed: 1000,
      grabCursor: true,
      loop: true,
      slidesPerView: 1,
      spaceBetween: 24,
      pagination: {
        el: ".service-two-slider-pagination",
        clickable: true,
      },
       navigation: {
        nextEl: ".service-two-slider-button-next",
        prevEl: ".service-two-slider-button-prev",
      },
      breakpoints: {
        300: {
          slidesPerView: 1,
        },
        768: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });
    // ================================= service Two slider End =========================


    // ========================= AOS Js Start ===========================
    AOS.init({
      once: true,
    });
    // ========================= AOS Js End ===========================

    // ========================= magnific Popup Js Start =====================
    $(".play-button").magnificPopup({
      type: "iframe",
      removalDelay: 300,
      mainClass: "mfp-fade",
    });
    // ========================= magnific Popup Js End =====================

    // ============== Magnific Popup Js Start =======================
    $(".gallery-popup").magnificPopup({
      type: "image",
      gallery: {
        enabled: true,
      },
    });
    // ============== Magnific Popup Js End =======================

    // ============== Wishlist button Js Start =======================
    $(document).on("click", ".wishlist-btn", function () {
      $(this).toggleClass("active");
    });
    // ============== Wishlist button Js End =======================

    // ========================= Counter Up Js Start ===================
    const counterUp = window.counterUp.default;

    const callback = (entries) => {
      entries.forEach((entry) => {
        const el = entry.target;
        if (entry.isIntersecting && !el.classList.contains("is-visible")) {
          counterUp(el, {
            duration: 2500,
            delay: 16,
          });
          el.classList.add("is-visible");
        }
      });
    };
    const IO = new IntersectionObserver(callback, { threshold: 1 });

    // Banner statistics Counter
    const statisticsCounter = document.querySelectorAll(".counter");
    if (statisticsCounter.length > 0) {
      statisticsCounter.forEach((counterNumber) => {
        IO.observe(counterNumber);
      });
    }

    // performance Count
    const performanceCount = document.querySelectorAll(".counter");
    if (performanceCount.length > 0) {
      performanceCount.forEach((counterNumber) => {
        IO.observe(counterNumber);
      });
    }
    // ========================= Counter Up Js End ===================

    // ================================ Floating Progress js start =================================
    const progressContainers = document.querySelectorAll(".progress-container");

    function setPercentage(progressContainer) {
      const percentage =
        progressContainer.getAttribute("data-percentage") + "%";

      const progressEl = progressContainer.querySelector(".progress");
      const percentageEl = progressContainer.querySelector(".percentage");

      progressEl.style.width = percentage;
      percentageEl.innerText = percentage;
      percentageEl.style.insetInlineStart = percentage;
    }

    // Intersection Observer to trigger progress animation when section is in view
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Element is in view, start the progress animation
            const progressContainer = entry.target;
            setPercentage(progressContainer);
            progressContainer
              .querySelector(".progress")
              .classList.remove("active");
            progressContainer
              .querySelector(".percentage")
              .classList.remove("active");
            observer.unobserve(progressContainer); 
          }
        });
      },
      {
        threshold: 0.5, 
      }
    );

    // Start observing all progress containers
    progressContainers.forEach((progressContainer) => {
      observer.observe(progressContainer);
    });
    // ================================ Floating Progress js End =================================

    // ========================= Increment & Decrement Js Start =====================
    $(document).on("click", ".increment-btn", function () {
      const $input = $(this).siblings(".input-value");
      let count = parseInt($input.val(), 10);
      $input.val(count + 1);
    });

    $(document).on("click", ".decrement-btn", function () {
      const $input = $(this).siblings(".input-value");
      let count = parseInt($input.val(), 10);
      if (count > 0) {
        $input.val(count - 1);
      }
    });
    // ========================= Increment & Decrement Js End =====================

    // ========================= Woo-commerce Rating Toggle =========================
    $(".rating-select .stars a").each(function () {
      $(this).on("click", function (e) {
        e.preventDefault();
        $(this).siblings().removeClass("active");
        $(this).parent().parent().addClass("selected");
        $(this).addClass("active");
      });
    });
    // ========================= Woo-commerce Rating Toggle =========================

  });
  // ==========================================
  //      End Document Ready function
  // ==========================================

  // ========================= Preloader Js Start =====================
  $(window).on("load", function () {
    $(".loader-mask").fadeOut();
  });
  // ========================= Preloader Js End=====================

  // ========================= Header Sticky Js Start ==============
  $(window).on("scroll", function () {
    if ($(window).scrollTop() >= 260) {
      $(".header").addClass("fixed-header");
    } else {
      $(".header").removeClass("fixed-header");
    }
  });
  // ========================= Header Sticky Js End===================
})(jQuery);
