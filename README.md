# TSP Solver - Traveling Salesman Problem Optimization

A Django web application that solves the Traveling Salesman Problem (TSP) using two nature-inspired optimization algorithms: **Ant Colony Optimization (ACO)** and **Artificial Bee Colony Optimization (ABCO)**.

## 🌟 Features

- **Two Optimization Algorithms**:
  - Ant Colony Optimization (ACO)
  - Artificial Bee Colony Optimization (ABCO)
- **Web-based Interface**: Interactive visualization of TSP solutions
- **Route Visualization**: Graphical representation of optimized routes
- **Performance Comparison**: Compare execution times and solution quality
- **Data Persistence**: Store and view historical results
- **Nigerian Cities Dataset**: Pre-configured with 5 Nigerian cities (Ilorin, Lagos, Abeokuta, Ibadan, Osogbo)

## 🏗️ Project Structure

```
tsp_solver/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database
├── tsp/                         # Main TSP application
│   ├── models.py               # Database models (City, Distance, TSPResult)
│   ├── views.py                # Web views and API endpoints
│   ├── urls.py                 # URL routing
│   ├── aco.py                  # Ant Colony Optimization implementation
│   ├── abco.py                 # Artificial Bee Colony Optimization implementation
│   ├── utils.py                # Utility functions
│   ├── templates/              # HTML templates
│   │   ├── tsp_chart.html      # Main visualization page
│   │   ├── tsp_result.html     # Results listing
│   │   └── tsp_result_detail.html  # Individual result details
│   └── management/
│       └── commands/
│           └── populate_db.py  # Database population script
├── tsp_solver/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── virt/                       # Virtual environment
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   git clone https://github.com/DevSeedorf/Traveling-Salesman-Problem-Optimization.git
   ```

2. **Create and activate the virtual environment**:
   ```bash
   # Windows
   python -m venv virt
   virt\Scripts\activate
   
   # Or using PowerShell
   .\virt\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   The project uses the following packages:
   - Django 5.1.7
   - NumPy 2.2.4
   - Matplotlib 3.10.1
   - Other supporting packages

4. **Navigate to the Django project**:
   ```bash
   cd tsp_solver
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Populate the database with sample data**:
   ```bash
   python manage.py populate_db
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:8000/tsp/`

## 🎯 Usage

### Web Interface

1. **Main Dashboard** (`/tsp/`): 
   - View the interactive map with city locations
   - Run ACO or ABCO algorithms
   - Visualize the optimized routes

2. **API Endpoints**:
   - `GET /tsp/aco/api/` - Run Ant Colony Optimization
   - `GET /tsp/abco/api/` - Run Artificial Bee Colony Optimization
   - `GET /tsp/results/<id>/` - View specific result details
   - `POST /tsp/clear-results/` - Clear all stored results

### Algorithm Parameters

#### Ant Colony Optimization (ACO)
- **Number of Ants**: 15
- **Iterations**: 100
- **Alpha (α)**: 1.0 (pheromone importance)
- **Beta (β)**: 3.0 (distance importance)
- **Evaporation Rate**: 0.3

#### Artificial Bee Colony Optimization (ABCO)
- **Colony Size**: 20
- **Max Iterations**: 200
- **Trials Limit**: 15

## 🏙️ Cities Dataset

The application comes pre-configured with 5 Nigerian cities:

| City | Coordinates (x, y) |
|------|-------------------|
| Ilorin | (3, 5) |
| Lagos | (9, 2) |
| Abeokuta | (7, 3) |
| Ibadan | (5, 4) |
| Osogbo | (4, 6) |

**Note**: All routes start and end at Ilorin.

## 🔬 Algorithm Details

### Ant Colony Optimization (ACO)
- Simulates the behavior of ants finding the shortest path
- Uses pheromone trails to guide future ants
- Balances exploration and exploitation through α and β parameters
- Implements pheromone evaporation to avoid local optima

### Artificial Bee Colony Optimization (ABCO)
- Mimics the foraging behavior of honey bees
- Uses employed bees, onlooker bees, and scout bees
- Implements neighborhood search for solution improvement
- Abandons poor solutions after a trials limit

## 📊 Data Models

### City
- `name`: City name (unique)
- `x`, `y`: Coordinates for visualization

### Distance
- `from_city`, `to_city`: City connections
- `distance`: Distance in kilometers
- `probability`: Route probability weight

### TSPResult
- `algorithm`: ACO or ABCO
- `route`: Optimized city sequence (JSON)
- `distance`: Total route distance
- `execution_time`: Algorithm runtime
- `created_at`: Timestamp

## 🛠️ Development

### Adding New Cities
1. Update the `populate_db.py` command with new city data
2. Run `python manage.py populate_db` to update the database

### Modifying Algorithms
- ACO parameters can be adjusted in `aco.py` constructor
- ABCO parameters can be modified in `abco.py` constructor

### Custom Distance Matrices
Modify the `get_distance_matrix()` function in `utils.py` to use different datasets.

## 📈 Performance Notes

- ACO typically converges faster but may get stuck in local optima
- ABCO explores the solution space more thoroughly but takes longer
- Results may vary between runs due to the stochastic nature of the algorithms
- Execution times are stored for performance comparison

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔍 Troubleshooting

### Common Issues

1. **Virtual Environment Issues**:
   ```bash
   # Recreate if needed
   python -m venv virt
   virt\Scripts\activate
   pip install django numpy matplotlib
   ```

2. **Database Issues**:
   ```bash
   # Reset database
   python manage.py migrate --run-syncdb
   python manage.py populate_db
   ```

3. **Port Already in Use**:
   ```bash
   # Use different port
   python manage.py runserver 8001
   ```

## 📚 References

- Dorigo, M., & Gambardella, L. M. (1997). Ant colony system: a cooperative learning approach to the traveling salesman problem.
- Karaboga, D., & Gorkemli, B. (2011). A quick artificial bee colony (qABC) algorithm and its performance on optimization problems.

---

**Built with Django 5.1.7 and Python 3.12**