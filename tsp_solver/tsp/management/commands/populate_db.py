from django.core.management.base import BaseCommand
from tsp.models import City, Distance

class Command(BaseCommand):
    help = "Populate database with initial cities and distances"

    def handle(self, *args, **kwargs):
        cities = ["Ilorin", "Lagos", "Abeokuta", "Ibadan", "Osogbo"]

        city_objects = {}
        for city_name in cities:
            city, created = City.objects.get_or_create(name=city_name)
            city_objects[city_name] = city

        distances = [
            # Ilorin connections
            ("Ilorin", "Lagos", 300, 0.7),  # 70% chance
            ("Ilorin", "Lagos", 280, 0.3),  # 30% chance (alternative route)
            ("Ilorin", "Abeokuta", 250, 0.7),
            ("Ilorin", "Abeokuta", 200, 0.3),
            ("Ilorin", "Ibadan", 180, 0.6),
            ("Ilorin", "Ibadan", 150, 0.4),
            ("Ilorin", "Osogbo", 100, 1.0),
            
            # Other connections
            ("Lagos", "Abeokuta", 100, 0.5),
            ("Lagos", "Abeokuta", 90, 0.5),
            ("Lagos", "Ibadan", 130, 0.7),
            ("Lagos", "Ibadan", 120, 0.3),
            ("Lagos", "Osogbo", 190, 1.0),
            ("Abeokuta", "Ibadan", 80, 0.6),
            ("Abeokuta", "Ibadan", 75, 0.4),
            ("Abeokuta", "Osogbo", 120, 1.0),
            ("Ibadan", "Osogbo", 90, 1.0),
        ]


        cities_data = [
            ("Ilorin", 3, 5),
            ("Lagos", 9, 2),
            ("Abeokuta", 7, 3),
            ("Ibadan", 5, 4),
            ("Osogbo", 4, 6),
        ]

        for name, x, y in cities_data:
            city, created = City.objects.get_or_create(
                name=name,
                defaults={'x': x, 'y': y}
            )
            if not created:
                city.x = x
                city.y = y
                city.save()

        for from_city, to_city, distance, prob in distances:
            Distance.objects.get_or_create(
                from_city=city_objects[from_city],
                to_city=city_objects[to_city],
                distance=distance,
                probability=prob
            )
            # Create reverse direction
            Distance.objects.get_or_create(
                from_city=city_objects[to_city],
                to_city=city_objects[from_city],
                distance=distance,
                probability=prob
            )

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
