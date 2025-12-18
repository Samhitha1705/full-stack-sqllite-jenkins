pipeline {
    agent any
/////////
    environment {
        IMAGE_NAME = "fullstack-sqlite"
        CONTAINER_NAME = "test-sqlite"
        DATA_VOLUME = "C:\\fullstack-data:/app/data" // Persistent volume outside Jenkins workspace
    }

    triggers {
        // Poll Git every 5 minutes as a fallback (Webhook preferred)
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Samhitha1705/full-stack-sqlite-jenkins.git'
            }
        }

        stage('Clean Old Container and Image') {
            steps {
                bat """
                docker rm -f %CONTAINER_NAME% || echo Container not found
                docker rmi %IMAGE_NAME% || echo Image not found
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
                docker run -d -p 5000:5000 -v %DATA_VOLUME% --name %CONTAINER_NAME% %IMAGE_NAME%
                """
            }
        }

        stage('Test APIs') {
            steps {
                script {
                    // Test registration API
                    def reg = bat(script: """
                        curl -s -X POST -H "Content-Type: application/json" ^
                        -d "{\\"username\\":\\"testuser%BUILD_NUMBER%\\",\\"password\\":\\"1234\\"}" ^
                        http://localhost:5000/api/register
                    """, returnStdout: true).trim()
                    echo "Registration Response: ${reg}"

                    // Test login API
                    def login = bat(script: """
                        curl -s -X POST -H "Content-Type: application/json" ^
                        -d "{\\"username\\":\\"testuser%BUILD_NUMBER%\\",\\"password\\":\\"1234\\"}" ^
                        http://localhost:5000/api/login
                    """, returnStdout: true).trim()
                    echo "Login Response: ${login}"

                    // Test login history API
                    def history = bat(script: "curl -s http://localhost:5000/api/logins", returnStdout: true).trim()
                    echo "Login History: ${history}"
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up container..."
            bat "docker rm -f %CONTAINER_NAME% || echo Container not found"
        }
    }
}
