-- =====================================================
-- SCHÉMA POSTGRESQL - LA CARAVELLA (VERSION CORRIGÉE)
-- Système de gestion de glaces artisanales
-- =====================================================

-- Configuration de la base de données
SET search_path = public;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLES DE BASE
-- =====================================================

-- Table des catégories de produits
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les catégories
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);
CREATE INDEX idx_categories_order ON categories("order");

-- Table des allergènes
CREATE TABLE allergens (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Table des parfums
CREATE TABLE flavors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#000000',
    is_active BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 0
);

-- Index pour les parfums
CREATE INDEX idx_flavors_slug ON flavors(slug);
CREATE INDEX idx_flavors_active ON flavors(is_active);

-- Table des produits
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    description TEXT,
    short_description VARCHAR(255),
    image VARCHAR(255),
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    product_type VARCHAR(20) DEFAULT 'ice_cream' CHECK (product_type IN ('ice_cream', 'sorbet', 'frozen_yogurt', 'gelato')),
    base_price DECIMAL(8,2) NOT NULL,
    sale_price DECIMAL(8,2),
    is_customizable BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    stock_quantity INTEGER DEFAULT 0,
    min_order_quantity INTEGER DEFAULT 1,
    max_order_quantity INTEGER DEFAULT 50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les produits
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_products_type ON products(product_type);

-- Table de relation produit-parfum
CREATE TABLE product_flavors (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    flavor_id INTEGER NOT NULL REFERENCES flavors(id) ON DELETE CASCADE,
    price_modifier DECIMAL(8,2) DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    "order" INTEGER DEFAULT 0,
    UNIQUE(product_id, flavor_id)
);

-- Table des images de produits
CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL,
    alt_text VARCHAR(200),
    is_primary BOOLEAN DEFAULT FALSE,
    "order" INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les images produits
CREATE INDEX idx_product_images_product ON product_images(product_id);
CREATE INDEX idx_product_images_primary ON product_images(is_primary);

-- Table des options de personnalisation
CREATE TABLE customization_options (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    option_type VARCHAR(20) NOT NULL CHECK (option_type IN ('topping', 'sauce', 'size', 'container')),
    description TEXT,
    price DECIMAL(8,2) DEFAULT 0,
    image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    max_selections INTEGER DEFAULT 1,
    "order" INTEGER DEFAULT 0
);

-- Table des avis produits
CREATE TABLE product_reviews (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200) NOT NULL,
    comment TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, user_id)
);

-- Index pour les avis
CREATE INDEX idx_reviews_product ON product_reviews(product_id);
CREATE INDEX idx_reviews_user ON product_reviews(user_id);
CREATE INDEX idx_reviews_approved ON product_reviews(is_approved);

-- Table des listes de souhaits
CREATE TABLE wishlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les listes de souhaits
CREATE INDEX idx_wishlists_user ON wishlists(user_id);

-- Table de relation wishlist-produits
CREATE TABLE wishlist_products (
    id SERIAL PRIMARY KEY,
    wishlist_id INTEGER NOT NULL REFERENCES wishlists(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(wishlist_id, product_id)
);

-- Index pour les relations wishlist-produits
CREATE INDEX idx_wishlist_products_wishlist ON wishlist_products(wishlist_id);
CREATE INDEX idx_wishlist_products_product ON wishlist_products(product_id);

-- =====================================================
-- TABLES UTILISATEURS
-- =====================================================

-- Table des profils utilisateurs
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE UNIQUE,
    phone VARCHAR(20),
    birth_date DATE,
    gender VARCHAR(10) CHECK (gender IN ('M', 'F', 'O')),
    newsletter_subscription BOOLEAN DEFAULT TRUE,
    loyalty_points INTEGER DEFAULT 0,
    loyalty_tier VARCHAR(20) DEFAULT 'bronze' CHECK (loyalty_tier IN ('bronze', 'silver', 'gold', 'platinum')),
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10,2) DEFAULT 0,
    last_order_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des activités utilisateurs
CREATE TABLE user_activities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    activity_type VARCHAR(20) NOT NULL CHECK (activity_type IN ('login', 'product_view', 'add_to_cart', 'purchase', 'review', 'wishlist_add', 'coupon_used')),
    description VARCHAR(255) NOT NULL,
    metadata JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les activités
CREATE INDEX idx_activities_user ON user_activities(user_id);
CREATE INDEX idx_activities_type ON user_activities(activity_type);
CREATE INDEX idx_activities_created ON user_activities(created_at);

-- Table du programme de parrainage
CREATE TABLE referral_programs (
    id SERIAL PRIMARY KEY,
    referrer_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    referred_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    referral_code VARCHAR(20) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    reward_claimed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des notifications
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    notification_type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    is_sent BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP WITH TIME ZONE
);

-- Table des préférences utilisateur
CREATE TABLE user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE UNIQUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    sms_notifications BOOLEAN DEFAULT FALSE,
    push_notifications BOOLEAN DEFAULT TRUE,
    preferred_shipping_method VARCHAR(50) DEFAULT 'standard',
    save_payment_info BOOLEAN DEFAULT FALSE,
    default_ice_cream_size VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLES E-COMMERCE
-- =====================================================

-- Table des adresses
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    address_type VARCHAR(20) NOT NULL CHECK (address_type IN ('shipping', 'billing')),
    is_default BOOLEAN DEFAULT FALSE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des paniers
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    session_key VARCHAR(40),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT carts_user_or_session CHECK ((user_id IS NOT NULL) OR (session_key IS NOT NULL))
);

-- Table des articles de panier
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    flavor_id INTEGER REFERENCES flavors(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    customizations JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, product_id, flavor_id)
);

-- Table des commandes
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    order_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (order_status IN ('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded')),
    payment_status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'failed', 'refunded')),
    shipping_address_id INTEGER NOT NULL REFERENCES addresses(id),
    billing_address_id INTEGER NOT NULL REFERENCES addresses(id),
    subtotal DECIMAL(10,2) NOT NULL,
    shipping_cost DECIMAL(8,2) NOT NULL,
    discount_amount DECIMAL(8,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    stripe_payment_intent_id VARCHAR(255),
    shipping_method VARCHAR(50) DEFAULT 'standard',
    tracking_number VARCHAR(100),
    estimated_delivery DATE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les commandes
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_number ON orders(order_number);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);

-- Table des articles de commande
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    flavor_id INTEGER REFERENCES flavors(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(8,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    customizations JSONB DEFAULT '{}'
);

-- Table des coupons
CREATE TABLE coupons (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    description VARCHAR(200) NOT NULL,
    coupon_type VARCHAR(20) NOT NULL CHECK (coupon_type IN ('percentage', 'fixed', 'free_shipping')),
    value DECIMAL(8,2) NOT NULL,
    min_order_amount DECIMAL(8,2) DEFAULT 0,
    max_uses INTEGER,
    used_count INTEGER DEFAULT 0,
    valid_from TIMESTAMP WITH TIME ZONE NOT NULL,
    valid_until TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index pour les coupons
CREATE INDEX idx_coupons_code ON coupons(code);
CREATE INDEX idx_coupons_active ON coupons(is_active);
CREATE INDEX idx_coupons_valid ON coupons(valid_from, valid_until);

-- =====================================================
-- TABLES DE RELATION MANY-TO-MANY
-- =====================================================

-- Table de relation produit-allergènes
CREATE TABLE product_allergens (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    allergen_id INTEGER NOT NULL REFERENCES allergens(id) ON DELETE CASCADE,
    UNIQUE(product_id, allergen_id)
);

-- Table de relation profil-parfums préférés
CREATE TABLE user_profile_favorite_flavors (
    id SERIAL PRIMARY KEY,
    userprofile_id INTEGER NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    flavor_id INTEGER NOT NULL REFERENCES flavors(id) ON DELETE CASCADE,
    UNIQUE(userprofile_id, flavor_id)
);

-- Table de relation profil-restrictions alimentaires
CREATE TABLE user_profile_dietary_restrictions (
    id SERIAL PRIMARY KEY,
    userprofile_id INTEGER NOT NULL REFERENCES user_profiles(id) ON DELETE CASCADE,
    allergen_id INTEGER NOT NULL REFERENCES allergens(id) ON DELETE CASCADE,
    UNIQUE(userprofile_id, allergen_id)
);

-- =====================================================
-- TRIGGERS ET FONCTIONS
-- =====================================================

-- Fonction pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers pour updated_at
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_addresses_updated_at BEFORE UPDATE ON addresses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_carts_updated_at BEFORE UPDATE ON carts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cart_items_updated_at BEFORE UPDATE ON cart_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_wishlists_updated_at BEFORE UPDATE ON wishlists FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Fonction pour générer un numéro de commande unique
CREATE OR REPLACE FUNCTION generate_order_number()
RETURNS TRIGGER AS $$
BEGIN
    NEW.order_number = 'ORD-' || TO_CHAR(NEW.created_at, 'YYYYMMDD') || '-' || LPAD(NEW.id::TEXT, 6, '0');
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour générer le numéro de commande
CREATE TRIGGER generate_order_number_trigger BEFORE INSERT ON orders FOR EACH ROW EXECUTE FUNCTION generate_order_number();

-- =====================================================
-- VUES
-- =====================================================

-- Vue des produits avec catégories
CREATE VIEW products_with_categories AS
SELECT 
    p.*,
    c.name as category_name,
    c.slug as category_slug
FROM products p
JOIN categories c ON p.category_id = c.id;

-- Vue des commandes avec informations utilisateur
CREATE VIEW orders_with_user AS
SELECT 
    o.*,
    u.username,
    u.email,
    u.first_name,
    u.last_name
FROM orders o
JOIN auth_user u ON o.user_id = u.id;

-- Vue des statistiques de produits
CREATE VIEW product_stats AS
SELECT 
    p.id,
    p.name,
    p.base_price,
    p.sale_price,
    COUNT(pr.id) as review_count,
    AVG(pr.rating) as average_rating,
    COUNT(oi.id) as order_count,
    SUM(oi.quantity) as total_sold
FROM products p
LEFT JOIN product_reviews pr ON p.id = pr.product_id AND pr.is_approved = true
LEFT JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name, p.base_price, p.sale_price;

-- =====================================================
-- DONNÉES DE TEST
-- =====================================================

-- Insertion des catégories
INSERT INTO categories (name, slug, description, "order") VALUES
('Glaces Artisanales', 'glaces-artisanales', 'Nos glaces artisanales préparées avec des ingrédients naturels', 1),
('Sorbets', 'sorbets', 'Des sorbets rafraîchissants à base de fruits frais', 2),
('Yaourts Glacés', 'yaourts-glaces', 'Nos yaourts glacés crémeux et légers', 3),
('Gelato Italien', 'gelato-italien', 'Authentique gelato italien avec une densité incomparable', 4),
('Glaces Végétales', 'glaces-vegetales', 'Nos glaces 100% végétales, sans lactose ni œufs', 5);

-- Insertion des allergènes
INSERT INTO allergens (name, icon, description) VALUES
('Lait', '🥛', 'Produits laitiers'),
('Œufs', '🥚', 'Œufs et produits dérivés'),
('Fruits à coque', '🥜', 'Noix, amandes, pistaches, etc.'),
('Gluten', '🌾', 'Blé, orge, seigle, avoine'),
('Soja', '🫘', 'Soja et produits dérivés'),
('Sulfites', '🍷', 'Conservateurs à base de soufre');

-- Insertion des parfums
INSERT INTO flavors (name, slug, description, color, "order") VALUES
('Vanille', 'vanille', 'Gousse de vanille de Madagascar', '#F5DEB3', 1),
('Chocolat', 'chocolat', 'Chocolat noir 70% cacao', '#8B4513', 2),
('Fraise', 'fraise', 'Fraise Gariguette', '#FF69B4', 3),
('Pistache', 'pistache', 'Pistache de Sicile', '#32CD32', 4),
('Coco', 'coco', 'Noix de coco fraîche', '#F0F8FF', 5),
('Citron', 'citron', 'Citron vert bio', '#FFFF00', 6);

-- =====================================================
-- COMMENTAIRES
-- =====================================================

COMMENT ON TABLE categories IS 'Catégories de produits (glaces, sorbets, etc.)';
COMMENT ON TABLE products IS 'Produits principaux du catalogue';
COMMENT ON TABLE flavors IS 'Parfums disponibles pour les produits';
COMMENT ON TABLE allergens IS 'Allergènes et restrictions alimentaires';
COMMENT ON TABLE orders IS 'Commandes clients';
COMMENT ON TABLE user_profiles IS 'Profils utilisateurs étendus avec programme de fidélité';

COMMENT ON COLUMN products.product_type IS 'Type de produit: ice_cream, sorbet, frozen_yogurt, gelato';
COMMENT ON COLUMN orders.order_status IS 'Statut de la commande: pending, confirmed, processing, shipped, delivered, cancelled, refunded';
COMMENT ON COLUMN orders.payment_status IS 'Statut du paiement: pending, paid, failed, refunded';
COMMENT ON COLUMN user_profiles.loyalty_tier IS 'Niveau de fidélité: bronze, silver, gold, platinum';

-- =====================================================
-- FIN DU SCHÉMA
-- =====================================================
