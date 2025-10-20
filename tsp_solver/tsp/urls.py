from django.urls import path
from .views import tsp_aco_api, tsp_abco_api, tsp_home, tsp_result_detail, clear_tsp_results

urlpatterns = [
    path('tsp/aco/api/', tsp_aco_api, name='tsp_aco_api'),
    path('tsp/abco/api/', tsp_abco_api, name='tsp_abco_api'),
    path('tsp/', tsp_home, name='tsp_home'),  # Visualization page
    path('tsp/results/<int:result_id>/', tsp_result_detail, name='tsp_result_detail'),
    path('tsp/clear-results/', clear_tsp_results, name='clear_tsp_results'),
]
