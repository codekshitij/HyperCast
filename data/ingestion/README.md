## Data Ingestion

Phase 0 target: fetch historical and live datasets (e.g., NOAA GFS) into object storage.

- Start with a small geographic window and limited variables to validate the pipeline.
- Produce Parquet/Zarr locally; plan to move to S3/GCS later.
