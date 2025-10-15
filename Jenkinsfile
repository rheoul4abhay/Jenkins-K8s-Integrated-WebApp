pipeline {
    agent {
        label 'docker-node'
    }

    environment {
		DEPLOYMENT_SERVER_IP = '44.213.155.233'
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

        stage('Deploy to OpenShift') {
	    when {
		branch 'main'
	    }
            steps {
		withCredentials([string(credentialsId: 'openshift-token', variable: 'OPENSHIFT_TOKEN')])
                sh '''
			oc login --token=$OPENSHIFT_TOKEN --server=https://api.rm2.thpm.p1.openshiftapps.com:6443 --insecure-skip-tls-verify=true
			helm upgrade --install jk-webapp ./webapp-chart \
			--set platform=openshift \
  			--set image.frontend.repository=$DOCKERHUB_USERNAME/jk-frontend-app \
			--set image.frontend.tag=$BUILD_NUMBER \
			--set image.backend.repository=$DOCKERHUB_USERNAME/jk-backend-app \
			--set image.backend.tag=$BUILD_NUMBER
        	'''
            }
        }
    }
}
