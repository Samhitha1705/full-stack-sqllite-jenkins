pipeline {
    agent any

    environment {
        IMAGE_NAME = "fullstack-sqlite"
        CONTAINER_NAME = "test-sqlite"
        DATA_DIR = "${WORKSPACE}/data"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out repository..."
                checkout scm
            }
        }

        stage('Prepare Data Directory') {
            steps {
                echo "Creating data directory if it does not exist..."
                bat "if not exist \"${DATA_DIR}\" mkdir \"${DATA_DIR}\""
            }
        }

        stage('Clean Old Container & Image') {
            steps {
                echo "Removing old container and image if exist..."
                bat """
                    docker rm -f ${CONTAINER_NAME} 2>nul || echo "No old container"
                    docker rmi ${IMAGE_NAME} 2>nul || echo "No old image"
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Container') {
            steps {
                echo "Running container..."
                bat """
                    docker run -d --name ${CONTAINER_NAME} -p 5000:5000 -v \"${DATA_DIR}:/app/data\" ${IMAGE_NAME}
                """
            }
        }

        stage('Verify Container') {
            steps {
                echo "Checking running containers..."
                bat "docker ps"
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS! App should be running at http://localhost:5000"
        }
        failure {
            echo "Pipeline FAILED! Check logs for errors."
        }
    }
}
