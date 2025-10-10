pipeline {
    agent {
        label 'docker-node'
    }

    environment {
		DEPLOYMENT_SERVER_IP = '98.84.80.42'
        DOCKERHUB_USERNAME = 'abhayshrivastava'
	SONARQUBE_TOKEN = credentials('sonarqube-token')
    }

    stages {
	stage('Code Analysis') {
	    steps {
		withSonarQubeEnv('SonarQube') {
		    sh """
			cd backend
			sonar-scanner \
              		-Dsonar.projectKey=jk-backend \
              		-Dsonar.sources=. \
                	-Dsonar.exclusions=**/node_modules/**,**/venv/**,**/tests/**,**/proc/** \
              		-Dsonar.host.url=http://$DEPLOYMENT_SERVER_IP:9000 \
              		-Dsonar.login=$SONARQUBE_TOKEN

            		cd ../frontend
            		sonar-scanner \
              		-Dsonar.projectKey=jk-frontend \
              		-Dsonar.sources=. \
                	-Dsonar.exclusions=**/node_modules/**,**/venv/**,**/tests/**,**/proc/** \
              		-Dsonar.host.url=http://$DEPLOYMENT_SERVER_IP:9000 \
              		-Dsonar.login=$SONARQUBE_TOKEN
		    """
		}
	    }
	}
        stage('Build Frontend') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-creds') {
                        sh '''
                        cd frontend
                        sudo docker build -t $DOCKERHUB_USERNAME/jk-frontend-app:$BUILD_NUMBER .
                        sudo docker push $DOCKERHUB_USERNAME/jk-frontend-app:$BUILD_NUMBER
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
                        sudo docker build -t $DOCKERHUB_USERNAME/jk-backend-app:$BUILD_NUMBER .
                        sudo docker push $DOCKERHUB_USERNAME/jk-backend-app:$BUILD_NUMBER
                        '''
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
	    when {
		branch 'main'
	    }
            steps {
                sh '''
        	ssh -i /home/jenkins/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@$DEPLOYMENT_SERVER_IP "
                helm repo add jk-webapp https://rheoul4abhay.github.io/my-helm-charts && \
                helm repo update && \
                helm upgrade --install jk-webapp jk-webapp/webapp-chart \
		--set image.frontend.repository=$DOCKERHUB_USERNAME/jk-frontend-app \
		--set image.frontend.tag=$BUILD_NUMBER \
		--set image.backend.repository=$DOCKERHUB_USERNAME/jk-backend-app \
		--set image.backend.tag=$BUILD_NUMBER
		"
        	'''
            }
        }
    }
}
