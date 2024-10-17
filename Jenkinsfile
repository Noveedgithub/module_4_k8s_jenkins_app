pipeline {
    agent any

    environment {
        KUBECONFIG_FILE = 'kubeconfig' 
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
                sh 'docker build -t noveedwork/activity4:app -f flask/Dockerfile .'
                sh 'docker build -t noveedwork/activity4:appv2 -f flask_2/Dockerfile .'
            }
        }
        stage("Run Tests") {
            steps {
                sh '''
                docker run --rm -v $(pwd)/flask:/app noveedwork/activity4:app bash -c "
                cd /app && python -m unittest discover -s . -p 'test_app.py'"
                '''
            }
        }
        stage("Push Image to Docker Hub") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    docker push docker.io/noveedwork/activity4:app
                    docker push docker.io/noveedwork/activity4:appv2
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
