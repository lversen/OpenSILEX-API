#!/usr/bin/env python3
"""
Practical example of using OpenSilex client with SSH config
This example shows a real-world workflow for data analysis
"""

import logging
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path

# Import the OpenSilex client
from opensilex_client import OpenSilexClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main workflow example."""
    
    # ====== 1. Initialize Client ======
    # The client will automatically check SSH config for VM IP
    # It looks for hosts named: 'opensilex', 'opensilex-vm', 'opensilex-dev', 'vm'
    
    logger.info("Initializing OpenSilex client...")
    
    # Option 1: Auto-detect from SSH config
    client = OpenSilexClient()
    
    # Option 2: Specify SSH host explicitly
    # client = OpenSilexClient.from_ssh_config(ssh_host="my-opensilex-vm")
    
    # Option 3: Override with custom credentials if needed
    # client = OpenSilexClient(
    #     ssh_host="opensilex-vm",
    #     username="myuser@opensilex.org",
    #     password="mypassword"
    # )
    
    logger.info(f"Using OpenSilex at: {client.base_url}")
    
    # ====== 2. Authenticate ======
    if not client.authenticate():
        logger.error("Authentication failed! Check your credentials and VM status.")
        return
    
    logger.info("Authentication successful!")
    
    # ====== 3. Explore Available Data ======
    
    # Get experiments
    logger.info("\nFetching experiments...")
    experiments = client.get_experiments(page_size=10)
    
    if not experiments:
        logger.warning("No experiments found!")
        return
    
    print(f"\nFound {len(experiments)} experiments:")
    for exp in experiments[:5]:  # Show first 5
        print(f"  - {exp['name']} (URI: {exp['uri']})")
    
    # Select first experiment for demo
    selected_exp = experiments[0]
    exp_uri = selected_exp['uri']
    logger.info(f"\nWorking with experiment: {selected_exp['name']}")
    
    # ====== 4. Get Experiment Details ======
    
    # Get variables measured in this experiment
    logger.info("Fetching variables...")
    variables = client.get_variables(page_size=50)
    
    if variables:
        print(f"\nAvailable variables ({len(variables)} total):")
        for var in variables[:10]:  # Show first 10
            print(f"  - {var.get('name', 'Unknown')} ({var.get('uri', '')})")
    
    # Get scientific objects (plants, plots, etc.)
    logger.info("Fetching scientific objects...")
    objects = client.get_scientific_objects(
        experiment_uri=exp_uri,
        page_size=20
    )
    
    if objects:
        object_types = {}
        for obj in objects:
            obj_type = obj.get('rdf_type', 'Unknown').split('/')[-1]
            object_types[obj_type] = object_types.get(obj_type, 0) + 1
        
        print(f"\nScientific objects in experiment:")
        for obj_type, count in object_types.items():
            print(f"  - {obj_type}: {count}")
    
    # ====== 5. Retrieve and Analyze Data ======
    
    logger.info("\nFetching measurement data...")
    
    # Get data for the experiment
    data = client.get_data(
        experiment_uri=exp_uri,
        page_size=100  # Get first 100 data points as example
    )
    
    if not data:
        logger.warning("No data found for this experiment!")
        return
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(data)
    
    # Parse dates
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
    
    print(f"\nData summary:")
    print(f"  - Total measurements: {len(df)}")
    
    if 'date' in df.columns:
        print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
    
    if 'variable' in df.columns:
        print(f"  - Variables measured: {df['variable'].nunique()}")
        print("\n  Variable counts:")
        for var, count in df['variable'].value_counts().head(5).items():
            var_name = var.split('/')[-1]  # Extract name from URI
            print(f"    - {var_name}: {count} measurements")
    
    # ====== 6. Data Visualization ======
    
    # Create a simple time series plot if we have suitable data
    if 'date' in df.columns and 'value' in df.columns and 'variable' in df.columns:
        # Select first variable with numeric data
        numeric_vars = df[pd.to_numeric(df['value'], errors='coerce').notna()]['variable'].unique()
        
        if len(numeric_vars) > 0:
            selected_var = numeric_vars[0]
            var_data = df[df['variable'] == selected_var].copy()
            var_data['value'] = pd.to_numeric(var_data['value'])
            
            # Create plot
            plt.figure(figsize=(12, 6))
            
            # If we have multiple objects, plot them separately
            if 'scientific_object' in var_data.columns:
                for obj in var_data['scientific_object'].unique()[:5]:  # Limit to 5 objects
                    obj_data = var_data[var_data['scientific_object'] == obj]
                    obj_name = obj.split('/')[-1]
                    plt.plot(obj_data['date'], obj_data['value'], 
                            marker='o', label=obj_name, alpha=0.7)
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            else:
                plt.plot(var_data['date'], var_data['value'], marker='o')
            
            plt.title(f"Time Series: {selected_var.split('/')[-1]}")
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save plot
            output_dir = Path("opensilex_outputs")
            output_dir.mkdir(exist_ok=True)
            plot_file = output_dir / f"timeseries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(plot_file)
            logger.info(f"Plot saved to: {plot_file}")
            plt.close()
    
    # ====== 7. Export Data ======
    
    # Export to CSV for further analysis
    output_file = Path("opensilex_outputs") / f"experiment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Data exported to: {output_file}")
    
    # ====== 8. Summary Report ======
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
    print(f"Experiment: {selected_exp['name']}")
    print(f"Total data points analyzed: {len(df)}")
    print(f"Output files saved in: ./opensilex_outputs/")
    print("\nNext steps:")
    print("1. Review the exported CSV for detailed analysis")
    print("2. Check the time series plot for data trends")
    print("3. Use the data for statistical analysis or modeling")


def check_ssh_config():
    """Helper function to check SSH configuration."""
    from opensilex_client import SSHConfigParser
    
    print("\n=== SSH Configuration Check ===")
    
    config = SSHConfigParser.parse_ssh_config()
    
    if not config:
        print("No SSH config found at ~/.ssh/config")
        print("\nTo set up SSH config for OpenSilex:")
        print("1. Create/edit ~/.ssh/config")
        print("2. Add:")
        print("   Host opensilex-vm")
        print("   HostName YOUR_VM_IP")
        print("   User YOUR_USERNAME")
        return
    
    print("Found SSH hosts:")
    for host in config:
        if 'hostname' in config[host]:
            print(f"  - {host}: {config[host]['hostname']}")
    
    # Check for OpenSilex-related hosts
    opensilex_hosts = [h for h in config if 'opensilex' in h.lower() or h == 'vm']
    if opensilex_hosts:
        print(f"\nPotential OpenSilex hosts: {opensilex_hosts}")
    else:
        print("\nNo OpenSilex-related hosts found. Consider adding one.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--check-ssh":
        check_ssh_config()
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        except Exception as e:
            logger.error(f"Error: {str(e)}", exc_info=True)