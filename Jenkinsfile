// Declarative Jenkins pipeline — the same flow as .github/workflows/ci.yml,
// for teams running Jenkins: test -> build/push image -> update the manifest.
pipeline {
    agent any

    environment {
        IMAGE = "ghcr.io/mreshma575/cicd-demo-app"
    }

    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements-dev.txt'
                sh 'pytest -v'
            }
        }
        stage('Build & Push Image') {
            when { branch 'main' }
            steps {
                script {
                    def tag = env.GIT_COMMIT.take(7)
                    docker.build("${IMAGE}:${tag}")
                    docker.withRegistry('https://ghcr.io', 'ghcr-credentials') {
                        docker.image("${IMAGE}:${tag}").push()
                        docker.image("${IMAGE}:${tag}").push('latest')
                    }
                    env.IMAGE_TAG = tag
                }
            }
        }
        stage('Update Manifest') {
            when { branch 'main' }
            steps {
                sh """
                    sed -i "s|image: ${IMAGE}:.*|image: ${IMAGE}:${IMAGE_TAG}|" k8s/deployment.yaml
                    git config user.name "jenkins"
                    git config user.email "jenkins@ci.local"
                    git add k8s/deployment.yaml
                    git commit -m "Deploy ${IMAGE_TAG} [skip ci]" || echo "No manifest change"
                    git push origin main
                """
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed — the manifest was not updated, so the cluster keeps the last good version.'
        }
    }
}
