console.log("Script loaded!");

// ====== API BASE URL ======
const API_BASE = "http://127.0.0.1:5000/api";

// ================= DYNAMIC HEADER & FOOTER =================
function loadHeaderFooter() {
    const headerHTML = `
      <header class="navbar">
          <a href="index.html" class="logo"><img src="assets/images/Logo_final.png" alt="KKM"></a>

        <button class="menu-btn" aria-label="Toggle menu">
            <i class="fas fa-bars"></i>
        </button>

        <nav class="nav">
            <ul class="nav-links">
                <li><a href="index.html" data-page="index">Home</a></li>
                <li><a href="buy.html" data-page="buy">Listings</a></li>
                <li><a href="sell.html" data-page="sell">Sell</a></li>
                <li><a href="about.html" data-page="about">About</a></li>
                <li><a href="contact.html" data-page="contact">Contact</a></li>
            </ul>

            <!-- Sign In Button - Shows in mobile menu -->
            <div class="nav-actions" id="mobileNavActions">
                <a href="login.html" class="sign-in-link">
                    <button class="submit-btn">Sign in</button>
                </a>
            </div>
        </nav>

        <!-- Desktop Sign In Button -->
        <div class="nav-actions" id="navActions">
            <a href="login.html" class="sign-in-link">
                <button class="submit-btn">Sign in</button>
            </a>
        </div>
    </header>
    `;

    const footerHTML = `
       <footer class="carft" id="siteFooter">
            <div class="wrap">
                <div class="grid">
                    <!-- Brand / About -->
                    <div>
                        <div class="brand">
                            <div class="logo" aria-hidden="true">
                                <!-- simple car icon -->
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M5 11l1.5-4.5A3 3 0 0 1 9.3 4h5.4a3 3 0 0 1 2.8 2.5L19 11h1a2 2 0 0 1 2 2v3h-2v1a1 1 0 0 1-2 0v-1H6v1a1 1 0 0 1-2 0v-1H2v-3a2 2 0 0 1 2-2h1zm2.2-1h9.6l-.9-2.8A1.5 1.5 0 0 0 14.7 6H9.3a1.5 1.5 0 0 0-1.4 1.2L7.2 10zM6.5 15A1.5 1.5 0 1 0 6.5 12 1.5 1.5 0 0 0 6.5 15zm11 0A1.5 1.5 0 1 0 17.5 12 1.5 1.5 0 0 0 17.5 15z" />
                                </svg>
                            </div>
                            <div class="brandText">Your Brand Motors</div>
                        </div>
                        <p class="muted" style="margin:10px 0 0;max-width:38ch">Premium new & used cars with trusted service, finance, and doorstep test-drives.</p>
                        <div class="social" aria-label="Social links">
                            <a aria-label="Facebook" href="#" target="_blank" rel="noopener">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M13 9h3V6h-3c-1.66 0-3 1.34-3 3v2H8v3h2v7h3v-7h3l1-3h-4V9c0-.55.45-1 1-1z" />
                                </svg>
                            </a>
                            <a aria-label="Instagram" href="#" target="_blank" rel="noopener">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7zm5 3.5A5.5 5.5 0 1 1 6.5 13 5.5 5.5 0 0 1 12 7.5zm0 2A3.5 3.5 0 1 0 15.5 13 3.5 3.5 0 0 0 12 9.5zM18 7.2a1 1 0 1 0 1 1 1 1 0 0 0-1-1z" />
                                </svg>
                            </a>
                            <a aria-label="YouTube" href="#" target="_blank" rel="noopener">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M23 7s-.2-1.5-.8-2.1c-.8-.8-1.7-.8-2.1-.9C17.9 4 12 4 12 4h0s-5.9 0-8.1.1c-.4 0-1.3.1-2.1.9C1.2 5.5 1 7 1 7S.9 8.7.9 10.4v1.2C.9 13.3 1 15 1 15s.2 1.5.8 2.1c.8.8 1.8.8 2.2.9C6.1 18.1 12 18.1 12 18.1s5.9 0 8.1-.1c.4 0 1.3-.1 2.1-.9.6-.6.8-2.1.8-2.1s.1-1.7.1-3.4v-1.2C23.1 8.7 23 7 23 7zM9.8 14.3V7.9l6 3.2-6 3.2z" />
                                </svg>
                            </a>
                            <a aria-label="X (Twitter)" href="#" target="_blank" rel="noopener">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M3 3h4.6l4.1 6.1L16.9 3H21l-7.1 9.5L21 21h-4.6l-4.4-6.5L7.1 21H3l7.5-8.6L3 3z" />
                                </svg>
                            </a>
                        </div>
                    </div>

                    <!-- Contact -->
                    <div>
                        <h4>Contact</h4>
                        <ul class="contact muted">
                            <li>
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M12 2L3 9v13h6v-6h6v6h6V9z" />
                                </svg>
                                <span> NH-8, AutoDrive Arena, Ahmedabad, Gujarat 380015</span>
                            </li>
                            <li>
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M6.6 10.8A15.1 15.1 0 0 0 13.2 17l2.2-2.2c.3-.3.8-.4 1.2-.2 1 .4 2 .7 3.1.8.5 0 .9.5.9 1v3.5c0 .6-.5 1-1.1 1A18.5 18.5 0 0 1 3 5.6C3 5 3.5 4.5 4.1 4.5H7.6c.5 0 1 .4 1 1 0 1.1.3 2.1.8 3.1.2.4.1.9-.2 1.2L6.6 10.8z" />
                                </svg>
                                <a href="tel:+919999999999"> +91 99999 99999</a>
                            </li>
                            <li>
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" />
                                </svg>
                                <a href="mailto:hello@autodrive.in"> hello@autodrive.in</a>
                            </li>
                            <li>
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M12 2a8 8 0 0 0-8 8c0 5.3 8 12 8 12s8-6.7 8-12a8 8 0 0 0-8-8zm0 10.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z" />
                                </svg>
                                <a href="#" target="_blank" rel="noopener"> Find us on Maps</a>
                            </li>
                        </ul>
                    </div>

                    <!-- Quick Links -->
                    <div>
                        <h4>Quick Links</h4>
                        <ul class="muted">
                            <li><a href="index.html">Home</a></li>
                            <li><a href="buy.html">Listings</a></li>
                            <li><a href="sell.html">Sell</a></li>
                            <li><a href="about.html">About</a></li>
                            <li><a href="#">Contact</a></li>
                        </ul>
                    </div>

                    <!-- Hours -->
                    <div>
                        <h4>Showroom Hours</h4>
                        <ul class="muted">
                            <li>Mon–Sat: 9:30 AM – 8:00 PM</li>
                            <li>Sunday: 10:00 AM – 6:00 PM</li>
                            <li>24×7 Roadside Assist</li>
                        </ul>
                    </div>
                </div>

                <div class="bottom">
                    <div>© <span id="year"></span> Your Brand Motors. All rights reserved.</div>
                    <div class="legal">
                        <a href="#">Privacy</a>
                        <a href="#">Terms</a>
                        <a href="#">Cookies</a>
                    </div>
                </div>
            </div>
        </footer>
    `;

    // Inject header if missing
    if (!document.querySelector('.navbar')) {
        document.body.insertAdjacentHTML('afterbegin', headerHTML);
    }

    // Inject footer only if NOT on car detail page
    if (!document.querySelector('.footer') && !window.isCarDetailPage) {
        document.body.insertAdjacentHTML('beforeend', footerHTML);
    }

    // Update year in footer
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // Dispatch custom event to notify other scripts
    console.log("✅ Dispatching headerFooterLoaded event");
    window.dispatchEvent(new Event('headerFooterLoaded'));

    // Set active page after header is loaded
    setActivePage();

    // Setup mobile menu toggle
    setupMobileMenu();
}

// ================= ACTIVE PAGE HIGHLIGHTING =================
function setActivePage() {
    // Get current page filename
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';

    // Extract page name without extension
    let pageName = currentPage.replace('.html', '');

    // Handle home page (empty string or index)
    if (pageName === '' || pageName === 'index') {
        pageName = 'index';
    }

    console.log("🎯 Current page:", pageName);

    // Find all nav links
    const navLinks = document.querySelectorAll('.nav-links a');

    // Remove active class from all links first
    navLinks.forEach(link => {
        link.classList.remove('active');
    });

    // Add active class to matching link
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('data-page');
        if (linkPage === pageName) {
            link.classList.add('active');
            console.log("✅ Set active class on:", linkPage);
        }
    });
}

// ================= MOBILE MENU TOGGLE =================
function setupMobileMenu() {
    const menuBtn = document.querySelector('.menu-btn');
    const nav = document.querySelector('.nav');

    if (!menuBtn || !nav) return;

    menuBtn.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuBtn.classList.toggle('active');
    });

    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            nav.classList.remove('active');
            menuBtn.classList.remove('active');
        });
    });

    // Close menu when clicking overlay
    document.addEventListener('click', (e) => {
        if (nav.classList.contains('active') &&
            !nav.contains(e.target) &&
            !menuBtn.contains(e.target)) {
            nav.classList.remove('active');
            menuBtn.classList.remove('active');
        }
    });
}

// ================= NAVBAR LOGIN/SIGNUP =================
function renderNavbar() {
    console.log("🔧 Rendering navbar...");

    // Update both desktop and mobile nav actions
    const navActions = document.getElementById("navActions");
    const mobileNavActions = document.getElementById("mobileNavActions");

    if (!navActions) {
        console.error("❌ navActions element not found!");
        return;
    }

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    console.log("🔐 Token exists:", !!token);
    console.log("👤 Username:", username);

    // Clear both sections
    navActions.innerHTML = "";
    if (mobileNavActions) mobileNavActions.innerHTML = "";

    if (token && username) {
        console.log("✅ User is logged in, showing username and logout");

        const userHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="color: #333; font-weight: 600;">
                    <i class="fas fa-user-circle" style="margin-right: 5px;"></i>${username}
                </span>
                <button class="submit-btn" id="logoutBtn" style="background: #ffb400;">Logout</button>
            </div>
        `;

        navActions.innerHTML = userHTML;
        if (mobileNavActions) mobileNavActions.innerHTML = userHTML;

        // Add logout functionality
        const logoutButtons = document.querySelectorAll("#logoutBtn");
        logoutButtons.forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.preventDefault();
                logout();
            });
        });
    } else {
        console.log("🔓 User not logged in, showing sign in button");

        const signInHTML = `
            <a href="login.html" class="sign-in-link">
                <button class="submit-btn">Sign in</button>
            </a>
        `;

        navActions.innerHTML = signInHTML;
        if (mobileNavActions) mobileNavActions.innerHTML = signInHTML;
    }
}

function logout() {
    console.log("🚪 Logging out user...");
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_fullname");

    console.log("✅ User data cleared from localStorage");

    // Show logout message
    alert("You have been logged out successfully!");

    // Reload page or redirect to home
    window.location.href = "index.html";
}

// ================= BRANDS TOGGLE =================
function setupBrandToggle() {
    const toggleBtn = document.getElementById('toggleBrands');
    const hiddenBrands = document.querySelectorAll('.brand-card.hidden');

    if (!toggleBtn) return;

    let expanded = false;
    toggleBtn.addEventListener('click', () => {
        expanded = !expanded;
        hiddenBrands.forEach(brand => {
            brand.style.display = expanded ? 'block' : 'none';
        });
        toggleBtn.textContent = expanded ? 'View Less Brands' : 'View More Brands';
    });
}

// ================= HOME PAGE FEATURED CARS =================
async function loadFeaturedCars() {
    const grid = document.getElementById("vehicleGrid");
    const msg = document.getElementById("noCarsMsg");
    if (!grid) return;

    grid.innerHTML = `
        <div style="text-align: center; width: 100%; padding: 40px;">
            <i class="fas fa-spinner fa-spin" style="font-size: 40px;"></i>
            <p style="margin-top: 15px; color: #666;">Loading vehicles...</p>
        </div>
    `;

    try {
        const res = await fetch(`${API_BASE}/cars`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const cars = Array.isArray(data) ? data : data.cars || [];

        grid.innerHTML = "";
        if (!cars.length) {
            if (msg) {
                msg.style.display = "block";
                msg.textContent = "No cars available at the moment.";
            }
            return;
        }

        if (msg) msg.style.display = "none";
        const featuredCars = cars.slice(0, 4);

        featuredCars.forEach(car => {
            const imgSrc = (car.images && car.images.length > 0) ? car.images[0] : "assets/images/placeholder.jpg";
            const badgeColor = (car.mileage && car.mileage < 10000) ? "blue" : "green";
            const badgeText = badgeColor === "blue" ? "Low Mileage" : "Great Price";

            const card = document.createElement("div");
            card.className = "vehicle-card";
            card.innerHTML = `
                <img src="${imgSrc}" 
                     alt="${escapeHtml(car.name)}" 
                     onerror="this.src='assets/images/placeholder.jpg'"
                     loading="lazy">
                <span class="badge ${badgeColor}">${badgeText}</span>
                <h3>${escapeHtml(car.name || 'Unknown Car')}</h3>
                <p class="miles">
                    ${escapeHtml(
                        (car.mileage ? car.mileage + " Miles" : '') +
                        (car.fuel_type ? " • " + car.fuel_type : '') +
                        (car.transmission ? " • " + car.transmission : '')
                    )}
                </p>
                <div class="price-details">
                    <span class="price">₹${formatPrice(car.price)}</span>
                    <a href="cardetail.html?id=${car.id}" class="details-link">View Details →</a>
                </div>
            `;
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            grid.appendChild(card);

            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        });
    } catch (err) {
        console.error("❌ Error loading cars:", err);
        grid.innerHTML = "";
        if (msg) {
            msg.style.display = "block";
            msg.innerHTML = `
                <i class="fas fa-exclamation-circle" style="color: #ffb400; margin-right: 8px;"></i>
                Error loading vehicles. Please try again later.
            `;
        }
    }
}

// ================= HELPER FUNCTIONS =================
function formatPrice(price) {
    if (!price) return "--";
    return Number(price).toLocaleString("en-IN");
}

function escapeHtml(text) {
    if (!text) return '';
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// ================= SELL FORM SUBMISSION =================
function setupSellForm() {
    const sellForm = document.getElementById("sellForm");
    const successBox = document.getElementById("sell-success");
    if (!sellForm) return;

    sellForm.addEventListener("submit", async(e) => {
        e.preventDefault();
        const submitBtn = sellForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn ? submitBtn.textContent : '';
        if (submitBtn) {
            submitBtn.textContent = 'Submitting...';
            submitBtn.disabled = true;
        }
        const formData = new FormData(sellForm);

        try {
            const res = await fetch(`${API_BASE}/sell_request`, {
                method: "POST",
                body: formData
            });
            const data = await res.json();
            if (data.ok) {
                sellForm.style.display = "none";
                if (successBox) successBox.style.display = "block";
                sellForm.reset();
            } else {
                alert(data.msg || "Something went wrong while submitting the form!");
                if (submitBtn) {
                    submitBtn.textContent = originalBtnText;
                    submitBtn.disabled = false;
                }
            }
        } catch (err) {
            console.error("❌ Error submitting sell request:", err);
            alert("Server error while submitting the form. Please try again later.");
            if (submitBtn) {
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
            }
        }
    });
}

// ================= TESTIMONIAL CAROUSEL =================
function setupTestimonialCarousel() {
    const testimonials = document.querySelectorAll('.kkm-testimonial');
    const prevBtn = document.getElementById('kkm-prev');
    const nextBtn = document.getElementById('kkm-next');
    if (!testimonials.length || !prevBtn || !nextBtn) return;

    let currentIndex = 0;

    function showTestimonial(index) {
        testimonials.forEach((t, i) => t.classList.toggle('active', i === index));
    }
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
        showTestimonial(currentIndex);
    });
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % testimonials.length;
        showTestimonial(currentIndex);
    });
    setInterval(() => {
        currentIndex = (currentIndex + 1) % testimonials.length;
        showTestimonial(currentIndex);
    }, 5000);
}

// ================= VIDEO MODAL =================
function setupVideoModal() {
    const playVideoBtn = document.getElementById('playVideoBtn');
    const videoModal = document.getElementById('videoModal');
    const closeVideoBtn = document.getElementById('closeVideoBtn');
    const carVideo = document.getElementById('carVideo');
    if (!playVideoBtn || !videoModal) return;

    playVideoBtn.addEventListener('click', function() {
        videoModal.style.display = 'flex';
        if (carVideo) carVideo.play();
    });
    if (closeVideoBtn) {
        closeVideoBtn.addEventListener('click', function() {
            videoModal.style.display = 'none';
            if (carVideo) {
                carVideo.pause();
                carVideo.currentTime = 0;
            }
        });
    }
    videoModal.addEventListener('click', function(e) {
        if (e.target === videoModal) {
            videoModal.style.display = 'none';
            if (carVideo) {
                carVideo.pause();
                carVideo.currentTime = 0;
            }
        }
    });
}

// ================= COUNTER ANIMATION =================
function setupCounterAnimation() {
    const counters = document.querySelectorAll('.stat-number');
    if (!counters.length) return;

    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        const unit = counter.getAttribute('data-unit') || '';
        const duration = 2000;
        const steps = 60;
        const increment = target / steps;
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target + unit;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current) + unit;
            }
        }, duration / steps);
    };

    // Intersection Observer for counter animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// ================= INIT =================
document.addEventListener("DOMContentLoaded", async() => {
    console.log("🚀 Initializing page...");

    // Step 1: Load header/footer first
    await loadHeaderFooter();

    // Step 2: Wait briefly to ensure DOM update
    await new Promise(resolve => setTimeout(resolve, 200));

    // Step 3: Initialize navbar (must happen after header loads)
    console.log("🔧 Setting up navbar...");
    renderNavbar();

    // Step 4: Initialize other modules
    setupBrandToggle();
    setupSellForm();
    setupTestimonialCarousel();
    setupVideoModal();
    setupCounterAnimation();

    // Step 5: Check which page and call appropriate init function
    if (window.isBuyPage && typeof window.initBuyPageCars === 'function') {
        console.log("🚗 Initializing buy page cars...");
        await window.initBuyPageCars();
    } else if (window.isCarDetailPage && typeof window.initCarDetailPage === 'function') {
        console.log("🚗 Initializing car detail page...");
        await window.initCarDetailPage();
    } else if (!window.isBuyPage && !window.isCarDetailPage) {
        console.log("🏠 Loading featured cars for home page");
        loadFeaturedCars();
    }

    console.log("✅ Page initialization complete");
});

// Listen for auth state changes across tabs
window.addEventListener('storage', (e) => {
    if (e.key === 'token' || e.key === 'username') {
        console.log("🔄 Auth state changed in another tab, updating navbar...");
        renderNavbar();
    }
});

// Listen for custom login event
window.addEventListener('userLoggedIn', () => {
    console.log("🎉 User logged in event received!");
    renderNavbar();
});

// Auto-rotate testimonial groups
(function() {
    const root = document.getElementById('testimonials');
    if (!root) return;

    const grid = root.querySelector('#tstGrid');
    const cards = Array.from(grid.querySelectorAll('.card'));
    const dotsWrap = root.querySelector('#tstDots');
    const GROUP_SIZE = 3;
    const groups = Math.ceil(cards.length / GROUP_SIZE);

    // Create dots
    for (let i = 0; i < groups; i++) {
        const d = document.createElement('span');
        d.className = 'dot';
        dotsWrap.appendChild(d);
    }
    const dots = Array.from(dotsWrap.children);

    function showGroup(g) {
        cards.forEach((card, idx) => {
            const inGroup = Math.floor(idx / GROUP_SIZE) === g;
            card.style.display = inGroup ? 'block' : 'none';
        });
        dots.forEach((d, i) => d.classList.toggle('active', i === g));
    }

    let current = 0;
    showGroup(current);
    setInterval(() => {
        current = (current + 1) % groups;
        showGroup(current);
    }, 5000);
})();