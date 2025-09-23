/**
 * Système de personnalisation des glaces La Caravela
 * Inspiré de Magnum Create
 */

class IceCreamCustomizer {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            apiBaseUrl: '/products/ajax/',
            currency: 'MAD',
            ...options
        };
        
        this.currentProduct = null;
        this.selectedFlavor = null;
        this.selectedCustomizations = {};
        this.totalPrice = 0;
        
        this.init();
    }
    
    init() {
        this.render();
        this.bindEvents();
        this.loadCustomizationOptions();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="ice-cream-customizer">
                <div class="customizer-header">
                    <h3>Personnalisez votre glace</h3>
                    <div class="price-display">
                        <span class="total-price">0.00 MAD</span>
                    </div>
                </div>
                
                <div class="customizer-sections">
                    <!-- Section Parfum -->
                    <div class="customizer-section" id="flavor-section">
                        <h4>Choisissez votre parfum</h4>
                        <div class="flavor-grid" id="flavor-grid"></div>
                    </div>
                    
                    <!-- Section Toppings -->
                    <div class="customizer-section" id="toppings-section">
                        <h4>Ajoutez vos toppings</h4>
                        <div class="toppings-grid" id="toppings-grid"></div>
                    </div>
                    
                    <!-- Section Sauces -->
                    <div class="customizer-section" id="sauces-section">
                        <h4>Sélectionnez vos sauces</h4>
                        <div class="sauces-grid" id="sauces-grid"></div>
                    </div>
                    
                    <!-- Section Taille -->
                    <div class="customizer-section" id="size-section">
                        <h4>Choisissez votre taille</h4>
                        <div class="size-options" id="size-options"></div>
                    </div>
                </div>
                
                <div class="customizer-summary">
                    <h4>Récapitulatif</h4>
                    <div class="summary-items" id="summary-items"></div>
                </div>
                
                <div class="customizer-actions">
                    <button class="btn btn-secondary" id="reset-customization">Recommencer</button>
                    <button class="btn btn-primary" id="add-to-cart">Ajouter au panier</button>
                </div>
            </div>
        `;
    }
    
    bindEvents() {
        // Reset button
        document.getElementById('reset-customization').addEventListener('click', () => {
            this.resetCustomization();
        });
        
        // Add to cart button
        document.getElementById('add-to-cart').addEventListener('click', () => {
            this.addToCart();
        });
    }
    
    async loadCustomizationOptions() {
        try {
            const response = await fetch(`${this.options.apiBaseUrl}customization-options/`);
            const data = await response.json();
            
            this.renderFlavors(data.flavors || []);
            this.renderToppings(data.toppings || []);
            this.renderSauces(data.sauces || []);
            this.renderSizes(data.sizes || []);
            
        } catch (error) {
            console.error('Erreur lors du chargement des options:', error);
        }
    }
    
    renderFlavors(flavors) {
        const grid = document.getElementById('flavor-grid');
        grid.innerHTML = flavors.map(flavor => `
            <div class="flavor-option" data-flavor-id="${flavor.id}">
                <div class="flavor-color" style="background-color: ${flavor.color}"></div>
                <div class="flavor-info">
                    <h5>${flavor.name}</h5>
                    <p>${flavor.description}</p>
                    <span class="price-modifier">${flavor.price_modifier > 0 ? '+' : ''}${flavor.price_modifier} MAD</span>
                </div>
            </div>
        `).join('');
        
        // Bind flavor selection events
        grid.querySelectorAll('.flavor-option').forEach(option => {
            option.addEventListener('click', () => {
                this.selectFlavor(option.dataset.flavorId);
            });
        });
    }
    
    renderToppings(toppings) {
        const grid = document.getElementById('toppings-grid');
        grid.innerHTML = toppings.map(topping => `
            <div class="customization-option" data-option-id="${topping.id}" data-type="topping">
                <div class="option-image">
                    ${topping.image_url ? `<img src="${topping.image_url}" alt="${topping.name}">` : ''}
                </div>
                <div class="option-info">
                    <h5>${topping.name}</h5>
                    <p>${topping.description}</p>
                    <div class="option-controls">
                        <span class="price">${topping.price} MAD</span>
                        <div class="quantity-controls">
                            <button class="qty-btn minus" data-action="decrease">-</button>
                            <span class="quantity">0</span>
                            <button class="qty-btn plus" data-action="increase">+</button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
        
        this.bindCustomizationEvents('topping');
    }
    
    renderSauces(sauces) {
        const grid = document.getElementById('sauces-grid');
        grid.innerHTML = sauces.map(sauce => `
            <div class="customization-option" data-option-id="${sauce.id}" data-type="sauce">
                <div class="option-image">
                    ${sauce.image_url ? `<img src="${sauce.image_url}" alt="${sauce.name}">` : ''}
                </div>
                <div class="option-info">
                    <h5>${sauce.name}</h5>
                    <p>${sauce.description}</p>
                    <div class="option-controls">
                        <span class="price">${sauce.price} MAD</span>
                        <div class="quantity-controls">
                            <button class="qty-btn minus" data-action="decrease">-</button>
                            <span class="quantity">0</span>
                            <button class="qty-btn plus" data-action="increase">+</button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
        
        this.bindCustomizationEvents('sauce');
    }
    
    renderSizes(sizes) {
        const container = document.getElementById('size-options');
        container.innerHTML = sizes.map(size => `
            <div class="size-option" data-size-id="${size.id}">
                <div class="size-info">
                    <h5>${size.name}</h5>
                    <p>${size.description}</p>
                    <span class="price">${size.price} MAD</span>
                </div>
            </div>
        `).join('');
        
        // Bind size selection events
        container.querySelectorAll('.size-option').forEach(option => {
            option.addEventListener('click', () => {
                this.selectSize(option.dataset.sizeId);
            });
        });
    }
    
    bindCustomizationEvents(type) {
        const options = document.querySelectorAll(`[data-type="${type}"]`);
        
        options.forEach(option => {
            const optionId = option.dataset.optionId;
            const minusBtn = option.querySelector('.qty-btn.minus');
            const plusBtn = option.querySelector('.qty-btn.plus');
            const quantitySpan = option.querySelector('.quantity');
            
            minusBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.updateCustomizationQuantity(optionId, -1);
            });
            
            plusBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.updateCustomizationQuantity(optionId, 1);
            });
        });
    }
    
    selectFlavor(flavorId) {
        // Remove previous selection
        document.querySelectorAll('.flavor-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selection to clicked option
        const selectedOption = document.querySelector(`[data-flavor-id="${flavorId}"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
            this.selectedFlavor = flavorId;
            this.updatePrice();
            this.updateSummary();
        }
    }
    
    selectSize(sizeId) {
        // Remove previous selection
        document.querySelectorAll('.size-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selection to clicked option
        const selectedOption = document.querySelector(`[data-size-id="${sizeId}"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
            this.selectedSize = sizeId;
            this.updatePrice();
            this.updateSummary();
        }
    }
    
    updateCustomizationQuantity(optionId, change) {
        const currentQuantity = this.selectedCustomizations[optionId] || 0;
        const newQuantity = Math.max(0, currentQuantity + change);
        
        if (newQuantity === 0) {
            delete this.selectedCustomizations[optionId];
        } else {
            this.selectedCustomizations[optionId] = newQuantity;
        }
        
        // Update UI
        const option = document.querySelector(`[data-option-id="${optionId}"]`);
        if (option) {
            const quantitySpan = option.querySelector('.quantity');
            quantitySpan.textContent = newQuantity;
            
            // Update button states
            const minusBtn = option.querySelector('.qty-btn.minus');
            minusBtn.disabled = newQuantity === 0;
        }
        
        this.updatePrice();
        this.updateSummary();
    }
    
    async updatePrice() {
        if (!this.currentProduct) return;
        
        try {
            const response = await fetch(`${this.options.apiBaseUrl}calculate-price/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    product_id: this.currentProduct.id,
                    flavor_id: this.selectedFlavor,
                    customizations: Object.entries(this.selectedCustomizations).map(([id, quantity]) => ({
                        option_id: parseInt(id),
                        quantity: quantity
                    }))
                })
            });
            
            const data = await response.json();
            this.totalPrice = data.total_price;
            
            // Update price display
            const priceDisplay = document.querySelector('.total-price');
            priceDisplay.textContent = `${data.total_price.toFixed(2)} MAD`;
            
        } catch (error) {
            console.error('Erreur lors du calcul du prix:', error);
        }
    }
    
    updateSummary() {
        const summaryContainer = document.getElementById('summary-items');
        const items = [];
        
        // Add base product
        if (this.currentProduct) {
            items.push({
                name: this.currentProduct.name,
                price: this.currentProduct.base_price
            });
        }
        
        // Add selected flavor
        if (this.selectedFlavor) {
            const flavorOption = document.querySelector(`[data-flavor-id="${this.selectedFlavor}"]`);
            if (flavorOption) {
                const flavorName = flavorOption.querySelector('h5').textContent;
                const priceModifier = parseFloat(flavorOption.querySelector('.price-modifier').textContent.replace(/[^0-9.-]/g, ''));
                items.push({
                    name: `Parfum: ${flavorName}`,
                    price: priceModifier
                });
            }
        }
        
        // Add customizations
        Object.entries(this.selectedCustomizations).forEach(([optionId, quantity]) => {
            const option = document.querySelector(`[data-option-id="${optionId}"]`);
            if (option) {
                const optionName = option.querySelector('h5').textContent;
                const optionPrice = parseFloat(option.querySelector('.price').textContent.replace(/[^0-9.-]/g, ''));
                items.push({
                    name: `${optionName} x${quantity}`,
                    price: optionPrice * quantity
                });
            }
        });
        
        // Render summary
        summaryContainer.innerHTML = items.map(item => `
            <div class="summary-item">
                <span class="item-name">${item.name}</span>
                <span class="item-price">${item.price > 0 ? '+' : ''}${item.price.toFixed(2)} MAD</span>
            </div>
        `).join('');
    }
    
    resetCustomization() {
        this.selectedFlavor = null;
        this.selectedCustomizations = {};
        this.selectedSize = null;
        
        // Reset UI
        document.querySelectorAll('.flavor-option, .size-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        document.querySelectorAll('.quantity').forEach(span => {
            span.textContent = '0';
        });
        
        document.querySelectorAll('.qty-btn.minus').forEach(btn => {
            btn.disabled = true;
        });
        
        this.updatePrice();
        this.updateSummary();
    }
    
    async addToCart() {
        if (!this.currentProduct) {
            alert('Veuillez sélectionner un produit');
            return;
        }
        
        const cartData = {
            product_id: this.currentProduct.id,
            flavor_id: this.selectedFlavor,
            customizations: this.selectedCustomizations,
            quantity: 1
        };
        
        try {
            const response = await fetch('/checkout/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify(cartData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message
                this.showNotification('Produit ajouté au panier !', 'success');
                
                // Update cart count in header
                this.updateCartCount(result.cart_count);
                
                // Reset customization
                this.resetCustomization();
            } else {
                this.showNotification(result.error || 'Erreur lors de l\'ajout au panier', 'error');
            }
            
        } catch (error) {
            console.error('Erreur lors de l\'ajout au panier:', error);
            this.showNotification('Erreur lors de l\'ajout au panier', 'error');
        }
    }
    
    setProduct(product) {
        this.currentProduct = product;
        this.updatePrice();
        this.updateSummary();
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    updateCartCount(count) {
        const cartCountElement = document.querySelector('.cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    }
}

// Initialize customizer when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const customizerContainer = document.getElementById('ice-cream-customizer');
    if (customizerContainer) {
        window.iceCreamCustomizer = new IceCreamCustomizer('ice-cream-customizer');
    }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IceCreamCustomizer;
} 