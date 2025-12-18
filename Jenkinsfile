pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'fullstack-sqlite'
        CONTAINER_NAME = 'test-sqlite'
        WORKSPACE_DATA = "${env.WORKSPACE}\\data"
        FLASK_APP = 'backend/app.py'
        FLASK_ENV = 'development'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out repo...'
                git url: 'https://github.com/Samhitha1705/full-stack-sqllite-jenkins.git', 
                    credentialsId: 'github-fine-grained-pat', branch: 'main'
            }
        }

        stage('Clean Old Container and Image') {
            steps {
                echo 'Removing old container and image if exists...'
                bat """
                docker rm -f %CONTAINER_NAME% || echo Container not found
                docker rmi %DOCKER_IMAGE% || echo Image not found
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t %DOCKER_IMAGE% ."
            }
        }

        stage('Run Container') {
            steps {
                echo 'Starting Docker container...'
                bat """
                if not exist "%WORKSPACE_DATA%" mkdir "%WORKSPACE_DATA%"
                docker ps -a | findstr %CONTAINER_NAME% 1>nul
                if %ERRORLEVEL% == 0 (
                    echo Container exists, restarting...
                    docker start %CONTAINER_NAME%
                ) else (
                    docker run -d -p 5000:5000 `
                        -e FLASK_APP=%FLASK_APP% `
                        -e FLASK_ENV=%FLASK_ENV% `
                        -v "%WORKSPACE_DATA%:/app/data" `
                        --name %CONTAINER_NAME% %DOCKER_IMAGE%
                )
                """
            }
        }

        stage('Test APIs') {
            steps {
                echo 'Running API tests...'
                bat """
                timeout /t 5
                curl -v http://localhost:5000/
                """
            }
        }

        stage('Verify SQLite DB') {
            steps {
                echo 'Checking SQLite DB...'
                bat """
                sqlite3 "%WORKSPACE_DATA%\\app.db" ".tables"
                """
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. Container is still running for persistence.'
        }
    }
}
