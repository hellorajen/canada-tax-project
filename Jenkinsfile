pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'canada-tax-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/yourusername/canada-tax-project.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Example: Run Python tests
                    sh 'python -m pytest tests/'
                    
                    // Or run tests inside the container
                    // docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").inside {
                    //     sh 'python -m pytest tests/'
                    // }
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                // Add your deployment steps here
                // Example: SSH to production server and run the container
            }
        }
    }
    
    post {
        always {
            // Clean up
            sh 'docker system prune -f'
        }
        failure {
            // Notify on failure
            emailext body: 'Build failed!', subject: 'Build Failed', to: 'team@example.com'
        }
    }
}