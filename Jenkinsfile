pipeline {
    agent any
/////////////
    environment {
        IMAGE_NAME = "fullstack-sqlite"
        CONTAINER_NAME = "test-sqlite"
        HOST_DATA_DIR = "C:\\Users\\1016\\Downloads\\fullstack sql lite jenkins\\data"
        CONTAINER_DATA_DIR = "/app/data"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Clean Old Container & Image') {
            steps {
                bat """
                docker rm -f %CONTAINER_NAME% 2>nul
                docker rmi %IMAGE_NAME% 2>nul
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run Container') {
            steps {
                bat """
                docker run -d -p 5000:5000 --name %CONTAINER_NAME% -v "%HOST_DATA_DIR%:%CONTAINER_DATA_DIR%" %IMAGE_NAME%
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Check your container and database!"
        }
    }
}
