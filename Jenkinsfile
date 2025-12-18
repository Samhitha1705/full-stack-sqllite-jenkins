pipeline {
    agent any

    environment {
        // Docker image name
        IMAGE_NAME = 'fullstack-sqlite'
        CONTAINER_NAME = 'test-sqlite'
        DATA_DIR = "${env.WORKSPACE}\\data"  // Maps to container /app/data
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

        stage('Clean Old Container and Image') {
            steps {
                echo "Removing old container and image if exists..."
                bat "docker rm -f %CONTAINER_NAME% || echo Container not found"
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
                echo "Running Docker container..."
                // Creates data folder if not exists
                bat """
                if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
                docker run -d -p 5000:5000 -v "%DATA_DIR%:/app/data" --name %CONTAINER_NAME% %IMAGE_NAME%
                """
            }
        }

        stage('Test APIs') {
            steps {
                echo "Placeholder: Add your API test scripts here"
                // Example: call curl or Python test script
                // bat "curl http://localhost:5000/test"
            }
        }
    }

    post {
        always {
            echo "Cleaning up container after pipeline..."
            bat "docker rm -f %CONTAINER_NAME% || echo Container not found"
        }
    }
}
