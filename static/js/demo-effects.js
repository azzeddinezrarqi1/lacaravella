/**
 * Script de démonstration des effets dynamiques
 * Pour tester et présenter les nouvelles fonctionnalités
 */

window.DemoEffects = {
    // Initialisation
    init: function() {
        this.createColorPalette();
        this.createAnimationShowcase();
        this.createInteractiveElements();
        this.bindEvents();
    },

    // Créer une palette de couleurs interactive
    createColorPalette: function() {
        const colors = [
            { name: 'Caravela', value: '#f2751a', class: 'caravela-500' },
            { name: 'Mint', value: '#14b8a6', class: 'mint-500' },
            { name: 'Lavender', value: '#a855f7', class: 'lavender-500' },
            { name: 'Coral', value: '#e53e3e', class: 'coral-500' },
            { name: 'Sunshine', value: '#f59e0b', class: 'sunshine-500' }
        ];

        const palette = document.createElement('div');
        palette.className = 'fixed bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 z-50';
        palette.innerHTML = '<h3 class="font-bold mb-2">Palette de Couleurs</h3>';

        colors.forEach(color => {
            const colorDiv = document.createElement('div');
            colorDiv.className = 'flex items-center mb-2 cursor-pointer hover-lift';
            colorDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full mr-3 bg-${color.class}"></div>
                <span class="text-sm">${color.name}</span>
            `;
            
            colorDiv.addEventListener('click', () => {
                this.changeThemeColor(color.value);
            });
            
            palette.appendChild(colorDiv);
        });

        document.body.appendChild(palette);
    },

    // Changer la couleur du thème
    changeThemeColor: function(color) {
        document.documentElement.style.setProperty('--accent-primary', color);
        
        // Animation de transition
        document.body.style.transition = 'all 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    },

    // Créer un showcase d'animations
    createAnimationShowcase: function() {
        const showcase = document.createElement('div');
        showcase.className = 'fixed top-4 right-4 bg-white rounded-lg shadow-lg p-4 z-50';
        showcase.innerHTML = `
            <h3 class="font-bold mb-2">Animations</h3>
            <div class="space-y-2">
                <button class="btn-primary btn-sm" onclick="DemoEffects.triggerAnimation('bounce')">Bounce</button>
                <button class="btn-mint btn-sm" onclick="DemoEffects.triggerAnimation('pulse')">Pulse</button>
                <button class="btn-lavender btn-sm" onclick="DemoEffects.triggerAnimation('wiggle')">Wiggle</button>
                <button class="btn-coral btn-sm" onclick="DemoEffects.triggerAnimation('rainbow')">Rainbow</button>
            </div>
        `;

        document.body.appendChild(showcase);
    },

    // Déclencher une animation
    triggerAnimation: function(type) {
        const elements = document.querySelectorAll('.product-card, .floating-card, .stats-card');
        
        elements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.remove('animate-bounce-in', 'animate-pulse', 'animate-wiggle', 'animate-rainbow');
                
                switch(type) {
                    case 'bounce':
                        element.classList.add('animate-bounce-in');
                        break;
                    case 'pulse':
                        element.classList.add('animate-pulse');
                        break;
                    case 'wiggle':
                        element.classList.add('animate-wiggle');
                        break;
                    case 'rainbow':
                        element.classList.add('animate-rainbow');
                        break;
                }
                
                // Retirer la classe après l'animation
                setTimeout(() => {
                    element.classList.remove('animate-bounce-in', 'animate-pulse', 'animate-wiggle', 'animate-rainbow');
                }, 2000);
            }, index * 100);
        });
    },

    // Créer des éléments interactifs
    createInteractiveElements: function() {
        // Ajouter des particules dynamiques
        this.createDynamicParticles();
        
        // Créer un curseur personnalisé
        this.createCustomCursor();
    },

    // Créer des particules dynamiques
    createDynamicParticles: function() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'fixed inset-0 pointer-events-none z-10';
        particleContainer.id = 'dynamic-particles';

        document.body.appendChild(particleContainer);

        // Générer des particules aléatoires
        setInterval(() => {
            this.createParticle();
        }, 200);
    },

    // Créer une particule individuelle
    createParticle: function() {
        const container = document.getElementById('dynamic-particles');
        if (!container) return;

        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Position aléatoire
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDuration = (Math.random() * 3 + 2) + 's';
        
        // Couleur aléatoire
        const colors = ['var(--caravela-500)', 'var(--mint-500)', 'var(--lavender-500)', 'var(--coral-500)', 'var(--sunshine-500)'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];

        container.appendChild(particle);

        // Supprimer la particule après l'animation
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, 5000);
    },

    // Créer un curseur personnalisé
    createCustomCursor: function() {
        const cursor = document.createElement('div');
        cursor.className = 'fixed w-4 h-4 bg-caravela-500 rounded-full pointer-events-none z-50 mix-blend-difference';
        cursor.id = 'custom-cursor';

        document.body.appendChild(cursor);

        // Suivre la souris
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX - 8 + 'px';
            cursor.style.top = e.clientY - 8 + 'px';
        });

        // Effet au survol des éléments interactifs
        document.addEventListener('mouseover', (e) => {
            if (e.target.matches('button, a, .hover-lift, .hover-glow')) {
                cursor.style.transform = 'scale(2)';
                cursor.style.background = 'var(--mint-500)';
            }
        });

        document.addEventListener('mouseout', (e) => {
            if (e.target.matches('button, a, .hover-lift, .hover-glow')) {
                cursor.style.transform = 'scale(1)';
                cursor.style.background = 'var(--caravela-500)';
            }
        });
    },

    // Lier les événements
    bindEvents: function() {
        // Raccourcis clavier
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case '1':
                        e.preventDefault();
                        this.changeThemeColor('#f2751a'); // Caravela
                        break;
                    case '2':
                        e.preventDefault();
                        this.changeThemeColor('#14b8a6'); // Mint
                        break;
                    case '3':
                        e.preventDefault();
                        this.changeThemeColor('#a855f7'); // Lavender
                        break;
                    case '4':
                        e.preventDefault();
                        this.changeThemeColor('#e53e3e'); // Coral
                        break;
                    case '5':
                        e.preventDefault();
                        this.changeThemeColor('#f59e0b'); // Sunshine
                        break;
                }
            }
        });

        // Effet de confettis au clic
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-rainbow, .btn-magic')) {
                this.createConfetti(e.clientX, e.clientY);
            }
        });
    },

    // Créer des confettis
    createConfetti: function(x, y) {
        const colors = ['#f2751a', '#14b8a6', '#a855f7', '#e53e3e', '#f59e0b'];
        
        for (let i = 0; i < 20; i++) {
            const confetti = document.createElement('div');
            confetti.style.position = 'fixed';
            confetti.style.left = x + 'px';
            confetti.style.top = y + 'px';
            confetti.style.width = '6px';
            confetti.style.height = '6px';
            confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.borderRadius = '50%';
            confetti.style.pointerEvents = 'none';
            confetti.style.zIndex = '9999';

            document.body.appendChild(confetti);

            // Animation de chute
            const angle = Math.random() * 360;
            const velocity = Math.random() * 10 + 5;
            const gravity = 0.5;
            let vx = Math.cos(angle * Math.PI / 180) * velocity;
            let vy = Math.sin(angle * Math.PI / 180) * velocity;
            let currentY = y;

            const animate = () => {
                vx *= 0.99; // Friction
                vy += gravity; // Gravité
                
                x += vx;
                currentY += vy;
                
                confetti.style.left = x + 'px';
                confetti.style.top = currentY + 'px';
                confetti.style.opacity = Math.max(0, 1 - (currentY - y) / 300);

                if (currentY < window.innerHeight + 100) {
                    requestAnimationFrame(animate);
                } else {
                    confetti.remove();
                }
            };

            requestAnimationFrame(animate);
        }
    },

    // Mode démonstration
    enableDemoMode: function() {
        // Ajouter un indicateur de mode démo
        const indicator = document.createElement('div');
        indicator.className = 'fixed top-0 left-0 right-0 bg-gradient-to-r from-caravela-500 to-mint-500 text-white text-center py-2 z-50';
        indicator.innerHTML = '🎨 Mode Démonstration Actif - Utilisez Ctrl+1-5 pour changer les couleurs';
        
        document.body.appendChild(indicator);

        // Démarrer les effets
        this.init();
    }
};

// Auto-initialisation si on est sur la page de démo
if (window.location.pathname.includes('demo') || document.querySelector('.demo-mode')) {
    document.addEventListener('DOMContentLoaded', () => {
        DemoEffects.enableDemoMode();
    });
}
