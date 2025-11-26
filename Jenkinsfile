pipeline {
    agent {
        label 'docker-node'
    }

    environment {
		DOCKERHUB_USERNAME = 'abhayshrivastava'
		SONARQUBE_TOKEN = credentials('sonarqube-token')
		OPENSHIFT_SERVER_URL = 'https://api.rm3.7wse.p1.openshiftapps.com:6443'
		MONITORING_SERVER_IP = '100.30.213.217'
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
			-Dsonar.host.url=http://$MONITORING_SERVER_IP:9000 \
			-Dsonar.login=$SONARQUBE_TOKEN

			cd ../frontend
			sonar-scanner \
			-Dsonar.projectKey=jk-frontend \
			-Dsonar.sources=. \
			-Dsonar.exclusions=**/node_modules/**,**/venv/**,**/tests/**,**/proc/** \
			-Dsonar.host.url=http://$MONITORING_SERVER_IP:9000 \
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
                        docker build -t $DOCKERHUB_USERNAME/jk-frontend-app:$BUILD_NUMBER .
                        docker push $DOCKERHUB_USERNAME/jk-frontend-app:$BUILD_NUMBER
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
                        docker build -t $DOCKERHUB_USERNAME/jk-backend-app:$BUILD_NUMBER .
                        docker push $DOCKERHUB_USERNAME/jk-backend-app:$BUILD_NUMBER
                        '''
                    }
                }
            }
        }
	
	stage('Package and Push Helm Chart') {
	    when {
		branch 'main'
	    }
	    steps {
		withCredentials([usernamePassword(credentialsId: 'github-login', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_PASS')]) {
		    sh '''
			git config --global user.email "abhayshrivastava830@gmail.com"
			git config --global user.name "Abhay Shrivastava"
			
			rm -rf helm-repo

			git clone --branch gh-pages https://$GITHUB_USER:$GITHUB_PASS@github.com/rheoul4abhay/my-helm-charts.git helm-repo

			cd helm-repo
			rm -f *.tgz index.yaml

			cd ..
			helm lint ./webapp-chart
			helm package ./webapp-chart --version 0.3.$BUILD_NUMBER --destination ./charts
			cp ./charts/* ./helm-repo/
			
			cd helm-repo
			helm repo index . --url https://rheoul4abhay.github.io/my-helm-charts
			git add .
			git commit -m "Updated Helm chart to version 0.3.$BUILD_NUMBER"
			git push https://$GITHUB_USER:$GITHUB_PASS@github.com/rheoul4abhay/my-helm-charts.git gh-pages
		    '''
		}
	    }
	}

        stage('Deploy to OpenShift') {
	    when {
		branch 'main'
	    }
            steps {
		withCredentials([string(credentialsId: 'openshift-token', variable: 'OPENSHIFT_TOKEN')]) {
			sh '''
			oc login --token=$OPENSHIFT_TOKEN --server=$OPENSHIFT_SERVER_URL
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

	stage('Deploy to Minikube for monitoring') {
	    when {
		branch 'main'
	    }
	    steps {
			sh '''
			sleep 45 # Wait for GitHub pages to update helm deployment
		    	ssh -i /home/jenkins/.ssh/id_rsa -o StrictHostKeyChecking=no ubuntu@$MONITORING_SERVER_IP "
		    	helm repo add jk-webapp https://rheoul4abhay.github.io/my-helm-charts && \
		    	helm repo update && \
		    	helm upgrade --install jk-webapp jk-webapp/webapp-chart \
                    	--version 0.3.$BUILD_NUMBER \
                    	--namespace production \
                    	--create-namespace \
                    	--set namespace=production \
                    	--set platform=minikube \
                    	--set image.frontend.repository=$DOCKERHUB_USERNAME/jk-frontend-app \
                    	--set image.frontend.tag=$BUILD_NUMBER \
                    	--set image.backend.repository=$DOCKERHUB_USERNAME/jk-backend-app \
                    	--set image.backend.tag=$BUILD_NUMBER
                	"
			'''
	    }
	}
    }
    post {
	success {
            withCredentials([string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK')]) {
        	sh """
        	curl -X POST -H 'Content-type: application/json' --data '{ 
		"text": "✅ Jenkins CI/CD Pipeline succeeded for branch: ${env.BRANCH_NAME}, Build #${env.BUILD_NUMBER}"
            	}' $SLACK_WEBHOOK
            	"""
            }
	}
	failure {
	    withCredentials([string(credentialsId: 'slack-webhook-url', variable: 'SLACK_WEBHOOK')]) {
                sh """
                curl -X POST -H 'Content-type: application/json' --data '{
                "text": "❌ Jenkins CI/CD Pipeline failed for branch: ${env.BRANCH_NAME}, Build #${env.BUILD_NUMBER}"
            	}' $SLACK_WEBHOOK
            	"""
            }
	}
    }
}
