// Main JavaScript for E-Commerce

// CSRF Token Setup
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// AJAX Setup
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain && !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Cart Functions
class Cart {
    constructor() {
        this.updateCartCount();
        this.bindEvents();
    }

    bindEvents() {
        // Add to cart buttons
        $(document).on('click', '.add-to-cart-btn', (e) => {
            e.preventDefault();
            const btn = $(e.currentTarget);
            const productId = btn.data('product-id');
            const quantity = btn.closest('.product-card').find('.quantity-input').val() || 1;
            this.addToCart(productId, quantity, btn);
        });

        // Remove from cart buttons
        $(document).on('click', '.remove-from-cart-btn', (e) => {
            e.preventDefault();
            const btn = $(e.currentTarget);
            const itemId = btn.data('item-id');
            this.removeFromCart(itemId, btn);
        });

        // Update cart item quantity
        $(document).on('change', '.cart-quantity-input', (e) => {
            const input = $(e.currentTarget);
            const itemId = input.data('item-id');
            const quantity = input.val();
            this.updateCartItem(itemId, quantity);
        });

        // Clear cart button
        $(document).on('click', '.clear-cart-btn', (e) => {
            e.preventDefault();
            if (confirm('Tem certeza que deseja limpar o carrinho?')) {
                this.clearCart();
            }
        });
    }

    addToCart(productId, quantity, btn) {
        const originalText = btn.html();
        btn.html('<span class="spinner"></span> Adicionando...').prop('disabled', true);

        $.ajax({
            url: '/carrinho/adicionar/',
            method: 'POST',
            data: {
                'product_id': productId,
                'quantity': quantity
            },
            success: (response) => {
                if (response.success) {
                    this.showMessage('Produto adicionado ao carrinho!', 'success');
                    this.updateCartCount();
                    
                    // Update button temporarily
                    btn.html('<i class="fas fa-check"></i> Adicionado!');
                    setTimeout(() => {
                        btn.html(originalText).prop('disabled', false);
                    }, 2000);
                } else {
                    this.showMessage(response.message || 'Erro ao adicionar produto', 'error');
                    btn.html(originalText).prop('disabled', false);
                }
            },
            error: (xhr) => {
                let message = 'Erro ao adicionar produto ao carrinho';
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    message = xhr.responseJSON.message;
                }
                this.showMessage(message, 'error');
                btn.html(originalText).prop('disabled', false);
            }
        });
    }

    removeFromCart(itemId, btn) {
        const originalText = btn.html();
        btn.html('<span class="spinner"></span>').prop('disabled', true);

        $.ajax({
            url: '/carrinho/remover/',
            method: 'POST',
            data: {
                'item_id': itemId
            },
            success: (response) => {
                if (response.success) {
                    this.showMessage('Item removido do carrinho', 'success');
                    this.updateCartCount();
                    
                    // Remove the cart item from DOM
                    btn.closest('.cart-item').fadeOut(300, function() {
                        $(this).remove();
                        // Update cart total
                        cart.updateCartTotal();
                    });
                } else {
                    this.showMessage(response.message || 'Erro ao remover item', 'error');
                    btn.html(originalText).prop('disabled', false);
                }
            },
            error: (xhr) => {
                this.showMessage('Erro ao remover item do carrinho', 'error');
                btn.html(originalText).prop('disabled', false);
            }
        });
    }

    updateCartItem(itemId, quantity) {
        if (quantity < 1) {
            quantity = 1;
        }

        $.ajax({
            url: '/carrinho/atualizar/',
            method: 'POST',
            data: {
                'item_id': itemId,
                'quantity': quantity
            },
            success: (response) => {
                if (response.success) {
                    this.updateCartCount();
                    this.updateCartTotal();
                    
                    // Update item total in DOM
                    const itemRow = $(`.cart-quantity-input[data-item-id="${itemId}"]`).closest('.cart-item');
                    itemRow.find('.item-total').text(response.item_total);
                } else {
                    this.showMessage(response.message || 'Erro ao atualizar quantidade', 'error');
                }
            },
            error: (xhr) => {
                this.showMessage('Erro ao atualizar quantidade', 'error');
            }
        });
    }

    clearCart() {
        $.ajax({
            url: '/carrinho/limpar/',
            method: 'POST',
            success: (response) => {
                if (response.success) {
                    this.showMessage('Carrinho limpo com sucesso', 'success');
                    this.updateCartCount();
                    
                    // Reload page or update DOM
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    this.showMessage(response.message || 'Erro ao limpar carrinho', 'error');
                }
            },
            error: (xhr) => {
                this.showMessage('Erro ao limpar carrinho', 'error');
            }
        });
    }

    updateCartCount() {
        $.ajax({
            url: '/carrinho/count/',
            method: 'GET',
            success: (response) => {
                $('.cart-count').text(response.count);
                if (response.count > 0) {
                    $('.cart-count').show();
                } else {
                    $('.cart-count').hide();
                }
            }
        });
    }

    updateCartTotal() {
        $.ajax({
            url: '/carrinho/total/',
            method: 'GET',
            success: (response) => {
                $('.cart-total').text(response.total);
                $('.cart-subtotal').text(response.subtotal);
            }
        });
    }

    showMessage(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Remove existing alerts
        $('.alert').remove();
        
        // Add new alert
        $('main').prepend(alertHtml);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            $('.alert').fadeOut();
        }, 5000);
    }
}

// Search Functions
class Search {
    constructor() {
        this.bindEvents();
    }

    bindEvents() {
        // Search suggestions
        $('#search-input').on('input', debounce((e) => {
            const query = $(e.target).val();
            if (query.length >= 2) {
                this.getSuggestions(query);
            } else {
                this.hideSuggestions();
            }
        }, 300));

        // Hide suggestions when clicking outside
        $(document).on('click', (e) => {
            if (!$(e.target).closest('.search-container').length) {
                this.hideSuggestions();
            }
        });

        // Select suggestion
        $(document).on('click', '.search-suggestion', (e) => {
            e.preventDefault();
            const suggestion = $(e.currentTarget).text();
            $('#search-input').val(suggestion);
            this.hideSuggestions();
            $('#search-form').submit();
        });
    }

    getSuggestions(query) {
        $.ajax({
            url: '/buscar/sugestoes/',
            method: 'GET',
            data: { 'q': query },
            success: (response) => {
                this.showSuggestions(response.suggestions);
            }
        });
    }

    showSuggestions(suggestions) {
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }

        let html = '<div class="search-suggestions">';
        suggestions.forEach(suggestion => {
            html += `<div class="search-suggestion">${suggestion}</div>`;
        });
        html += '</div>';

        $('.search-container').append(html);
    }

    hideSuggestions() {
        $('.search-suggestions').remove();
    }
}

// Form Validation
class FormValidator {
    constructor() {
        this.bindEvents();
    }

    bindEvents() {
        // Username availability check
        $('#id_username').on('blur', (e) => {
            const username = $(e.target).val();
            if (username.length >= 3) {
                this.checkUsernameAvailability(username);
            }
        });

        // Email availability check
        $('#id_email').on('blur', (e) => {
            const email = $(e.target).val();
            if (email.includes('@')) {
                this.checkEmailAvailability(email);
            }
        });

        // Password strength indicator
        $('#id_password1, #id_password').on('input', (e) => {
            const password = $(e.target).val();
            this.showPasswordStrength(password, e.target);
        });

        // Password confirmation
        $('#id_password2').on('input', (e) => {
            const password1 = $('#id_password1').val();
            const password2 = $(e.target).val();
            this.checkPasswordMatch(password1, password2);
        });
    }

    checkUsernameAvailability(username) {
        $.ajax({
            url: '/usuarios/check-username/',
            method: 'GET',
            data: { 'username': username },
            success: (response) => {
                const feedback = $('#id_username').siblings('.form-feedback');
                if (response.available) {
                    feedback.removeClass('text-danger').addClass('text-success')
                           .text('Nome de usuário disponível');
                } else {
                    feedback.removeClass('text-success').addClass('text-danger')
                           .text('Nome de usuário já está em uso');
                }
            }
        });
    }

    checkEmailAvailability(email) {
        $.ajax({
            url: '/usuarios/check-email/',
            method: 'GET',
            data: { 'email': email },
            success: (response) => {
                const feedback = $('#id_email').siblings('.form-feedback');
                if (response.available) {
                    feedback.removeClass('text-danger').addClass('text-success')
                           .text('E-mail disponível');
                } else {
                    feedback.removeClass('text-success').addClass('text-danger')
                           .text('E-mail já está cadastrado');
                }
            }
        });
    }

    showPasswordStrength(password, element) {
        const strength = this.calculatePasswordStrength(password);
        const feedback = $(element).siblings('.password-strength');
        
        if (feedback.length === 0) {
            $(element).after('<div class="password-strength mt-1"></div>');
        }
        
        const strengthFeedback = $(element).siblings('.password-strength');
        const strengthText = ['Muito fraca', 'Fraca', 'Média', 'Forte', 'Muito forte'];
        const strengthClass = ['text-danger', 'text-warning', 'text-info', 'text-success', 'text-success'];
        
        strengthFeedback.removeClass('text-danger text-warning text-info text-success')
                       .addClass(strengthClass[strength])
                       .text(`Força da senha: ${strengthText[strength]}`);
    }

    calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        return Math.min(strength, 4);
    }

    checkPasswordMatch(password1, password2) {
        const feedback = $('#id_password2').siblings('.form-feedback');
        if (password2.length > 0) {
            if (password1 === password2) {
                feedback.removeClass('text-danger').addClass('text-success')
                       .text('Senhas coincidem');
            } else {
                feedback.removeClass('text-success').addClass('text-danger')
                       .text('Senhas não coincidem');
            }
        } else {
            feedback.text('');
        }
    }
}

// Image Upload Preview
class ImageUpload {
    constructor() {
        this.bindEvents();
    }

    bindEvents() {
        $(document).on('change', 'input[type="file"][accept*="image"]', (e) => {
            this.previewImage(e.target);
        });

        $(document).on('click', '.image-remove-btn', (e) => {
            e.preventDefault();
            this.removeImagePreview(e.target);
        });
    }

    previewImage(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = $(input).siblings('.image-upload-preview');
                if (preview.length === 0) {
                    $(input).after(`
                        <div class="image-upload-container mt-2">
                            <img src="${e.target.result}" class="image-upload-preview" alt="Preview">
                            <button type="button" class="image-remove-btn">&times;</button>
                        </div>
                    `);
                } else {
                    preview.attr('src', e.target.result);
                }
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    removeImagePreview(button) {
        const container = $(button).closest('.image-upload-container');
        const input = container.siblings('input[type="file"]');
        input.val('');
        container.remove();
    }
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function formatCurrency(amount, currency = 'BRL') {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

function showLoading(element) {
    $(element).addClass('loading');
}

function hideLoading(element) {
    $(element).removeClass('loading');
}

// Initialize when document is ready
$(document).ready(() => {
    // Initialize classes
    window.cart = new Cart();
    window.search = new Search();
    window.formValidator = new FormValidator();
    window.imageUpload = new ImageUpload();

    // Initialize tooltips
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    // Initialize popovers
    if (typeof bootstrap !== 'undefined') {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    }

    // Smooth scrolling for anchor links
    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            let target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 100
                }, 1000);
                return false;
            }
        }
    });

    // Back to top button
    $(window).scroll(() => {
        if ($(window).scrollTop() > 300) {
            $('.back-to-top').fadeIn();
        } else {
            $('.back-to-top').fadeOut();
        }
    });

    $('.back-to-top').click(() => {
        $('html, body').animate({ scrollTop: 0 }, 1000);
        return false;
    });
});