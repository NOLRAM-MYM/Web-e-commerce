/**
 * Magic UI Components adaptados para Django
 * Componentes de interface modernos e animados
 */

// Shimmer Button Component
class ShimmerButton {
    constructor(element) {
        this.element = element;
        this.init();
    }

    init() {
        this.element.classList.add('shimmer-button');
        this.element.style.position = 'relative';
        this.element.style.overflow = 'hidden';
        
        // Adicionar efeito shimmer
        const shimmer = document.createElement('div');
        shimmer.className = 'shimmer-effect';
        this.element.appendChild(shimmer);
        
        this.addStyles();
    }

    addStyles() {
        if (!document.getElementById('shimmer-styles')) {
            const style = document.createElement('style');
            style.id = 'shimmer-styles';
            style.textContent = `
                .shimmer-button {
                    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    cursor: pointer;
                    font-weight: 600;
                    padding: 12px 24px;
                    transition: all 0.3s ease;
                    transform: translateZ(0);
                }
                
                .shimmer-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
                }
                
                .shimmer-effect {
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                    animation: shimmer 2s infinite;
                }
                
                @keyframes shimmer {
                    0% { left: -100%; }
                    100% { left: 100%; }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Magic Card Component
class MagicCard {
    constructor(element) {
        this.element = element;
        this.init();
    }

    init() {
        this.element.classList.add('magic-card');
        this.addMouseEffect();
        this.addStyles();
    }

    addMouseEffect() {
        this.element.addEventListener('mousemove', (e) => {
            const rect = this.element.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.element.style.setProperty('--mouse-x', `${x}px`);
            this.element.style.setProperty('--mouse-y', `${y}px`);
        });
    }

    addStyles() {
        if (!document.getElementById('magic-card-styles')) {
            const style = document.createElement('style');
            style.id = 'magic-card-styles';
            style.textContent = `
                .magic-card {
                    position: relative;
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 16px;
                    padding: 24px;
                    transition: all 0.3s ease;
                    overflow: hidden;
                }
                
                .magic-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: radial-gradient(circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(255,255,255,0.1) 0%, transparent 50%);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                    pointer-events: none;
                }
                
                .magic-card:hover::before {
                    opacity: 1;
                }
                
                .magic-card:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Animated Grid Pattern Background
class AnimatedGridPattern {
    constructor(element) {
        this.element = element;
        this.init();
    }

    init() {
        this.element.classList.add('animated-grid');
        this.createGrid();
        this.addStyles();
    }

    createGrid() {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('class', 'grid-pattern');
        svg.innerHTML = `
            <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(156, 163, 175, 0.2)" stroke-width="1"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
        `;
        this.element.appendChild(svg);
    }

    addStyles() {
        if (!document.getElementById('grid-pattern-styles')) {
            const style = document.createElement('style');
            style.id = 'grid-pattern-styles';
            style.textContent = `
                .animated-grid {
                    position: relative;
                    overflow: hidden;
                }
                
                .grid-pattern {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    opacity: 0.5;
                    animation: gridMove 20s linear infinite;
                }
                
                @keyframes gridMove {
                    0% { transform: translate(0, 0); }
                    100% { transform: translate(40px, 40px); }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Number Ticker Component
class NumberTicker {
    constructor(element, options = {}) {
        this.element = element;
        this.target = parseInt(element.dataset.target) || 0;
        this.duration = options.duration || 2000;
        this.init();
    }

    init() {
        this.element.classList.add('number-ticker');
        this.animate();
        this.addStyles();
    }

    animate() {
        const start = 0;
        const startTime = performance.now();
        
        const updateNumber = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / this.duration, 1);
            
            // Easing function
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (this.target - start) * easeOut);
            
            this.element.textContent = current.toLocaleString('pt-BR');
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        };
        
        requestAnimationFrame(updateNumber);
    }

    addStyles() {
        if (!document.getElementById('number-ticker-styles')) {
            const style = document.createElement('style');
            style.id = 'number-ticker-styles';
            style.textContent = `
                .number-ticker {
                    font-weight: 700;
                    font-size: 2rem;
                    color: #1f2937;
                    transition: all 0.3s ease;
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Ripple Effect Component
class RippleEffect {
    constructor(element) {
        this.element = element;
        this.init();
    }

    init() {
        this.element.classList.add('ripple-container');
        this.element.addEventListener('click', this.createRipple.bind(this));
        this.addStyles();
    }

    createRipple(event) {
        const rect = this.element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        const ripple = document.createElement('div');
        ripple.className = 'ripple';
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        this.element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    addStyles() {
        if (!document.getElementById('ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                .ripple-container {
                    position: relative;
                    overflow: hidden;
                }
                
                .ripple {
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.6);
                    transform: scale(0);
                    animation: ripple-animation 0.6s linear;
                    pointer-events: none;
                }
                
                @keyframes ripple-animation {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }
}

// Inicialização automática dos componentes
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar Shimmer Buttons
    document.querySelectorAll('.btn-shimmer').forEach(btn => {
        new ShimmerButton(btn);
    });
    
    // Inicializar Magic Cards
    document.querySelectorAll('.card-magic').forEach(card => {
        new MagicCard(card);
    });
    
    // Inicializar Grid Patterns
    document.querySelectorAll('.bg-grid').forEach(grid => {
        new AnimatedGridPattern(grid);
    });
    
    // Inicializar Number Tickers
    document.querySelectorAll('.number-ticker').forEach(ticker => {
        new NumberTicker(ticker);
    });
    
    // Inicializar Ripple Effects
    document.querySelectorAll('.btn-ripple').forEach(btn => {
        new RippleEffect(btn);
    });
});

// Exportar classes para uso global
window.MagicUI = {
    ShimmerButton,
    MagicCard,
    AnimatedGridPattern,
    NumberTicker,
    RippleEffect
};