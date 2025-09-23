/**
 * JavaScript principal pour La Caravela
 */

// Configuration globale
window.Caravela = {
    // Configuration de l'application
    config: {
        apiBaseUrl: '/api/',
        stripePublishableKey: document.querySelector('meta[name="stripe-publishable-key"]')?.content || '',
        currency: 'MAD',
        locale: 'fr-FR'
    },

    // Utilitaires
    utils: {
        // Formater un prix
        formatPrice: function(price) {
            return new Intl.NumberFormat('fr-FR', {
                style: 'currency',
                currency: 'EUR'
            }).format(price);
        },

        // Formater une date
        formatDate: function(date) {
            return new Intl.DateTimeFormat('fr-FR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            }).format(new Date(date));
        },

        // Débouncer une fonction
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Throttler une fonction
        throttle: function(func, limit) {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        }
    },

    // Gestionnaire de notifications
    notifications: {
        show: function(message, type = 'info', duration = 5000) {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, duration);
        },

        success: function(message) {
            this.show(message, 'success');
        },

        error: function(message) {
            this.show(message, 'error');
        },

        info: function(message) {
            this.show(message, 'info');
        }
    },

    // Gestionnaire de modales
    modal: {
        open: function(modalId) {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('open');
                document.body.style.overflow = 'hidden';
            }
        },

        close: function(modalId) {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('open');
                document.body.style.overflow = '';
            }
        },

        closeAll: function() {
            document.querySelectorAll('.modal.open').forEach(modal => {
                modal.classList.remove('open');
            });
            document.body.style.overflow = '';
        }
    },

    // Gestionnaire de panier
    cart: {
        addItem: function(productId, quantity = 1, customizations = {}) {
            fetch('/checkout/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity,
                    customizations: customizations
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Caravela.notifications.success('Produit ajouté au panier !');
                    this.updateCartCount(data.cart_count);
                } else {
                    Caravela.notifications.error(data.error || 'Erreur lors de l\'ajout au panier');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                Caravela.notifications.error('Erreur lors de l\'ajout au panier');
            });
        },

        updateCartCount: function(count) {
            const cartCountElement = document.querySelector('.cart-count');
            if (cartCountElement) {
                cartCountElement.textContent = count;
            }
        },

        getCSRFToken: function() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                   document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
        }
    },

    // Gestionnaire de recherche
    search: {
        init: function() {
            const searchInput = document.querySelector('#search-input');
            if (searchInput) {
                const debouncedSearch = Caravela.utils.debounce(this.performSearch, 300);
                searchInput.addEventListener('input', debouncedSearch);
            }
        },

        performSearch: function(event) {
            const query = event.target.value;
            if (query.length < 2) return;

            fetch(`/products/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    this.displayResults(data.results);
                })
                .catch(error => {
                    console.error('Erreur de recherche:', error);
                });
        },

        displayResults: function(results) {
            const resultsContainer = document.querySelector('#search-results');
            if (!resultsContainer) return;

            resultsContainer.innerHTML = results.map(product => `
                <div class="search-result-item p-4 border-b border-gray-200 hover:bg-gray-50">
                    <a href="${product.url}" class="flex items-center">
                        <img src="${product.image}" alt="${product.name}" class="w-12 h-12 object-cover rounded mr-4">
                        <div>
                            <h4 class="font-semibold text-gray-900">${product.name}</h4>
                            <p class="text-sm text-gray-600">${product.price}</p>
                        </div>
                    </a>
                </div>
            `).join('');
        }
    },

    // Gestionnaire de lazy loading
    lazyLoading: {
        init: function() {
            const images = document.querySelectorAll('img[data-src]');
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        }
    },

    // Gestionnaire de navigation mobile
    mobileNav: {
        init: function() {
            const mobileMenuButton = document.querySelector('#mobile-menu-button');
            const mobileMenu = document.querySelector('#mobile-menu');
            const mobileMenuClose = document.querySelector('#mobile-menu-close');

            if (mobileMenuButton && mobileMenu) {
                mobileMenuButton.addEventListener('click', () => {
                    mobileMenu.classList.toggle('open');
                });
            }

            if (mobileMenuClose && mobileMenu) {
                mobileMenuClose.addEventListener('click', () => {
                    mobileMenu.classList.remove('open');
                });
            }

            // Fermer le menu en cliquant à l'extérieur
            document.addEventListener('click', (event) => {
                if (mobileMenu && !mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                    mobileMenu.classList.remove('open');
                }
            });
        }
    },

    // Gestionnaire de formulaires
    forms: {
        init: function() {
            this.initValidation();
            this.initAutoSave();
        },

        initValidation: function() {
            const forms = document.querySelectorAll('form[data-validate]');
            forms.forEach(form => {
                form.addEventListener('submit', this.validateForm);
            });
        },

        validateForm: function(event) {
            const form = event.target;
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    this.showFieldError(input, 'Ce champ est requis');
                    isValid = false;
                } else {
                    this.clearFieldError(input);
                }
            });

            if (!isValid) {
                event.preventDefault();
            }
        },

        showFieldError: function(field, message) {
            this.clearFieldError(field);
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
            field.classList.add('border-red-500');
        },

        clearFieldError: function(field) {
            const errorDiv = field.parentNode.querySelector('.error-message');
            if (errorDiv) {
                errorDiv.remove();
            }
            field.classList.remove('border-red-500');
        },

        initAutoSave: function() {
            const forms = document.querySelectorAll('form[data-autosave]');
            forms.forEach(form => {
                const inputs = form.querySelectorAll('input, textarea, select');
                inputs.forEach(input => {
                    input.addEventListener('change', () => {
                        this.autoSaveForm(form);
                    });
                });
            });
        },

        autoSaveForm: function(form) {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            
            localStorage.setItem(`form_${form.id}`, JSON.stringify(data));
            Caravela.notifications.info('Formulaire sauvegardé automatiquement');
        }
    },

    // Gestionnaire d'effets visuels dynamiques
    visualEffects: {
        init: function() {
            this.initScrollReveal();
            this.initParticleSystem();
            this.initHoverEffects();
            this.initGradientAnimations();
        },

        initScrollReveal: function() {
            const revealElements = document.querySelectorAll('.scroll-reveal');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                    }
                });
            }, { threshold: 0.1 });

            revealElements.forEach(el => observer.observe(el));
        },

        initParticleSystem: function() {
            const particlesContainer = document.querySelector('.particles');
            if (!particlesContainer) return;

            // Créer des particules supplémentaires
            for (let i = 0; i < 15; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 8 + 's';
                particle.style.animationDuration = (Math.random() * 4 + 6) + 's';
                particlesContainer.appendChild(particle);
            }
        },

        initHoverEffects: function() {
            // Effet de ripple sur les boutons
            document.querySelectorAll('.hover-ripple').forEach(button => {
                button.addEventListener('click', function(e) {
                    const ripple = document.createElement('span');
                    const rect = this.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    const x = e.clientX - rect.left - size / 2;
                    const y = e.clientY - rect.top - size / 2;

                    ripple.style.width = ripple.style.height = size + 'px';
                    ripple.style.left = x + 'px';
                    ripple.style.top = y + 'px';
                    ripple.style.position = 'absolute';
                    ripple.style.borderRadius = '50%';
                    ripple.style.background = 'rgba(255, 255, 255, 0.6)';
                    ripple.style.animation = 'ripple 0.6s linear';
                    ripple.style.pointerEvents = 'none';

                    this.appendChild(ripple);

                    setTimeout(() => {
                        ripple.remove();
                    }, 600);
                });
            });

            // Effet de tilt sur les cartes
            document.querySelectorAll('.hover-tilt').forEach(card => {
                card.addEventListener('mousemove', function(e) {
                    const rect = this.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;

                    this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
                });

                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
                });
            });
        },

        initGradientAnimations: function() {
            // Animer les gradients de texte
            document.querySelectorAll('.gradient-text').forEach(element => {
                element.addEventListener('mouseenter', function() {
                    this.style.animationDuration = '1s';
                });

                element.addEventListener('mouseleave', function() {
                    this.style.animationDuration = '3s';
                });
            });
        }
    },

    // Gestionnaire d'animations avancées
    animations: {
        init: function() {
            this.initCounterAnimations();
            this.initProgressBars();
            this.initTypewriter();
        },

        initCounterAnimations: function() {
            const counters = document.querySelectorAll('[data-counter]');
            counters.forEach(counter => {
                const target = parseInt(counter.dataset.counter);
                const duration = parseInt(counter.dataset.duration) || 2000;
                const increment = target / (duration / 16);
                let current = 0;

                const updateCounter = () => {
                    current += increment;
                    if (current < target) {
                        counter.textContent = Math.floor(current);
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target;
                    }
                };

                // Démarrer l'animation quand l'élément est visible
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            updateCounter();
                            observer.unobserve(entry.target);
                        }
                    });
                });

                observer.observe(counter);
            });
        },

        initProgressBars: function() {
            const progressBars = document.querySelectorAll('[data-progress]');
            progressBars.forEach(bar => {
                const target = parseInt(bar.dataset.progress);
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            bar.style.width = target + '%';
                            observer.unobserve(entry.target);
                        }
                    });
                });

                observer.observe(bar);
            });
        },

        initTypewriter: function() {
            const typewriterElements = document.querySelectorAll('[data-typewriter]');
            typewriterElements.forEach(element => {
                const text = element.dataset.typewriter;
                const speed = parseInt(element.dataset.speed) || 100;
                let i = 0;

                const type = () => {
                    if (i < text.length) {
                        element.textContent += text.charAt(i);
                        i++;
                        setTimeout(type, speed);
                    }
                };

                // Démarrer l'animation quand l'élément est visible
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            type();
                            observer.unobserve(entry.target);
                        }
                    });
                });

                observer.observe(element);
            });
        }
    },

    // Initialisation de l'application
    init: function() {
        // Initialiser tous les modules
        this.lazyLoading.init();
        this.mobileNav.init();
        this.search.init();
        this.forms.init();
        this.visualEffects.init();
        this.animations.init();

        // Événements globaux
        this.bindGlobalEvents();

        console.log('La Caravela - Application initialisée avec effets visuels avancés');
    },

    bindGlobalEvents: function() {
        // Fermer les modales avec Escape
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                this.modal.closeAll();
            }
        });

        // Gestionnaire de clics pour les liens externes
        document.addEventListener('click', (event) => {
            const link = event.target.closest('a[href^="http"]');
            if (link && !link.hostname.includes(window.location.hostname)) {
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
            }
        });

        // Gestionnaire de scroll pour l'effet parallaxe
        window.addEventListener('scroll', Caravela.utils.throttle(() => {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('[data-parallax]');
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.parallax || 0.5;
                element.style.transform = `translateY(${scrolled * speed}px)`;
            });
        }, 16));
    }
};

// Initialiser l'application quand le DOM est prêt
document.addEventListener('DOMContentLoaded', function() {
    Caravela.init();
});

// Exporter pour utilisation globale
window.Caravela = Caravela; 