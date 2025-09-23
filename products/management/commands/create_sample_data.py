from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Créer des données d\'exemple pour La Caravela'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🍦 Création des données d\'exemple...'))
        
        # Créer des catégories
        categories_data = [
            {'name': 'Glaces Classiques', 'description': 'Nos glaces traditionnelles aux parfums intemporels'},
            {'name': 'Glaces Exotiques', 'description': 'Des parfums du monde entier pour voyager'},
            {'name': 'Glaces Bio', 'description': 'Glaces biologiques aux ingrédients naturels'},
            {'name': 'Glaces Sans Lactose', 'description': 'Pour ceux qui préfèrent sans lactose'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f"✅ Catégorie créée: {category.name}")
        
        # Créer des produits
        products_data = [
        {
            'name': 'Vanille de Madagascar',
            'description': 'Une glace onctueuse à la vanille bourbon de Madagascar',
            'base_price': 4.50,
            'category': categories[0],
            'is_featured': True,
            'stock_quantity': 100
        },
        {
            'name': 'Chocolat Noir 70%',
            'description': 'Glace intense au chocolat noir équitable',
            'base_price': 5.00,
            'category': categories[0],
            'is_featured': True,
            'stock_quantity': 80
        },
        {
            'name': 'Fraise Gariguette',
            'description': 'Glace aux fraises de Carpentras',
            'base_price': 4.80,
            'category': categories[0],
            'stock_quantity': 60
        },
        {
            'name': 'Mangue Passion',
            'description': 'Mélange exotique de mangue et fruit de la passion',
            'base_price': 5.50,
            'category': categories[1],
            'is_featured': True,
            'stock_quantity': 40
        },
        {
            'name': 'Coco Lime',
            'description': 'Glace coco rafraîchissante au zeste de citron vert',
            'base_price': 5.20,
            'category': categories[1],
            'stock_quantity': 50
        },
        {
            'name': 'Lavande de Provence',
            'description': 'Glace parfumée à la lavande de Provence',
            'base_price': 5.80,
            'category': categories[2],
            'is_featured': True,
            'stock_quantity': 35
        },
        {
            'name': 'Amande Bio',
            'description': 'Glace à l\'amande sans lactose',
            'base_price': 5.60,
            'category': categories[3],
            'stock_quantity': 55
        },
        {
            'name': 'Pistache de Sicile',
            'description': 'Glace à la pistache AOP de Sicile',
            'base_price': 6.50,
            'category': categories[0],
            'is_featured': True,
            'stock_quantity': 25
        }
        ]
        
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'base_price': prod_data['base_price'],
                    'category': prod_data['category'],
                    'is_featured': prod_data.get('is_featured', False),
                    'stock_quantity': prod_data.get('stock_quantity', 50),
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"✅ Produit créé: {product.name} - {product.base_price}€")
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Données d\'exemple créées avec succès !'))
        self.stdout.write(f"📊 {len(categories)} catégories créées")
        self.stdout.write(f"🍦 {len(products_data)} produits créés")
        self.stdout.write("\n🌐 Vous pouvez maintenant visiter:")
        self.stdout.write("   - http://127.0.0.1:8000/ (Page d'accueil)")
        self.stdout.write("   - http://127.0.0.1:8000/demo/ (Démonstration des effets)")
        self.stdout.write("   - http://127.0.0.1:8000/admin/ (Administration Django)")
        self.stdout.write("   - http://127.0.0.1:8000/products/ (Liste des produits)")
