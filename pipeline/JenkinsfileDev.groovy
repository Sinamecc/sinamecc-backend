pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.dev_aws"
        DATABASE_HOST = "sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com"
        DATABASE_NAME = "sinamecc_dev_2020"
        DATABASE_CREDS  = credentials('sinamecc-dev-dba')
        DATABASE_URL    = "postgres://${DATABASE_CREDS}@${DATABASE_HOST}:5432/${DATABASE_NAME}"
    }

    stages {
        stage("Build and Test") {
            steps {
                withPythonEnv('/usr/bin/python3.6') {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-credentials-us-east-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
                    {
                        echo "DATABASE URL: ${DATABASE_URL}"
                        echo "Step: Updating requirements"
                        sh 'pip install -r requirements.txt'

                        echo "Step: Running Tests"
                        sh 'python manage.py test'

                        echo "Step: Running Migrations"
                        sh 'python manage.py migrate'                    
                    }
                }
            }
        }

        stage ("Building docker image") {
            steps {
                withPythonEnv('/usr/bin/python3.6') {
                    echo "Step: Building docker image"
                    sh 'docker build -t sinamecc_backend:dev .'
                }
            }   
        }

        stage ("Restarting docker container") {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-credentials-us-east-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']])
                {
                    echo "Step: Stopping current container"
                    sh 'test ! -z "`docker ps | grep sinamecc_backend_dev`" && (docker stop sinamecc_backend_dev && docker rm sinamecc_backend_dev) || echo "sinamecc_backend_dev does not exists"'

                    echo "Step: Running new container"
                    sh "docker run -d -e \"DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}\" -e \"DATABASE_URL=${DATABASE_URL}\" -e \"AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}\" -e \"AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}\" --name sinamecc_backend_dev -p 8015:8015 sinamecc_backend:dev"
                }
            }   
        }
    }
}
