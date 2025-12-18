pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fullstack-sqlite'
        CONTAINER_NAME = 'test-sqlite'
        PORT = '5000'
        FLASK_APP = 'backend/app.py'
        FLASK_DEBUG = '1'
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo "Checking out repository..."
                checkout scm
            }
        }

        stage('Clean Old Container & Image') {
            steps {
                bat '''
                docker rm -f %CONTAINER_NAME% 2>nul
                docker rmi %DOCKER_IMAGE% 2>nul
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }

        stage('Run Container') {
            steps {
                echo "Running Docker container..."

                bat '''
                if not exist "%WORKSPACE%\\data" mkdir "%WORKSPACE%\\data"

                docker run -d ^
                  -p %PORT%:%PORT% ^
                  -e FLASK_APP=%FLASK_APP% ^
                  -e FLASK_DEBUG=%FLASK_DEBUG% ^
                  -v "%WORKSPACE%\\data:/app/data" ^
                  --name %CONTAINER_NAME% ^
                  %DOCKER_IMAGE%
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully"
        }
        failure {
            echo "❌ Pipeline failed – check logs"
        }
    }
}
