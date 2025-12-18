pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fullstack-sqlite'
        CONTAINER_NAME = 'test-sqlite'
        WORKSPACE_PATH = "${env.WORKSPACE}"
        DATA_PATH = "${WORKSPACE_PATH}\\data"
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out repo...'
                git branch: 'main',
                    url: 'https://github.com/Samhitha1705/full-stack-sqllite-jenkins.git',
                    credentialsId: 'github-fine-grained-pat'
            }
        }

        stage('Clean Old Container and Image') {
            steps {
                echo 'Removing old container and image if exists...'
                bat """
                docker rm -f %CONTAINER_NAME% || echo Container not found
                docker rmi %IMAGE_NAME% || echo Image not found
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat """
                docker build -t %IMAGE_NAME% .
                """
            }
        }

        stage('Run Container') {
            steps {
                echo 'Starting Docker container...'
                bat """
                if not exist "%DATA_PATH%" mkdir "%DATA_PATH%"

                docker ps -a | findstr %CONTAINER_NAME% 1>nul
                if %ERRORLEVEL% == 0 (
                    echo Container exists, restarting...
                    docker start %CONTAINER_NAME%
                ) else (
                    docker run -d -p 5000:5000 -e FLASK_APP=backend/app.py -e FLASK_ENV=development -v "%DATA_PATH%:/app/data" --name %CONTAINER_NAME% %IMAGE_NAME%
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
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
