document.addEventListener("DOMContentLoaded", function () {
  const filter = document.getElementById("work-category-filter");
  const count = document.getElementById("works-count");
  const grid = document.getElementById("works-grid");
  const pagination = document.getElementById("works-pagination");

  if (!filter || !count || !grid || !pagination) return;

  function buildFilteredUrl(sourceUrl, keepPage) {
    const url = new URL(sourceUrl || window.location.href);

    if (!keepPage) {
      url.searchParams.delete("page");
    }

    if (filter.value) {
      url.searchParams.set("category", filter.value);
    } else {
      url.searchParams.delete("category");
    }

    return url;
  }

  function replaceWorks(html) {
    const doc = new DOMParser().parseFromString(html, "text/html");
    const nextCount = doc.getElementById("works-count");
    const nextGrid = doc.getElementById("works-grid");
    const nextPagination = doc.getElementById("works-pagination");

    if (!nextCount || !nextGrid || !nextPagination) {
      throw new Error("Works markup was not found in response");
    }

    count.innerHTML = nextCount.innerHTML;
    grid.innerHTML = nextGrid.innerHTML;
    pagination.innerHTML = nextPagination.innerHTML;

    if (window.AOS) {
      AOS.refreshHard();
    }
  }

  function loadWorks(url) {
    filter.disabled = true;
    grid.classList.add("opacity-50");
    pagination.classList.add("pe-none");

    fetch(url.toString(), {
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error("Works request failed");
        }
        return response.text();
      })
      .then(function (html) {
        replaceWorks(html);
      })
      .catch(function (error) {
        console.error("Works filter error:", error);
      })
      .finally(function () {
        filter.disabled = false;
        grid.classList.remove("opacity-50");
        pagination.classList.remove("pe-none");
      });
  }

  filter.addEventListener("change", function () {
    loadWorks(buildFilteredUrl(window.location.href, false));
  });

  pagination.addEventListener("click", function (event) {
    const link = event.target.closest("a");
    if (!link) return;

    event.preventDefault();
    loadWorks(buildFilteredUrl(link.href, true));
  });
});
