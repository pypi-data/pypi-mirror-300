#!/bin/bash

# Check if Docker should be used
useDocker=false

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --useDocker) useDocker=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

if [ "$useDocker" = true ]; then
    echo "Running Docker commands..."

    # Build the Docker image
    docker build -t whiteduck .

    # Run the Docker container, remove it after execution, and map port 8000
    docker run --rm -p 8000:8000 whiteduck
else
    # Step 1: Check if Poetry is installed
    if ! command -v poetry &> /dev/null; then
        echo "Poetry is not installed. Installing Poetry..."
        pip install poetry
    else
        echo "Poetry is already installed."
    fi

    # Step 2: Install project dependencies using Poetry
    echo "Installing project dependencies using Poetry..."
    poetry install --no-root

    # Step 3: Start the app
    echo "Starting App..."
    poetry run shiny run ./app.py

    # Step 4: Keep the script open indefinitely
    echo "Press Enter to exit the script..."
    read -r
fi
