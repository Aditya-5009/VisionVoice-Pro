#!/bin/bash
# VisionVoice Pro - Build & Run Script
# Author: Aditya Menon (RA2311026050050)
# Course: SEAI (21CSE312P) - SRM IST Tiruchirappalli

IMAGE_NAME="visionvoice-pro"
DOCKERHUB_USER="adityamenon17"

case "${1:-all}" in
    build)
        echo "Building Docker image..."
        docker build -t ${IMAGE_NAME} .
        ;;
    run)
        echo "Running container on port 8501..."
        docker rm -f visionvoice-app 2>/dev/null
        docker run -d -p 8501:8501 --name visionvoice-app ${IMAGE_NAME}
        echo "Open: http://localhost:8501"
        ;;
    push)
        echo "Pushing to Docker Hub..."
        docker tag ${IMAGE_NAME} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
        ;;
    stop)
        echo "Stopping container..."
        docker rm -f visionvoice-app
        ;;
    all)
        docker build -t ${IMAGE_NAME} .
        docker rm -f visionvoice-app 2>/dev/null
        docker run -d -p 8501:8501 --name visionvoice-app ${IMAGE_NAME}
        echo "Done! Open: http://localhost:8501"
        ;;
    *)
        echo "Usage: $0 {build|run|push|stop|all}"
        exit 1
        ;;
esac