import unittest
import json
import os
import numpy as np
from geoplot import GeoPlot

class TestGeoPlot(unittest.TestCase):
    def setUp(self):
        # Mock configuration
        self.config = {
            "simulation_metadata": {
                "name": "test_geo_visualization",
                "num_episodes": 2,
                "num_steps_per_episode": 1
            }        }
        
        # GeoPlot options
        self.options = {
            "cesium_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3M2RkZGI0YS05MDU0LTRkN2MtYmZlMy0yOGQ1MGE1MTdiZWYiLCJpZCI6Mjk4MDgxLCJpYXQiOjE3NDU4ODI0OTJ9.HB9001ySR1tZG_NQswUnC55IYDzbT_zvhC3SkrsUKIU",
            "step_time": 3600,
            "coordinates": "agents/consumers/coordinates",
            "feature": "agents/consumers/money_spent",
            "visualization_type": "color"  # or "size"
        }
        
        # Define polygon layers for overlay
        self.polygon_layers = [
            {
                "name": "City Boundaries",
                "geojson": {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [[-74.0, 40.7], [-74.1, 40.7], [-74.1, 40.8], [-74.0, 40.8], [-74.0, 40.7]]
                        ]
                    },
                    "properties": {
                        "color": "#00FF00"
                    }
                }
            }
        ]
        
        # Create state trajectory with both point and polygon data
        # First episode, single step
        step1 = {
            "agents": {
                "consumers": {
                    "coordinates": [
                        [40.7128, -74.0060],  # Point: NYC
                        [[37.7749, -122.4194], [37.8044, -122.2712], 
                         [37.3382, -121.8863], [37.7749, -122.4194]]  # Polygon: SF Bay Area
                    ],
                    "money_spent": [100.0, 200.0]
                }
            }
        }
        
        # Second episode, single step
        step2 = {
            "agents": {
                "consumers": {
                    "coordinates": [
                        [40.7128, -74.0060],  # Same point location
                        [[37.7749, -122.4194], [37.8044, -122.2712], 
                         [37.3382, -121.8863], [37.7749, -122.4194]]  # Same polygon
                    ],
                    "money_spent": [150.0, 250.0]  # Different values for time series
                }
            }
        }
        
        self.state_trajectory = [
            [step1],  # Episode 1
            [step2]   # Episode 2
        ]
    
    def test_render_points_and_polygons(self):
        # Create GeoPlot instance
        geo_plot = GeoPlot(self.config, self.options, self.polygon_layers)
        
        # Render visualization
        geo_plot.render(self.state_trajectory)
        
        # Verify files were created
        html_file = f"{self.config['simulation_metadata']['name']}.html"
        geojson_file = f"{self.config['simulation_metadata']['name']}.geojson"
        
        self.assertTrue(os.path.exists(html_file), f"HTML file {html_file} was not created")
        self.assertTrue(os.path.exists(geojson_file), f"GeoJSON file {geojson_file} was not created")
        
        # Check file contents
        with open(geojson_file, 'r') as f:
            geojson_data = json.load(f)
            self.assertIsInstance(geojson_data, list, "GeoJSON data should be a list")
            self.assertGreater(len(geojson_data), 0, "GeoJSON data should not be empty")
            
            # Check for both point and polygon features
            features = geojson_data[0]["features"]
            feature_types = [f["geometry"]["type"] for f in features]
            self.assertIn("Point", feature_types, "GeoJSON should contain Point features")
            self.assertIn("Polygon", feature_types, "GeoJSON should contain Polygon features")
        
        # Cleanup
        os.remove(html_file)
        os.remove(geojson_file)
    
    def tearDown(self):
        # Clean up any remaining files
        html_file = f"{self.config['simulation_metadata']['name']}.html"
        geojson_file = f"{self.config['simulation_metadata']['name']}.geojson"
        
        if os.path.exists(html_file):
            os.remove(html_file)
        if os.path.exists(geojson_file):
            os.remove(geojson_file)

if __name__ == "__main__":
    unittest.main()