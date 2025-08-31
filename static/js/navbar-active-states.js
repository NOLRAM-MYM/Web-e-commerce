/* =================================================================
   ESTADOS ATIVOS PARA NAVBAR - MAGIC UI
   Arquivo: navbar-active-states.js
   Descrição: Funcionalidades JavaScript para gerenciar estados
   ativos dos elementos da barra de navegação
================================================================= */

(function() {
    'use strict';

    // Aguarda o carregamento completo do DOM
    document.addEventListener('DOMContentLoaded', function() {
        initializeNavbarActiveStates();
    });

    /**
     * Inicializa os estados ativos da navbar
     */
    function initializeNavbarActiveStates() {
        // Gerencia o estado ativo do dropdown toggle
        handleDropdownToggleStates();
        
        // Gerencia o estado ativo dos itens do dropdown
        handleDropdownItemStates();
        
        // Gerencia o estado ativo do span "Nenhuma categoria"
        handleEmptyCategoryState();
        
        // Adiciona indicadores visuais para página atual
        highlightCurrentPage();
    }

    /**
     * Gerencia os estados do dropdown toggle
     */
    function handleDropdownToggleStates() {
        const dropdownToggles = document.querySelectorAll('.navbar .nav-link.dropdown-toggle');
        
        dropdownToggles.forEach(toggle => {
            // Evento quando o dropdown é aberto
            toggle.addEventListener('show.bs.dropdown', function() {
                this.classList.add('show');
                addActiveEffect(this);
            });
            
            // Evento quando o dropdown é fechado
            toggle.addEventListener('hide.bs.dropdown', function() {
                this.classList.remove('show');
                removeActiveEffect(this);
            });
            
            // Clique direto no toggle (fora do Bootstrap)
            toggle.addEventListener('click', function(e) {
                if (!this.hasAttribute('data-bs-toggle')) {
                    e.preventDefault();
                    toggleActiveState(this);
                }
            });
        });
    }

    /**
     * Gerencia os estados dos itens do dropdown
     */
    function handleDropdownItemStates() {
        const dropdownItems = document.querySelectorAll('.navbar .dropdown-item');
        
        dropdownItems.forEach(item => {
            item.addEventListener('click', function(e) {
                // Remove estado ativo de outros itens
                clearActiveItems('.navbar .dropdown-item');
                
                // Adiciona estado ativo ao item clicado
                this.classList.add('active');
                this.setAttribute('aria-current', 'page');
                
                // Efeito visual de seleção
                addSelectionEffect(this);
                
                // Salva o estado no localStorage
                saveActiveState('activeDropdownItem', this.textContent.trim());
            });
            
            // Efeito hover aprimorado
            item.addEventListener('mouseenter', function() {
                if (!this.classList.contains('active')) {
                    this.style.transform = 'translateX(6px) scale(1.01)';
                }
            });
            
            item.addEventListener('mouseleave', function() {
                if (!this.classList.contains('active')) {
                    this.style.transform = '';
                }
            });
        });
    }

    /**
     * Gerencia o estado do span "Nenhuma categoria"
     */
    function handleEmptyCategoryState() {
        const emptyCategory = document.querySelector('.navbar .dropdown-item-text');
        
        if (emptyCategory) {
            emptyCategory.addEventListener('click', function() {
                // Toggle do estado ativo
                this.classList.toggle('active');
                
                if (this.classList.contains('active')) {
                    addSelectionEffect(this);
                    saveActiveState('emptyCategoryActive', 'true');
                } else {
                    removeActiveEffect(this);
                    saveActiveState('emptyCategoryActive', 'false');
                }
            });
            
            // Efeito de pulse quando ativo
            emptyCategory.addEventListener('mouseenter', function() {
                if (this.classList.contains('active')) {
                    this.style.animation = 'gentle-pulse 1s ease-in-out';
                }
            });
        }
    }

    /**
     * Destaca a página atual na navegação
     */
    function highlightCurrentPage() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar .nav-link:not(.dropdown-toggle)');
        
        navLinks.forEach(link => {
            const linkPath = new URL(link.href, window.location.origin).pathname;
            
            if (linkPath === currentPath) {
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            }
        });
        
        // Verifica itens do dropdown
        const dropdownItems = document.querySelectorAll('.navbar .dropdown-item');
        dropdownItems.forEach(item => {
            const itemPath = new URL(item.href, window.location.origin).pathname;
            
            if (itemPath === currentPath) {
                item.classList.add('active');
                item.setAttribute('aria-current', 'page');
                
                // Também marca o dropdown toggle como ativo
                const dropdownToggle = item.closest('.dropdown').querySelector('.dropdown-toggle');
                if (dropdownToggle) {
                    dropdownToggle.classList.add('active');
                }
            }
        });
    }

    /**
     * Adiciona efeito ativo a um elemento
     */
    function addActiveEffect(element) {
        element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        
        // Efeito de brilho
        setTimeout(() => {
            element.style.boxShadow = '0 0 20px rgba(99, 102, 241, 0.4)';
        }, 100);
    }

    /**
     * Remove efeito ativo de um elemento
     */
    function removeActiveEffect(element) {
        element.style.boxShadow = '';
        element.style.transform = '';
    }

    /**
     * Adiciona efeito de seleção
     */
    function addSelectionEffect(element) {
        // Efeito de ripple
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-effect 0.6s linear;
            pointer-events: none;
            left: 50%;
            top: 50%;
            width: 20px;
            height: 20px;
            margin-left: -10px;
            margin-top: -10px;
        `;
        
        element.style.position = 'relative';
        element.appendChild(ripple);
        
        // Remove o ripple após a animação
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }

    /**
     * Toggle do estado ativo
     */
    function toggleActiveState(element) {
        element.classList.toggle('active');
        
        if (element.classList.contains('active')) {
            addActiveEffect(element);
        } else {
            removeActiveEffect(element);
        }
    }

    /**
     * Remove estado ativo de todos os itens de um seletor
     */
    function clearActiveItems(selector) {
        const items = document.querySelectorAll(selector);
        items.forEach(item => {
            item.classList.remove('active');
            item.removeAttribute('aria-current');
        });
    }

    /**
     * Salva estado no localStorage
     */
    function saveActiveState(key, value) {
        try {
            localStorage.setItem(key, value);
        } catch (e) {
            console.warn('Não foi possível salvar o estado no localStorage:', e);
        }
    }

    /**
     * Recupera estado do localStorage
     */
    function getActiveState(key) {
        try {
            return localStorage.getItem(key);
        } catch (e) {
            console.warn('Não foi possível recuperar o estado do localStorage:', e);
            return null;
        }
    }

    /**
     * Restaura estados salvos
     */
    function restoreSavedStates() {
        // Restaura item ativo do dropdown
        const activeItem = getActiveState('activeDropdownItem');
        if (activeItem) {
            const items = document.querySelectorAll('.navbar .dropdown-item');
            items.forEach(item => {
                if (item.textContent.trim() === activeItem) {
                    item.classList.add('active');
                    item.setAttribute('aria-current', 'page');
                }
            });
        }
        
        // Restaura estado da categoria vazia
        const emptyCategoryActive = getActiveState('emptyCategoryActive');
        if (emptyCategoryActive === 'true') {
            const emptyCategory = document.querySelector('.navbar .dropdown-item-text');
            if (emptyCategory) {
                emptyCategory.classList.add('active');
            }
        }
    }

    // Adiciona CSS para animação de ripple
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple-effect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Restaura estados salvos quando a página carrega
    document.addEventListener('DOMContentLoaded', restoreSavedStates);

})();