#!/usr/bin/env python3
"""
GRIB2 Parser for GFS Weather Data

Extracts weather variables from GRIB2 files and converts them to structured format.
"""
import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, List
import warnings

import xarray as xr
import pandas as pd
import numpy as np

# Suppress cfgrib warnings
warnings.filterwarnings('ignore', category=UserWarning)


class GRIBParser:
    """Parse GRIB2 files and extract weather variables."""
    
    # Variable names mapping (GRIB name -> our name)
    VARIABLE_MAP = {
        't2m': 'temperature',      # 2m temperature (K)
        'r2': 'humidity',          # 2m relative humidity (%)
        'u10': 'wind_u',           # 10m U wind component (m/s)
        'v10': 'wind_v',           # 10m V wind component (m/s)
        'prmsl': 'pressure',       # Mean sea-level pressure (Pa)
        'tcc': 'clouds',           # Total cloud cover (0-1)
        'tp': 'precipitation',     # Total precipitation (m)
    }
    
    def __init__(self, target_lat: float = 33.749, target_lon: float = -84.388):
        """
        Initialize parser with target location.
        
        Args:
            target_lat: Target latitude (default: Atlanta, GA)
            target_lon: Target longitude (default: Atlanta, GA)
        """
        self.target_lat = target_lat
        self.target_lon = target_lon
        
    def parse_file(self, grib_file: Path) -> Optional[Dict]:
        """
        Parse a single GRIB2 file and extract all variables.
        
        Args:
            grib_file: Path to GRIB2 file
            
        Returns:
            Dictionary with timestamp and extracted variables, or None if failed
        """
        try:
            # Open the GRIB file using cfgrib backend
            # GFS files have multiple messages, we need to open each separately
            ds = xr.open_dataset(
                str(grib_file),
                engine='cfgrib',
                backend_kwargs={'errors': 'ignore'}
            )
            
            # Extract data point closest to target location
            data = self._extract_point(ds)
            
            if data:
                return data
                
        except Exception as e:
            print(f"Error parsing {grib_file}: {e}", file=sys.stderr)
            
        return None
    
    def _extract_point(self, ds) -> Optional[Dict]:
        """
        Extract data for the target location from xarray dataset.
        
        Args:
            ds: xarray Dataset
            
        Returns:
            Dictionary with extracted values
        """
        try:
            result = {}
            
            # Get timestamp (valid time)
            if 'valid_time' in ds.coords:
                timestamp = pd.Timestamp(ds.valid_time.values)
                result['timestamp'] = timestamp
            elif 'time' in ds.coords:
                timestamp = pd.Timestamp(ds.time.values)
                result['timestamp'] = timestamp
            
            # Try to find the closest lat/lon point
            if 'latitude' in ds.coords and 'longitude' in ds.coords:
                # Select nearest point
                point = ds.sel(
                    latitude=self.target_lat,
                    longitude=self.target_lon,
                    method='nearest'
                )
                
                # Extract each variable
                for grib_var, our_var in self.VARIABLE_MAP.items():
                    if grib_var in point.data_vars:
                        value = float(point[grib_var].values)
                        result[our_var] = value
            
            return result if len(result) > 1 else None
            
        except Exception as e:
            print(f"Error extracting point: {e}", file=sys.stderr)
            return None
    
    def parse_directory(self, grib_dir: Path) -> pd.DataFrame:
        """
        Parse all GRIB2 files in a directory and return combined DataFrame.
        
        Args:
            grib_dir: Directory containing GRIB2 files
            
        Returns:
            DataFrame with time-series weather data
        """
        grib_files = sorted(grib_dir.glob('**/*.grb2'))
        
        if not grib_files:
            print(f"No GRIB2 files found in {grib_dir}", file=sys.stderr)
            return pd.DataFrame()
        
        print(f"Found {len(grib_files)} GRIB2 files")
        
        data_list = []
        for grib_file in grib_files:
            print(f"Parsing {grib_file.name}...", end=' ')
            data = self.parse_file(grib_file)
            if data:
                data_list.append(data)
                print("✓")
            else:
                print("✗")
        
        if not data_list:
            print("No data extracted from GRIB files", file=sys.stderr)
            return pd.DataFrame()
        
        # Create DataFrame
        df = pd.DataFrame(data_list)
        
        # Sort by timestamp
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Convert temperature from Kelvin to Celsius
        if 'temperature' in df.columns:
            df['temperature'] = df['temperature'] - 273.15
        
        # Convert pressure from Pa to hPa
        if 'pressure' in df.columns:
            df['pressure'] = df['pressure'] / 100.0
        
        # Convert precipitation from m to mm
        if 'precipitation' in df.columns:
            df['precipitation'] = df['precipitation'] * 1000.0
        
        return df


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse GRIB2 files and extract weather data"
    )
    parser.add_argument(
        'input_dir',
        type=str,
        help='Directory containing GRIB2 files'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='atlanta_timeseries.parquet',
        help='Output file path (default: atlanta_timeseries.parquet)'
    )
    parser.add_argument(
        '--lat',
        type=float,
        default=33.749,
        help='Target latitude (default: 33.749 for Atlanta)'
    )
    parser.add_argument(
        '--lon',
        type=float,
        default=-84.388,
        help='Target longitude (default: -84.388 for Atlanta)'
    )
    parser.add_argument(
        '--format',
        choices=['parquet', 'csv'],
        default='parquet',
        help='Output format (default: parquet)'
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Error: {input_dir} does not exist", file=sys.stderr)
        return 1
    
    # Create parser
    parser = GRIBParser(target_lat=args.lat, target_lon=args.lon)
    
    # Parse all files
    print(f"\nExtracting data for location: {args.lat}°N, {args.lon}°W")
    df = parser.parse_directory(input_dir)
    
    if df.empty:
        print("No data extracted", file=sys.stderr)
        return 1
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.format == 'parquet':
        df.to_parquet(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)
    
    print(f"\n✓ Saved {len(df)} records to {output_path}")
    print(f"\nDataset summary:")
    print(f"  Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"  Variables: {', '.join([col for col in df.columns if col != 'timestamp'])}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

