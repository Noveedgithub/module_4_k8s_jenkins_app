pipeline {
    agent any

    environment {
        KUBECONFIG_FILE = 'Kubeconfig' 
    }

    stages {
        stage("Cleanup") {
            steps {
                sh 'docker rm -f $(docker ps -a -q --filter "label=app=noveedwork") || true'
                sh 'docker rmi -f $(docker images -q --filter "label=app=noveedwork") || true'
            }
        }
        stage("Build Docker Image") {
            steps {
                sh 'docker build -t noveedwork/activity4:app .'
            }
        }

        stage("Push Image to Docker Hub") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
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
            } 
        }
    }
}
