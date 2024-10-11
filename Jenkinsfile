pipeline {
    agent any

    environment {
        KUBECONFIG_FILE = 'kubeconfig'  // Reference the kubeconfig secret file ID
    }

    stages {
        stage("Cleanup") {
            steps {
                // Cleanup any running or stopped containers, and remove all images
                sh 'docker rm -f $(docker ps -aq) || true'
                sh 'docker rmi -f $(docker images -q) || true'
            }
        }
        stage("Build Docker Image") {
            steps {
                // Build the Docker image
                sh 'docker build -t noveedwork/activity4:app .'
            }
        }

        stage("Push Image to Docker Hub") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    // Login and push the Docker image to Docker Hub
                    sh '''
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    docker push docker.io/noveedwork/activity4:app
                    '''
                }
            }
        }

        stage("Orchestrate Containers on Kubernetes") {
            steps {
                withCredentials([file(credentialsId: "${env.KUBECONFIG_FILE}", variable: 'KUBECONFIG')]) {
                    sh '''
                    kubectl apply -f flask_deployment.yaml
                    kubectl apply -f flask_service.yaml
                    kubectl apply -f nginx_deployment.yaml
                    kubectl apply -f nginx_service.yaml
                    '''
                }
            } // Correct closing of steps block
        }
    }

    post {
        always {
            // Optionally, print the Minikube status at the end of the pipeline
            sh 'minikube status'
        }
    }
}
