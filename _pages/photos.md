---
layout: page
permalink: /photos/
title: Lab Life
nav: false
---

<style>
.photo-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-top: 1rem;
}

.photo-item {
  cursor: pointer;
}

.photo-item img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 4px;
  display: block;
  transition: opacity 0.2s ease;
}

.photo-item:hover img {
  opacity: 0.88;
}

.photo-caption {
  font-size: 0.75rem;
  font-style: italic;
  color: var(--secondary-color);
  margin-top: 0.35rem;
}

/* Lightbox */
.lightbox-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.88);
  z-index: 9999;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
}

.lightbox-overlay.active {
  display: flex;
}

.lightbox-overlay img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 2px;
  cursor: default;
}

@media (max-width: 600px) {
  .photo-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="photo-grid">
  <div class="photo-item" onclick="openLightbox(this)">
    <img src="/assets/img/lab/april2026.jpeg" alt="April 2026">
    <p class="photo-caption">April 2026</p>
  </div>
  <div class="photo-item" onclick="openLightbox(this)">
    <img src="/assets/img/lab/dec2025.JPG" alt="NeurIPS 2025">
    <p class="photo-caption">NeurIPS 2025</p>
  </div>
  <div class="photo-item" onclick="openLightbox(this)">
    <img src="/assets/img/lab/halloween2025.jpg" alt="Halloween 2025">
    <p class="photo-caption">Halloween 2025</p>
  </div>
  <div class="photo-item" onclick="openLightbox(this)">
    <img src="/assets/img/lab/oct2025.jpg" alt="October 2025">
    <p class="photo-caption">October 2025</p>
  </div>
    <div class="photo-item" onclick="openLightbox(this)">
    <img src="/assets/img/lab/june2025.jpeg" alt="June 2025">
    <p class="photo-caption">June 2025</p>
  </div>
</div>

<div class="lightbox-overlay" id="lightbox" onclick="closeLightbox()">
  <img id="lightbox-img" src="" alt="">
</div>

<script>
function openLightbox(item) {
  const src = item.querySelector('img').src;
  const alt = item.querySelector('img').alt;
  document.getElementById('lightbox-img').src = src;
  document.getElementById('lightbox-img').alt = alt;
  document.getElementById('lightbox').classList.add('active');
}

function closeLightbox() {
  document.getElementById('lightbox').classList.remove('active');
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeLightbox();
});
</script>
