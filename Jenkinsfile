pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'your-dockerhub/canada-tax-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        K8S_NAMESPACE = 'tax-app'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/Canada-Tax-Project.git'
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
                sh 'python -m pytest tests/'  // Add your tests
            }
        }
        stage('Push to Registry') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                 sh """
                 kubectl apply -f k8s/deployment.yaml
                  kubectl apply -f k8s/service.yaml
                  """
            }
        }
    }
}