from django.db import models
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    x = models.FloatField(default=0)  # X coordinate
    y = models.FloatField(default=0)  # Y coordinate

    def __str__(self):
        return self.name

class Distance(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="from_city")
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="to_city")
    distance = models.IntegerField()
    probability = models.FloatField(default=1.0)
    
    def __str__(self):
        return f"{self.from_city} -> {self.to_city}: {self.distance} km (weight: {self.probability})"

class TSPResult(models.Model):
    ALGORITHM_CHOICES = [
        ('ACO', 'Ant Colony Optimization'),
        ('ABCO', 'Artificial Bee Colony Optimization'),
    ]
    
    algorithm = models.CharField(max_length=4, choices=ALGORITHM_CHOICES)
    route = models.JSONField()  # Stores list of city names
    distance = models.FloatField()
    execution_time = models.FloatField(null=True, blank=True)  # In seconds
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.get_algorithm_display()} - {self.distance} km - {self.created_at.strftime('%Y-%m-%d %H:%M')}"