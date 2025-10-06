pipeline {
    agent {
        label 'docker-node'
    }

    environment {
		DEPLOYMENT_SERVER_IP = '98.91.64.24'
        DOCKERHUB_USERNAME = 'abhayshrivastava'
    }

    stages {
        stage('Build Frontend') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        sh '''
                        cd frontend
                        sudo docker build -t $DOCKERHUB_USERNAME/jk-frontend-app .
                        sudo docker push $DOCKERHUB_USERNAME/jk-frontend-app
                        '''
                    }
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        sh '''
                        cd backend
                        sudo docker build -t $DOCKERHUB_USERNAME/jk-backend-app .
                        sudo docker push $DOCKERHUB_USERNAME/jk-backend-app
                        '''
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
        	ssh -i /home/jenkins/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@$DEPLOYMENT_SERVER_IP "
        	helm repo add my-webapp https://rheoul4abhay.github.io/my-helm-charts && \
        	helm repo update && \
		helm upgrade --install my-webapp ./webapp-chart \
  		--set image.frontend.repository=$DOCKERHUB_USERNAME/jk-frontend-app \
		--set image.frontend.tag=$DOCKER_TAG \
		--set image.backend.repository=$DOCKERHUB_USERNAME/jk-backend-app \
		--set image.backend.tag=$DOCKER_TAG
		"
        	'''
            }
        }
    }
}
