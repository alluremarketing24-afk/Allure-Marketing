// Import Lucide icons library
// import lucide from "lucide"

// Initialize Lucide icons
lucide.createIcons()



// Enhanced Video Modal Functions with Universal Format Support
function openVideoModal(el) {
  const videoSrc = el.dataset.videoSrc;
  const modal = document.getElementById("videoModal");
  const videoPlayer = document.getElementById("localVideoFrame");
  const videoSource = document.getElementById("videoSource");

  if (videoSrc) {
    // Show modal
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";

    // Load and play video
    videoSource.src = videoSrc;
    videoPlayer.load();
    videoPlayer.play();
  } else {
    console.error("No video source found.");
  }
}

function closeVideoModal() {
  const modal = document.getElementById("videoModal");
  const videoPlayer = document.getElementById("localVideoFrame");
  const videoSource = document.getElementById("videoSource");

  // Hide modal
  modal.classList.add("hidden");
  document.body.style.overflow = "auto";

  // Stop and reset video
  videoPlayer.pause();
  videoPlayer.currentTime = 0;
  videoSource.src = "";
  videoPlayer.load();
}


function getYoutubeEmbedUrl(url) {
  try {
    let videoId;
    if (url.includes("youtube.com")) {
      const urlObj = new URL(url);
      videoId = urlObj.searchParams.get("v");
    } else if (url.includes("youtu.be")) {
      videoId = url.split("/").pop();
    }
    return `https://www.youtube.com/embed/${videoId}?autoplay=1`;
  } catch (e) {
    return ""; // fallback
  }
}





function setupLocalVideo(videoSrc, videoElement, errorElement) {
  // Clear previous sources
  const sources = videoElement.querySelectorAll("source")
  sources.forEach((source) => {
    source.src = ""
    source.type = ""
  })

  // Detect video format and set up sources
  const videoFormats = detectVideoFormat(videoSrc)

  if (videoFormats.length === 0) {
    showVideoError(errorElement, videoElement)
    return
  }

  // Set up multiple sources for better compatibility
  videoFormats.forEach((format, index) => {
    if (sources[index]) {
      sources[index].src = format.src
      sources[index].type = format.type
    }
  })

  // Set up error handling
  videoElement.addEventListener(
    "error",
    () => {
      showVideoError(errorElement, videoElement)
    },
    { once: true },
  )

  videoElement.addEventListener(
    "loadeddata",
    () => {
      errorElement.style.display = "none"
    },
    { once: true },
  )

  // Load and play the video
  videoElement.load()

  // Attempt to play after a short delay
  setTimeout(() => {
    const playPromise = videoElement.play()
    if (playPromise !== undefined) {
      playPromise.catch((error) => {
        console.log("Auto-play prevented:", error)
      })
    }
  }, 300)
}

function detectVideoFormat(videoSrc) {
  const formats = []
  const extension = videoSrc.split(".").pop().toLowerCase()

  // Map of video extensions to MIME types
  const videoMimeTypes = {
    mp4: "video/mp4",
    m4v: "video/mp4",
    webm: "video/webm",
    ogv: "video/ogg",
    ogg: "video/ogg",
    mov: "video/quicktime",
    qt: "video/quicktime",
    avi: "video/x-msvideo",
    wmv: "video/x-ms-wmv",
    flv: "video/x-flv",
    mkv: "video/x-matroska",
    "3gp": "video/3gpp",
    "3g2": "video/3gpp2",
    asf: "video/x-ms-asf",
    rm: "video/vnd.rn-realvideo",
    rmvb: "video/vnd.rn-realvideo",
  }

  const mimeType = videoMimeTypes[extension]

  if (mimeType) {
    formats.push({
      src: videoSrc,
      type: mimeType,
    })

    // Add codec-specific variants for better compatibility
    if (extension === "mp4") {
      formats.push({
        src: videoSrc,
        type: 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"',
      })
    } else if (extension === "webm") {
      formats.push({
        src: videoSrc,
        type: 'video/webm; codecs="vp8, vorbis"',
      })
      formats.push({
        src: videoSrc,
        type: 'video/webm; codecs="vp9, opus"',
      })
    }
  }

  return formats
}

function showVideoError(errorElement, videoElement) {
  videoElement.style.display = "none"
  errorElement.style.display = "flex"
}

// function closeVideoModal() {
//   const modal = document.getElementById("videoModal")
//   const iframe = document.getElementById("videoFrame")
//   const localVideo = document.getElementById("localVideoFrame")
//   const videoError = document.getElementById("videoError")

//   // Hide modal with animation
//   modal.classList.remove("active")

//   // Stop and clear all video sources
//   setTimeout(() => {
//     // Clear iframe
//     iframe.src = ""

//     // Stop and clear local video
//     localVideo.pause()
//     localVideo.currentTime = 0
//     const sources = localVideo.querySelectorAll("source")
//     sources.forEach((source) => {
//       source.src = ""
//     })
//     localVideo.load()

//     // Hide error state
//     videoError.style.display = "none"

//     // Reset display states
//     iframe.style.display = "none"
//     localVideo.style.display = "none"
//   }, 300)

//   // Restore body scroll
//   document.body.style.overflow = "auto"
// }

// Portfolio Category Filter
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove active class from all buttons
      document.querySelectorAll(".filter-btn").forEach((b) => b.classList.remove("active"))

      // Add active class to clicked button
      this.classList.add("active")

      const category = this.getAttribute("data-category")
      const reelContainers = document.querySelectorAll(".reel-container")

      reelContainers.forEach((container) => {
        if (category === "all" || container.getAttribute("data-category") === category) {
          container.style.display = "block"
          container.style.opacity = "0"
          container.style.transform = "scale(0.8)"

          setTimeout(() => {
            container.style.opacity = "1"
            container.style.transform = "scale(1)"
          }, 100)
        } else {
          container.style.opacity = "0"
          container.style.transform = "scale(0.8)"

          setTimeout(() => {
            container.style.display = "none"
          }, 300)
        }
      })
    })
  })
})

// Close modal when clicking outside
document.addEventListener("DOMContentLoaded", () => {
  const videoModal = document.getElementById("videoModal")
  if (videoModal) {
    videoModal.addEventListener("click", function (e) {
      if (e.target === this) {
        closeVideoModal()
      }
    })
  }
})

// Close modal with ESC key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeVideoModal()

    // Also close mobile menu if open
    const menu = document.getElementById("mobileMenu")
    const hamburger = document.getElementById("hamburger")
    if (menu && menu.classList.contains("active")) {
      menu.classList.remove("active")
      hamburger.classList.remove("active")
      document.body.style.overflow = "auto"
    }
  }
})

// Close mobile menu when clicking outside
document.addEventListener("click", (event) => {
  const menu = document.getElementById("mobileMenu")
  const hamburger = document.getElementById("hamburger")

  if (menu && hamburger && !menu.contains(event.target) && !hamburger.contains(event.target)) {
    menu.classList.remove("active")
    hamburger.classList.remove("active")
    document.body.style.overflow = "auto"
  }
})

// Enhanced smooth scrolling for anchor links
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })
})

// Enhanced form submission
document.addEventListener("DOMContentLoaded", () => {
  const contactForm = document.getElementById("contactForm")
  if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault() // ✅ stop the reload

      const submitBtn = this.querySelector('button[type="submit"]')
      const originalText = submitBtn.textContent
      submitBtn.textContent = "Sending..."
      submitBtn.disabled = true

      const formData = new FormData(contactForm)
      const data = {}
      formData.forEach((value, key) => {
        data[key] = value
      })

      console.log("Sending form data via AJAX:", data)

      fetch("/contact_ajax/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),  // Optional if CSRF is enabled
        },
        body: JSON.stringify(data),
      })
        .then((res) => res.json())
        .then((result) => {
          console.log("Backend response:", result)

          if (result.success) {
            showToast(result.message)
            contactForm.reset()
          } else if (result.errors) {
            showToast("Please correct the errors in the form.")

            console.log("Form errors:", result.errors)
          } else {
            showToast("Something went wrong.")

          }
        })
        .catch((error) => {
          console.error("AJAX error:", error)
          showToast("Something went wrong.")

        })
        .finally(() => {
          submitBtn.textContent = originalText
          submitBtn.disabled = false
        })
    })
  }
})

// Optional helper if CSRF is enabled
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}


// Enhanced scroll animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1"
      entry.target.style.transform = "translateY(0)"
    }
  })
}, observerOptions)

// Observe elements for scroll animations
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".premium-card, .service-card, .testimonial-card, .reel-container").forEach((el) => {
    el.style.opacity = "0"
    el.style.transform = "translateY(30px)"
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease"
    observer.observe(el)
  })
})

// Enhanced loading animation
window.addEventListener("load", () => {
  document.body.style.opacity = "1"
})

// Reel hover effects
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".reel-container").forEach((container) => {
    container.addEventListener("mouseenter", function () {
      const playButton = this.querySelector(".reel-play-button")
      if (playButton) {
        playButton.style.transform = "translate(-50%, -50%) scale(1.1)"
      }
    })

    container.addEventListener("mouseleave", function () {
      const playButton = this.querySelector(".reel-play-button")
      if (playButton) {
        playButton.style.transform = "translate(-50%, -50%) scale(1)"
      }
    })
  })
})
function showToast(message, duration = 4000) {
  const toast = document.getElementById("toast");
  const toastMessage = document.getElementById("toast-message");

  toastMessage.textContent = message;

  // Reset styles
  toast.classList.remove("hidden", "-translate-x-full", "opacity-0");
  toast.classList.add("translate-x-0", "opacity-100");

  // Hide after duration
  setTimeout(() => {
    toast.classList.remove("translate-x-0", "opacity-100");
    toast.classList.add("-translate-x-full", "opacity-0");

    // Wait for transition to complete before hiding
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 500); // match transition duration
  }, duration);
}


document.addEventListener("DOMContentLoaded", function () {
  const decisionDropdown = document.getElementById("id_is_decision_maker"); // ✅ Corrected ID
  const decisionFields = document.getElementById("decisionFields");

  if (!decisionDropdown || !decisionFields) return;

  function toggleDecisionFields() {
    if (decisionDropdown.value === "no") {
      decisionFields.classList.remove("hidden");
    } else {
      decisionFields.classList.add("hidden");
    }
  }

  // Initialize and listen
  toggleDecisionFields();
  decisionDropdown.addEventListener("change", toggleDecisionFields);
});


// REPLACE your existing mobile menu JavaScript with this

// Enhanced Mobile Menu Functions
function toggleMobileMenu() {
  const menu = document.getElementById("mobileMenu");
  const hamburger = document.getElementById("hamburger");
  const body = document.body;

  console.log("Toggle called"); // Debug log
  
  if (menu && hamburger) {
      menu.classList.toggle("active");
      hamburger.classList.toggle("active");

      // Prevent body scroll when menu is open
      if (menu.classList.contains("active")) {
          body.classList.add("menu-open");
          console.log("Menu opened"); // Debug log
      } else {
          body.classList.remove("menu-open");
          console.log("Menu closed"); // Debug log
      }
  } else {
      console.error("Menu or hamburger element not found");
  }
}

function closeMobileMenu() {
  const menu = document.getElementById("mobileMenu");
  const hamburger = document.getElementById("hamburger");
  const body = document.body;

  if (menu && hamburger) {
      menu.classList.remove("active");
      hamburger.classList.remove("active");
      body.classList.remove("menu-open");
  }
}

// Close mobile menu when clicking outside
document.addEventListener("click", (event) => {
  const menu = document.getElementById("mobileMenu");
  const hamburger = document.getElementById("hamburger");

  if (menu && hamburger && 
      !menu.contains(event.target) && 
      !hamburger.contains(event.target) &&
      menu.classList.contains("active")) {
      closeMobileMenu();
  }
});

// Close mobile menu with ESC key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
      const menu = document.getElementById("mobileMenu");
      if (menu && menu.classList.contains("active")) {
          closeMobileMenu();
      }
  }
});

// Enhanced smooth scrolling for anchor links
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
          e.preventDefault();
          const target = document.querySelector(this.getAttribute("href"));
          if (target) {
              // Add offset for fixed navigation
              const offsetTop = target.offsetTop - 80;
              window.scrollTo({
                  top: offsetTop,
                  behavior: "smooth"
              });
          }
      });
  });
});