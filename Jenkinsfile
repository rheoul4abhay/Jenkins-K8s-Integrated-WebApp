pipeline {
    agent {
        label 'docker-node'
    }

    environment {
        DOCKERHUB_USERNAME = 'abhayshrivastava'
        DOCKERHUB_PASS = credentials('dockerhub-creds')
    }

    stages {
        stage('Build Frontend') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_PASS) {
                        sh '''
                        cd frontend
                        docker build -t $DOCKERHUB_USERNAME/jk-frontend-app .
                        docker push $DOCKERHUB_USERNAME/jk-frontend-app
                        '''
                    }
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_PASS) {
                        sh '''
                        cd backend
                        docker build -t $DOCKERHUB_USERNAME/jk-backend-app .
                        docker push $DOCKERHUB_USERNAME/jk-backend-app
                        '''
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@98.90.132.130 << EOF
                kubectl apply -f ~/Jenkins-K8s-Integrated-WebApp/K8s/
                EOF
                '''
            }
        }
    }
}
