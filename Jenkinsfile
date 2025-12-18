pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fullstack-sqlite'
        CONTAINER_NAME = 'test-sqlite'
        DATA_DIR = "${env.WORKSPACE}\\data"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out repo..."
                git(
                    url: 'https://github.com/Samhitha1705/full-stack-sqllite-jenkins.git',
                    branch: 'main',
                    credentialsId: 'github-fine-grained-pat'
                )
            }
        }

        stage('Clean Old Image') {
            steps {
                echo "Removing old image if exists..."
                bat "docker rmi %IMAGE_NAME% || echo Image not found"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run Container') {
            steps {
                echo "Starting container..."
                bat """
                if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
                docker ps -a | findstr %CONTAINER_NAME% >nul
                if %errorlevel%==0 (
                    echo Container already exists, restarting...
                    docker start %CONTAINER_NAME%
                ) else (
                    docker run -d -p 5000:5000 -v "%DATA_DIR%:/app/data" --name %CONTAINER_NAME% %IMAGE_NAME%
                )
                """
            }
        }

        stage('Test APIs') {
            steps {
                echo "Running API tests..."
                bat "curl http://localhost:5000/"
                // Add more curl or Python requests for additional endpoints
            }
        }

        stage('Verify SQLite DB') {
            steps {
                echo "Checking SQLite database..."
                bat """
                if exist "%DATA_DIR%\\app.db" (
                    echo app.db exists
                    sqlite3 "%DATA_DIR%\\app.db" "SELECT name FROM sqlite_master WHERE type='table';"
                ) else (
                    echo ERROR: app.db not found!
                    exit /b 1
                )
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Container is still running for persistence."
            // Container removal skipped to persist DB
            // bat "docker rm -f %CONTAINER_NAME% || echo Container not found"
        }
    }
}
