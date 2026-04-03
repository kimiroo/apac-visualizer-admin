#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

SRC="/app/default"
DST="/data"

echo "Initializing data..."

# 1. Check for config.json (File)
if [ ! -f "$DST/config.json" ]; then
    echo "config.json not found. Copying default..."
    cp "$SRC/config.json" "$DST/config.json"
fi

# 2. Check for country.json (File)
if [ ! -f "$DST/country.json" ]; then
    echo "country.json not found. Copying default..."
    cp "$SRC/country.json" "$DST/country.json"
fi

# 3. Check for LAST_MODIFIED in /data/geojson (Directory/File check)
# If the file doesn't exist, copy the entire directory
if [ ! -f "$DST/geojson/LAST_MODIFIED" ]; then
    echo "LAST_MODIFIED not found in $DST/geojson. Copying geojson directory..."
    # Create parent directory if it doesn't exist
    mkdir -p "$DST"
    # Copy directory (-r for recursive, -p to preserve permissions)
    cp -rp "$SRC/geojson" "$DST/"
fi

echo "Data initialization complete. Starting application..."

# Execute the main container process (PID 1)
exec "$@"