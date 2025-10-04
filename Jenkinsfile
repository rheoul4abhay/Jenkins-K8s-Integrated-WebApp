properties([
    pipelineTriggers([
        githubPush()
    ])
])
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
	  sh '''
	  cd frontend
	  sudo docker build -t $DOCKERHUB_USERNAME/jk-frontend-app .
	  sudo docker push $DOCKERHUB_USERNAME/jk-frontend-app
	  '''
	}
      }

      stage('Build Backend') {
	steps {
	  sh '''
	  cd backend
	  sudo docker build -t $DOCKERHUB_USERNAME/jk-backend-app .
	  sudo docker push $DOCKERHUB_USERNAME/jk-backend-app
	  '''
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
