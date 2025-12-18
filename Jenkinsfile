pipeline {
    agent any

    environment {
        IMAGE_NAME = "fullstack-sqlite"
        CONTAINER_NAME = "test-sqlite"
        DATA_PATH = "C:\\Users\\1016\\Downloads\\fullstack sql lite jenkins\\data"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Samhitha1705/full-stack-sqllite-jenkins.git',
                        credentialsId: 'github-fine-grained-pat'
                    ]]
                ])
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
                docker run -d --name %CONTAINER_NAME% -p 5000:5000 -v "%DATA_PATH%:/app/backend/data" %IMAGE_NAME%
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Check 'data' folder for app.db"
        }
        failure {
            echo "Pipeline FAILED. Check Jenkins logs for errors."
        }
    }
}
