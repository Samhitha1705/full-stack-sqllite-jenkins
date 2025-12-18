pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fullstack-sqlite'
        CONTAINER_NAME = 'test-sqlite'
        DATA_VOLUME = "${WORKSPACE}/data:/app/data"
        FLASK_APP = 'backend/app.py'
        FLASK_ENV = 'development'
        PORT = '5000'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "Checking out repo..."
                checkout scm
            }
        }

        stage('Clean Old Container and Image') {
            steps {
                echo "Removing old container and image if exists..."
                bat """
                    docker rm -f %CONTAINER_NAME% || echo Container not found
                    docker rmi %DOCKER_IMAGE% || echo Image not found
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t %DOCKER_IMAGE% ."
            }
        }

        stage('Run Container') {
            steps {
                echo "Starting Docker container..."
                bat """
                    if not exist "%WORKSPACE%\\data" mkdir "%WORKSPACE%\\data"
                    
                    docker ps -a | findstr %CONTAINER_NAME% > nul
                    if %ERRORLEVEL% == 0 (
                        echo Container exists, restarting...
                        docker start %CONTAINER_NAME%
                    ) else (
                        docker run -d -p %PORT%:%PORT% -e FLASK_APP=%FLASK_APP% -e FLASK_ENV=%FLASK_ENV% -v "%DATA_VOLUME%" --name %CONTAINER_NAME% %DOCKER_IMAGE%
                    )
                """
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
