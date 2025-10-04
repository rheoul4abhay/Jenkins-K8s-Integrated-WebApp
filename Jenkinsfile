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
        	scp -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no -r K8s ubuntu@98.90.132.130:~/Jenkins-K8s-Integrated-WebApp/
        	ssh -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@98.90.132.130 '
        	kubectl apply -f ~/Jenkins-K8s-Integrated-WebApp/K8s/
     		'''

            }
        }
    }
}
