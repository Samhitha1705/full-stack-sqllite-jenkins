pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Clean Old Container & Image') {
            steps {
                bat '''
                docker rm -f test-sqlite 2>nul
                docker rmi fullstack-sqlite 2>nul
                '''
            }
        }

        stage('Prepare Data Directory') {
            steps {
                bat '''
                if not exist data mkdir data
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                docker build -t fullstack-sqlite .
                '''
            }
        }

        stage('Run Container') {
            steps {
                bat '''
                docker run -d ^
                  --name test-sqlite ^
                  -p 5000:5000 ^
                  -v %cd%\\data:/app/data ^
                  fullstack-sqlite
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline SUCCESS'
        }
        failure {
            echo '❌ Pipeline FAILED'
        }
    }
}
