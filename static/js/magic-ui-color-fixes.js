/**
 * Magic UI Color Fixes - Correção automática de cores brancas problemáticas
 * Este script corrige automaticamente elementos com cores brancas que podem ser invisíveis
 */

(function() {
    'use strict';

    // Variáveis CSS do Magic UI
    const MAGIC_COLORS = {
        primary: '#6366f1',
        secondary: '#8b5cf6',
        accent: '#06b6d4',
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        dark: '#0f172a',
        light: '#f8fafc',
        textPrimary: '#ffffff',
        textSecondary: '#cbd5e1',
        cardBg: 'rgba(255, 255, 255, 0.1)',
        border: 'rgba(255, 255, 255, 0.2)',
        gradientPrimary: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
        gradientAccent: 'linear-gradient(135deg, #06b6d4, #6366f1)'
    };

    /**
     * Corrige elementos com cor branca problemática
     */
    function fixWhiteTextElements() {
        // Selecionar todos os elementos com color: white inline
        const whiteTextElements = document.querySelectorAll('[style*="color: white"], [style*="color:white"]');
        
        whiteTextElements.forEach(element => {
            const computedStyle = window.getComputedStyle(element);
            const backgroundColor = computedStyle.backgroundColor;
            
            // Se o fundo for claro ou transparente, mudar a cor do texto
            if (isLightBackground(backgroundColor) || backgroundColor === 'rgba(0, 0, 0, 0)' || backgroundColor === 'transparent') {
                element.style.color = MAGIC_COLORS.dark + ' !important';
            } else {
                element.style.color = MAGIC_COLORS.textPrimary + ' !important';
            }
        });
    }

    /**
     * Corrige elementos com fundo branco problemático
     */
    function fixWhiteBackgroundElements() {
        // Selecionar todos os elementos com background: white inline
        const whiteBgElements = document.querySelectorAll('[style*="background: white"], [style*="background-color: white"], [style*="background:white"], [style*="background-color:white"]');
        
        whiteBgElements.forEach(element => {
            // Aplicar fundo Magic UI com backdrop blur
            element.style.background = MAGIC_COLORS.cardBg + ' !important';
            element.style.backdropFilter = 'blur(20px)';
            element.style.border = '1px solid ' + MAGIC_COLORS.border;
            element.style.borderRadius = '12px';
            
            // Se o elemento contém texto, garantir que seja visível
            if (element.textContent.trim()) {
                element.style.color = MAGIC_COLORS.textPrimary + ' !important';
            }
        });
    }

    /**
     * Corrige botões com cores problemáticas
     */
    function fixButtonColors() {
        // Selecionar botões com cores brancas ou problemáticas
        const buttons = document.querySelectorAll('button, .btn, input[type="submit"], input[type="button"]');
        
        buttons.forEach(button => {
            const computedStyle = window.getComputedStyle(button);
            const backgroundColor = computedStyle.backgroundColor;
            const color = computedStyle.color;
            
            // Se o botão tem fundo branco ou muito claro
            if (isWhiteOrLight(backgroundColor)) {
                // Aplicar estilo Magic UI baseado na classe do botão
                if (button.classList.contains('btn-primary') || button.classList.contains('btn-login')) {
                    button.style.background = MAGIC_COLORS.gradientPrimary + ' !important';
                    button.style.color = MAGIC_COLORS.textPrimary + ' !important';
                } else if (button.classList.contains('btn-success')) {
                    button.style.background = 'linear-gradient(135deg, ' + MAGIC_COLORS.success + ', #059669) !important';
                    button.style.color = MAGIC_COLORS.textPrimary + ' !important';
                } else if (button.classList.contains('btn-danger')) {
                    button.style.background = 'linear-gradient(135deg, ' + MAGIC_COLORS.danger + ', #dc2626) !important';
                    button.style.color = MAGIC_COLORS.textPrimary + ' !important';
                } else if (button.classList.contains('btn-warning')) {
                    button.style.background = 'linear-gradient(135deg, ' + MAGIC_COLORS.warning + ', #d97706) !important';
                    button.style.color = MAGIC_COLORS.textPrimary + ' !important';
                } else if (button.classList.contains('btn-info')) {
                    button.style.background = MAGIC_COLORS.gradientAccent + ' !important';
                    button.style.color = MAGIC_COLORS.textPrimary + ' !important';
                } else if (button.classList.contains('btn-light')) {
                    button.style.background = 'rgba(248, 250, 252, 0.9) !important';
                    button.style.color = MAGIC_COLORS.dark + ' !important';
                } else {
                    // Botão padrão
                    button.style.background = MAGIC_COLORS.cardBg + ' !important';
                    button.style.color = MAGIC_COLORS.textPrimary + ' !important';
                    button.style.border = '1px solid ' + MAGIC_COLORS.border + ' !important';
                }
                
                // Aplicar efeitos Magic UI
                button.style.borderRadius = '12px';
                button.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                button.style.boxShadow = '0 4px 15px rgba(99, 102, 241, 0.4)';
                
                // Adicionar efeito hover
                button.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 8px 25px rgba(99, 102, 241, 0.6)';
                });
                
                button.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 4px 15px rgba(99, 102, 241, 0.4)';
                });
            }
        });
    }

    /**
     * Corrige elementos de formulário
     */
    function fixFormElements() {
        // Selecionar inputs, selects e textareas
        const formElements = document.querySelectorAll('input, select, textarea, .form-control');
        
        formElements.forEach(element => {
            const computedStyle = window.getComputedStyle(element);
            const backgroundColor = computedStyle.backgroundColor;
            
            // Se o fundo for branco ou muito claro
            if (isWhiteOrLight(backgroundColor)) {
                element.style.background = 'rgba(255, 255, 255, 0.05) !important';
                element.style.border = '1px solid ' + MAGIC_COLORS.border + ' !important';
                element.style.borderRadius = '12px';
                element.style.color = MAGIC_COLORS.textPrimary + ' !important';
                element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                
                // Efeito focus
                element.addEventListener('focus', function() {
                    this.style.borderColor = MAGIC_COLORS.primary;
                    this.style.boxShadow = '0 0 0 3px rgba(99, 102, 241, 0.1)';
                    this.style.background = 'rgba(255, 255, 255, 0.08) !important';
                });
                
                element.addEventListener('blur', function() {
                    this.style.borderColor = MAGIC_COLORS.border;
                    this.style.boxShadow = 'none';
                    this.style.background = 'rgba(255, 255, 255, 0.05) !important';
                });
            }
        });
    }

    /**
     * Corrige cards e containers
     */
    function fixCardElements() {
        // Selecionar cards e containers com fundo branco
        const cardElements = document.querySelectorAll('.card, .container, .modal-content, [style*="background: white"], [style*="background-color: white"]');
        
        cardElements.forEach(element => {
            const computedStyle = window.getComputedStyle(element);
            const backgroundColor = computedStyle.backgroundColor;
            
            if (isWhiteOrLight(backgroundColor)) {
                element.style.background = MAGIC_COLORS.cardBg + ' !important';
                element.style.backdropFilter = 'blur(20px)';
                element.style.border = '1px solid ' + MAGIC_COLORS.border + ' !important';
                element.style.borderRadius = '20px';
                element.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1)';
                element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            }
        });
    }

    /**
     * Verifica se uma cor é branca ou muito clara
     */
    function isWhiteOrLight(color) {
        if (!color || color === 'transparent' || color === 'rgba(0, 0, 0, 0)') {
            return false;
        }
        
        // Converter para RGB se necessário
        const rgb = getRGBValues(color);
        if (!rgb) return false;
        
        // Calcular luminância
        const luminance = (0.299 * rgb.r + 0.587 * rgb.g + 0.114 * rgb.b) / 255;
        
        // Considerar claro se luminância > 0.8
        return luminance > 0.8;
    }

    /**
     * Verifica se o fundo é claro
     */
    function isLightBackground(color) {
        return isWhiteOrLight(color);
    }

    /**
     * Extrai valores RGB de uma string de cor
     */
    function getRGBValues(color) {
        if (color.startsWith('rgb')) {
            const matches = color.match(/\d+/g);
            if (matches && matches.length >= 3) {
                return {
                    r: parseInt(matches[0]),
                    g: parseInt(matches[1]),
                    b: parseInt(matches[2])
                };
            }
        } else if (color === 'white') {
            return { r: 255, g: 255, b: 255 };
        } else if (color.startsWith('#')) {
            const hex = color.substring(1);
            if (hex.length === 6) {
                return {
                    r: parseInt(hex.substring(0, 2), 16),
                    g: parseInt(hex.substring(2, 4), 16),
                    b: parseInt(hex.substring(4, 6), 16)
                };
            }
        }
        return null;
    }

    /**
     * Aplica correções de acessibilidade
     */
    function applyAccessibilityFixes() {
        // Garantir contraste adequado
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(element => {
            const computedStyle = window.getComputedStyle(element);
            const color = computedStyle.color;
            const backgroundColor = computedStyle.backgroundColor;
            
            // Se texto branco em fundo claro
            if (color === 'rgb(255, 255, 255)' && isLightBackground(backgroundColor)) {
                element.style.color = MAGIC_COLORS.dark + ' !important';
            }
        });
    }

    /**
     * Inicializa todas as correções
     */
    function initColorFixes() {
        try {
            fixWhiteTextElements();
            fixWhiteBackgroundElements();
            fixButtonColors();
            fixFormElements();
            fixCardElements();
            applyAccessibilityFixes();
            
            console.log('Magic UI Color Fixes aplicadas com sucesso!');
        } catch (error) {
            console.error('Erro ao aplicar Magic UI Color Fixes:', error);
        }
    }

    /**
     * Observer para elementos adicionados dinamicamente
     */
    function setupMutationObserver() {
        const observer = new MutationObserver(function(mutations) {
            let shouldReapplyFixes = false;
            
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    shouldReapplyFixes = true;
                }
            });
            
            if (shouldReapplyFixes) {
                setTimeout(initColorFixes, 100);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    // Executar quando o DOM estiver carregado
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initColorFixes();
            setupMutationObserver();
        });
    } else {
        initColorFixes();
        setupMutationObserver();
    }

    // Executar novamente após o carregamento completo
    window.addEventListener('load', function() {
        setTimeout(initColorFixes, 500);
    });

    // Expor função global para correções manuais
    window.MagicUIColorFixes = {
        init: initColorFixes,
        fixButtons: fixButtonColors,
        fixForms: fixFormElements,
        fixCards: fixCardElements
    };

})();