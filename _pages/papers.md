---
layout: page
permalink: /papers/
title: Papers
description:
nav: true
nav_order: 5
---

<!-- _pages/papers.md -->

<div class="publications papers-page">

{% bibliography %}

</div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    var page = document.querySelector(".publications.papers-page");
    if (!page) return;

    var headings = Array.prototype.slice.call(page.querySelectorAll("h2.bibliography"));
    var cutoffHeading = headings.find(function (heading) {
      return heading.textContent.trim() === "2018";
    });
    if (!cutoffHeading) return;

    var cutoffList = cutoffHeading.nextElementSibling;
    if (!cutoffList || !cutoffList.matches("ol.bibliography")) return;

    cutoffHeading.textContent = "2018 and earlier";
    headings.forEach(function (heading) {
      var year = parseInt(heading.textContent.trim(), 10);
      if (Number.isNaN(year) || year >= 2018) return;

      var list = heading.nextElementSibling;
      if (list && list.matches("ol.bibliography")) {
        Array.prototype.slice.call(list.children).forEach(function (item) {
          cutoffList.appendChild(item);
        });
        list.remove();
      }
      heading.remove();
    });
  });
</script>
