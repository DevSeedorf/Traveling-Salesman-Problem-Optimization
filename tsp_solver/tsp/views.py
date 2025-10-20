from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .aco import AntColonyTSP
from .abco import ArtificialBeeColonyTSP
from .utils import get_distance_matrix
from .models import TSPResult
import time
from django.contrib import messages

CITY_COORDINATES = {
    "Ilorin": (3, 5),
    "Lagos": (9, 2),
    "Abeokuta": (7, 3),
    "Ibadan": (5, 4),
    "Osogbo": (4, 6),
}

def tsp_aco_api(request):
    start_time = time.time()
    aco = AntColonyTSP()
    best_route, best_distance = aco.optimize()
    cities, _ = get_distance_matrix()
    
    # Convert to coordinates from model
    coordinates = []
    for city_idx in best_route:
        city = cities[city_idx]
        coordinates.append((city.x, city.y))
    
    # Close the loop
    coordinates.append(coordinates[0])
    route_names = [cities[i].name for i in best_route] + [cities[best_route[0]].name]
    
    # Create steps
    stepwise_routes = []
    for i in range(1, len(coordinates) + 1):
        stepwise_routes.append(coordinates[:i])
    
    # Save to database
    TSPResult.objects.create(
        algorithm='ACO',
        route=route_names,
        distance=best_distance,
        execution_time=time.time() - start_time
    )
    
    return JsonResponse({
        "algorithm": "Ant Colony Optimization (ACO)",
        "route": route_names,
        "distance": best_distance,
        "steps": stepwise_routes
    })

def tsp_abco_api(request):
    """API for ABCO optimized TSP route with step-by-step visualization"""
    start_time = time.time()
    abco = ArtificialBeeColonyTSP()
    best_route, best_distance = abco.optimize()
    cities, _ = get_distance_matrix()

    # The route already starts with Ilorin, just need to return to it
    best_route.append(best_route[0])  
    
    route_names = [cities[i].name for i in best_route]
    
    stepwise_routes = []
    for i in range(1, len(best_route) + 1):
        stepwise_routes.append([CITY_COORDINATES[cities[idx].name] for idx in best_route[:i]])

    # Save to database
    TSPResult.objects.create(
        algorithm='ABCO',
        route=route_names,
        distance=best_distance,
        execution_time=time.time() - start_time
    )

    return JsonResponse({
        "algorithm": "Artificial Bee Colony Optimization (ABCO)",
        "route": route_names,
        "distance": best_distance,
        "steps": stepwise_routes
    })

def tsp_home(request):
    """Render the visualization template for TSP"""
    # Get historical results for display
    aco_results = TSPResult.objects.filter(algorithm='ACO').order_by('-created_at')[:10]
    abco_results = TSPResult.objects.filter(algorithm='ABCO').order_by('-created_at')[:10]
    
    return render(request, "tsp_chart.html", {
        'aco_results': aco_results,
        'abco_results': abco_results,
    })

def tsp_result_detail(request, result_id):
    """View to display details of a single TSP result"""
    result = get_object_or_404(TSPResult, pk=result_id)
    
    # Prepare data for visualization
    cities, _ = get_distance_matrix()
    city_coords = {city.name: (city.x, city.y) for city in cities}
    
    route_coordinates = []
    for city_name in result.route:
        if city_name in city_coords:
            route_coordinates.append(city_coords[city_name])
    
    # Close the loop if not already closed
    if len(route_coordinates) > 1 and route_coordinates[0] != route_coordinates[-1]:
        route_coordinates.append(route_coordinates[0])
    
    # Prepare stepwise routes for animation
    stepwise_routes = []
    for i in range(1, len(route_coordinates) + 1):
        stepwise_routes.append(route_coordinates[:i])
    
    return render(request, "tsp_result_detail.html", {
        'result': result,
        'route_coordinates': route_coordinates,
        'stepwise_routes': stepwise_routes,
    })

def clear_tsp_results(request):
    """View to clear all TSP results from database"""
    if request.method == 'POST':
        count = TSPResult.objects.all().count()
        TSPResult.objects.all().delete()
        messages.success(request, f'Successfully deleted {count} TSP results.')
    return redirect('tsp_home')