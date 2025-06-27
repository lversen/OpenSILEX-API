"""
OpenSilex Python Utilities and Advanced Examples
Additional utilities for data analysis, visualization, and batch operations
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp
from collections import defaultdict

# Import the main client (assuming it's in a file called opensilex_client.py)
# from opensilex_client import OpenSilexClient


class OpenSilexDataAnalyzer:
    """
    Utility class for analyzing data retrieved from OpenSilex.
    """
    
    def __init__(self, client):
        """
        Initialize the analyzer with an OpenSilex client.
        
        Args:
            client: An instance of OpenSilexClient
        """
        self.client = client
    
    def data_to_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """
        Convert OpenSilex data to a pandas DataFrame.
        
        Args:
            data: List of data points from OpenSilex
            
        Returns:
            DataFrame with parsed data
        """
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Parse dates if present
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Extract URIs to more readable format if needed
        for col in ['variable', 'scientific_object', 'experiment']:
            if col in df.columns:
                df[f'{col}_short'] = df[col].apply(
                    lambda x: x.split('/')[-1] if isinstance(x, str) else x
                )
        
        return df
    
    def get_experiment_summary(self, experiment_uri: str) -> Dict:
        """
        Get a comprehensive summary of an experiment.
        
        Args:
            experiment_uri: URI of the experiment
            
        Returns:
            Dictionary with experiment summary
        """
        summary = {
            'experiment_uri': experiment_uri,
            'scientific_objects': {},
            'variables': {},
            'data_points': 0,
            'date_range': None,
            'events': []
        }
        
        # Get experiment details
        exp_details = self.client.get_experiment(experiment_uri)
        if exp_details:
            summary['name'] = exp_details.get('name', 'Unknown')
            summary['start_date'] = exp_details.get('start_date')
            summary['end_date'] = exp_details.get('end_date')
        
        # Get scientific objects
        objects = self.client.get_all_pages(
            'get_scientific_objects',
            experiment_uri=experiment_uri
        )
        
        for obj in objects:
            obj_type = obj.get('rdf_type', 'Unknown')
            if obj_type not in summary['scientific_objects']:
                summary['scientific_objects'][obj_type] = 0
            summary['scientific_objects'][obj_type] += 1
        
        # Get data
        data = self.client.get_all_pages(
            'get_data',
            experiment_uri=experiment_uri
        )
        
        if data:
            df = self.data_to_dataframe(data)
            summary['data_points'] = len(df)
            
            if 'date' in df.columns:
                summary['date_range'] = (
                    df['date'].min().isoformat(),
                    df['date'].max().isoformat()
                )
            
            # Count by variable
            if 'variable' in df.columns:
                for var, count in df['variable'].value_counts().items():
                    summary['variables'][var] = count
        
        # Get events
        events = self.client.get_events(experiment_uri=experiment_uri)
        if events:
            summary['events'] = [
                {
                    'type': e.get('rdf_type', 'Unknown'),
                    'date': e.get('date', 'Unknown'),
                    'description': e.get('description', '')
                }
                for e in events
            ]
        
        return summary
    
    def plot_time_series(self, experiment_uri: str, variable_uri: str, 
                        scientific_object_uri: Optional[str] = None):
        """
        Plot time series data for a specific variable.
        
        Args:
            experiment_uri: URI of the experiment
            variable_uri: URI of the variable to plot
            scientific_object_uri: Optional specific object to plot
        """
        # Get data
        data = self.client.get_all_pages(
            'get_data',
            experiment_uri=experiment_uri,
            variable_uri=variable_uri,
            scientific_object_uri=scientific_object_uri
        )
        
        if not data:
            print("No data found for plotting")
            return
        
        df = self.data_to_dataframe(data)
        
        # Create plot
        plt.figure(figsize=(12, 6))
        
        if scientific_object_uri:
            # Single object plot
            plt.plot(df['date'], df['value'], marker='o')
            plt.title(f"Time Series: {variable_uri.split('/')[-1]}")
        else:
            # Multiple objects - group by scientific object
            for obj, group in df.groupby('scientific_object'):
                plt.plot(group['date'], group['value'], 
                        marker='o', label=obj.split('/')[-1])
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


class OpenSilexBatchProcessor:
    """
    Utility class for batch operations with OpenSilex.
    """
    
    def __init__(self, client):
        """
        Initialize the batch processor.
        
        Args:
            client: An instance of OpenSilexClient
        """
        self.client = client
    
    def batch_upload_data(self, csv_file: str, mapping: Dict[str, str]) -> Tuple[int, List[str]]:
        """
        Upload data from a CSV file to OpenSilex.
        
        Args:
            csv_file: Path to CSV file
            mapping: Dictionary mapping CSV columns to OpenSilex fields
                    Example: {
                        'date_column': 'date',
                        'value_column': 'value',
                        'plant_id': 'scientific_object',
                        'measurement_type': 'variable'
                    }
        
        Returns:
            Tuple of (success_count, list of errors)
        """
        df = pd.read_csv(csv_file)
        
        # Prepare data for upload
        data_list = []
        errors = []
        
        for idx, row in df.iterrows():
            try:
                data_point = {}
                
                for csv_col, api_field in mapping.items():
                    if csv_col in df.columns:
                        value = row[csv_col]
                        
                        # Handle date conversion
                        if api_field == 'date':
                            if not pd.isna(value):
                                # Convert to ISO format
                                date_obj = pd.to_datetime(value)
                                value = date_obj.isoformat() + 'Z'
                        
                        data_point[api_field] = value
                
                data_list.append(data_point)
                
            except Exception as e:
                errors.append(f"Row {idx}: {str(e)}")
        
        # Upload in batches
        batch_size = 100
        success_count = 0
        
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i + batch_size]
            
            if self.client.post_data(batch):
                success_count += len(batch)
            else:
                errors.append(f"Failed to upload batch {i//batch_size + 1}")
        
        return success_count, errors
    
    def export_experiment_data(self, experiment_uri: str, output_file: str, 
                              format: str = 'csv') -> bool:
        """
        Export all data from an experiment to a file.
        
        Args:
            experiment_uri: URI of the experiment
            output_file: Path to output file
            format: Output format ('csv' or 'json')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all data
            print(f"Fetching data for experiment {experiment_uri}...")
            data = self.client.get_all_pages(
                'get_data',
                experiment_uri=experiment_uri
            )
            
            if not data:
                print("No data found")
                return False
            
            print(f"Found {len(data)} data points")
            
            if format == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(output_file, index=False)
            elif format == 'json':
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                print(f"Unsupported format: {format}")
                return False
            
            print(f"Data exported to {output_file}")
            return True
            
        except Exception as e:
            print(f"Export error: {str(e)}")
            return False


class AsyncOpenSilexClient:
    """
    Asynchronous client for faster parallel operations.
    """
    
    def __init__(self, base_url: str = "http://opensilex.org/sandbox/rest",
                 username: str = "guest@opensilex.org",
                 password: str = "guest"):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
    
    async def authenticate(self, session: aiohttp.ClientSession) -> bool:
        """Authenticate and get token asynchronously."""
        auth_data = {
            "identifier": self.username,
            "password": self.password
        }
        
        async with session.post(
            f"{self.base_url}/security/authenticate",
            json=auth_data
        ) as response:
            if response.status == 200:
                result = await response.json()
                self.token = result["result"]["token"]
                return True
            return False
    
    async def fetch_data_async(self, session: aiohttp.ClientSession, 
                              endpoint: str, params: Dict) -> Optional[Dict]:
        """Fetch data asynchronously."""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        async with session.get(
            f"{self.base_url}{endpoint}",
            headers=headers,
            params=params
        ) as response:
            if response.status == 200:
                return await response.json()
            return None
    
    async def get_multiple_experiments_data(self, experiment_uris: List[str]) -> Dict[str, List[Dict]]:
        """
        Get data for multiple experiments in parallel.
        
        Args:
            experiment_uris: List of experiment URIs
            
        Returns:
            Dictionary mapping experiment URI to its data
        """
        async with aiohttp.ClientSession() as session:
            # Authenticate first
            if not await self.authenticate(session):
                return {}
            
            # Create tasks for each experiment
            tasks = []
            for uri in experiment_uris:
                params = {"experiment": uri, "page_size": 1000}
                task = self.fetch_data_async(session, "/core/data", params)
                tasks.append(task)
            
            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks)
            
            # Map results to experiment URIs
            data_by_experiment = {}
            for uri, result in zip(experiment_uris, results):
                if result:
                    data_by_experiment[uri] = result.get("result", [])
                else:
                    data_by_experiment[uri] = []
            
            return data_by_experiment


# === Example Usage Functions ===

def example_data_analysis():
    """Example of data analysis with OpenSilex data."""
    from opensilex_client import OpenSilexClient  # Import your main client
    
    client = OpenSilexClient()
    if not client.authenticate():
        print("Authentication failed!")
        return
    
    analyzer = OpenSilexDataAnalyzer(client)
    
    # Get first experiment
    experiments = client.get_experiments(page_size=1)
    if not experiments:
        print("No experiments found")
        return
    
    experiment_uri = experiments[0]['uri']
    
    # Get experiment summary
    print("=== Experiment Summary ===")
    summary = analyzer.get_experiment_summary(experiment_uri)
    print(f"Experiment: {summary['name']}")
    print(f"Data points: {summary['data_points']}")
    print(f"Date range: {summary['date_range']}")
    print(f"Scientific objects: {summary['scientific_objects']}")
    print(f"Variables measured: {len(summary['variables'])}")
    
    # Plot time series if data available
    if summary['variables']:
        first_variable = list(summary['variables'].keys())[0]
        print(f"\nPlotting time series for {first_variable}")
        analyzer.plot_time_series(experiment_uri, first_variable)


def example_batch_operations():
    """Example of batch operations."""
    from opensilex_client import OpenSilexClient
    
    client = OpenSilexClient()
    if not client.authenticate():
        print("Authentication failed!")
        return
    
    processor = OpenSilexBatchProcessor(client)
    
    # Example: Export experiment data
    experiments = client.get_experiments(page_size=1)
    if experiments:
        experiment_uri = experiments[0]['uri']
        processor.export_experiment_data(
            experiment_uri,
            "experiment_data.csv",
            format='csv'
        )
    
    # Example: Batch upload (commented out to avoid accidental uploads)
    # mapping = {
    #     'date': 'date',
    #     'measurement': 'value',
    #     'plant_id': 'scientific_object',
    #     'variable_type': 'variable'
    # }
    # success, errors = processor.batch_upload_data('data_to_upload.csv', mapping)
    # print(f"Uploaded {success} records, {len(errors)} errors")


async def example_async_operations():
    """Example of asynchronous operations for better performance."""
    async_client = AsyncOpenSilexClient()
    
    # Get multiple experiments' data in parallel
    experiment_uris = [
        "http://www.phenome-fppn.fr/m3p/ARCH2017-03-30",
        "http://www.phenome-fppn.fr/m3p/ARCH2016-02-01"
    ]
    
    data = await async_client.get_multiple_experiments_data(experiment_uris)
    
    for uri, exp_data in data.items():
        print(f"\nExperiment {uri}: {len(exp_data)} data points")


if __name__ == "__main__":
    # Run examples
    print("=== Data Analysis Example ===")
    example_data_analysis()
    
    print("\n\n=== Batch Operations Example ===")
    example_batch_operations()
    
    # Run async example
    print("\n\n=== Async Operations Example ===")
    asyncio.run(example_async_operations())