// Zoom functionality with min/max limits
const MIN_ZOOM = 0.5;  // 50% minimum zoom
const MAX_ZOOM = 1.5;   // 200% maximum zoom
const ZOOM_STEP = 0.1;  // 10% increment per click
const magicCursor = new MagicCursor();

let currentZoom = 1.0; // Start at 100%

// Get elements
const zoomContainer = document.getElementById('zoomContainer');
const zoomInBtn = document.getElementById('zoomIn');
const zoomOutBtn = document.getElementById('zoomOut');
const zoomLevelDisplay = document.getElementById('zoomLevel');

// Load saved zoom level from localStorage
function loadZoomLevel() {
  const savedZoom = localStorage.getItem('pageZoom');
  if (savedZoom) {
    currentZoom = parseFloat(savedZoom);
    applyZoom();
  }
}

// Save zoom level to localStorage
function saveZoomLevel() {
  localStorage.setItem('pageZoom', currentZoom.toString());
}

// Apply zoom transform
function applyZoom() {
  zoomContainer.style.transform = `scale(${currentZoom})`;
  zoomContainer.style.transformOrigin = 'center top';
  zoomLevelDisplay.textContent = `${Math.round(currentZoom * 100)}%`;
  
  // Enable/disable buttons based on limits
  zoomInBtn.disabled = currentZoom >= MAX_ZOOM;
  zoomOutBtn.disabled = currentZoom <= MIN_ZOOM;
  
  saveZoomLevel();
}

// Zoom in function
function zoomIn() {
  if (currentZoom < MAX_ZOOM) {
    currentZoom = Math.min(currentZoom + ZOOM_STEP, MAX_ZOOM);
    applyZoom();
  }
}

// Zoom out function
function zoomOut() {
  if (currentZoom > MIN_ZOOM) {
    currentZoom = Math.max(currentZoom - ZOOM_STEP, MIN_ZOOM);
    applyZoom();
  }
}

// Keyboard shortcuts (Ctrl/Cmd + Plus/Minus)
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === '=') {
    e.preventDefault();
    zoomIn();
  } else if ((e.ctrlKey || e.metaKey) && e.key === '-') {
    e.preventDefault();
    zoomOut();
  } else if ((e.ctrlKey || e.metaKey) && e.key === '0') {
    e.preventDefault();
    currentZoom = 1.0;
    applyZoom();
  }
});

// Mouse wheel zoom (Ctrl/Cmd + Scroll)
document.addEventListener('wheel', (e) => {
  if (e.ctrlKey || e.metaKey) {
    e.preventDefault();
    if (e.deltaY < 0) {
      zoomIn();
    } else {
      zoomOut();
    }
  }
}, { passive: false });

// Button event listeners
zoomInBtn.addEventListener('click', zoomIn);
zoomOutBtn.addEventListener('click', zoomOut);

// Initialize on page load
window.addEventListener('load', () => {
  loadZoomLevel();
  applyZoom();
});
// Fade in on page load
document.body.classList.remove("page-fade");

// Fade out before leaving
document.querySelectorAll("a").forEach(link => {
  link.addEventListener("click", e => {
    const url = link.getAttribute("href");

    // Ignore empty or # links
    if (!url || url.startsWith("#")) return;

    e.preventDefault();

    document.body.classList.add("page-fade");

    setTimeout(() => {
      window.location.href = url;
    }, 450); // match CSS duration
  });
});
