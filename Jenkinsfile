pipeline {
    agent any

    environment {
        IMAGE_NAME = "fullstack-sqlite"
        CONTAINER_NAME = "test-sqlite"
        DATA_DIR = "data"
        HOST_PATH = "${WORKSPACE}/data"
        CONTAINER_PATH = "/app/data"
        PORT = "5000"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
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

        stage('Prepare Data Directory') {
            steps {
                bat """
                if not exist %DATA_DIR% mkdir %DATA_DIR%
                icacls %DATA_DIR% /grant Everyone:(OI)(CI)F /T
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
                docker run -d -p %PORT%:5000 --name %CONTAINER_NAME% -v %HOST_PATH%:%CONTAINER_PATH% %IMAGE_NAME%
                """
            }
        }

        stage('Verify') {
            steps {
                bat "docker ps"
                bat "dir %DATA_DIR%"
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully. Access your app at http://localhost:5000"
        }
        failure {
            echo "❌ Pipeline FAILED. Check logs above."
        }
    }
}
