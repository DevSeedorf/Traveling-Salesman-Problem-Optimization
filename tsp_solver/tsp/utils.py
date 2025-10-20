import random
from .models import City, Distance

def get_distance_matrix():
    # Explicitly fetch Ilorin first, then other cities
    ilorin = City.objects.get(name="Ilorin")
    other_cities = City.objects.exclude(name="Ilorin").order_by('name')
    cities = [ilorin] + list(other_cities)
    
    num_cities = len(cities)
    city_index = {city.id: idx for idx, city in enumerate(cities)}

    distance_matrix = [[0] * num_cities for _ in range(num_cities)]

    for city in cities:
        for other in cities:
            if city != other:
                # Get a random distance based on probability weights
                distances = Distance.objects.filter(
                    from_city=city,
                    to_city=other
                )
                if distances.exists():
                    dist_choices = [(d.distance, d.probability) for d in distances]
                    distances, probs = zip(*dist_choices)
                    distance = random.choices(distances, weights=probs)[0]
                    i = city_index[city.id]
                    j = city_index[other.id]
                    distance_matrix[i][j] = distance

    return cities, distance_matrix