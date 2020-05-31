pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.dev_aws"
        DATABASE_HOST = "sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com"
        DATABASE_NAME = "sinamecc_dev_2020"
    }

    stages {
        stage("Build and Test") {
            withCredentials([
                [$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-credentials-us-east-2', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'], 
                usernamePassword(credentialsId: 'sinamecc-dev-dba', passwordVariable: 'DATABASE_PASSWORD', usernameVariable: 'DATABASE_USER')]
                ) 
            {
                environment {
                    DATABASE_URL="postgres://${DATABASE_USER}:${DATABASE_PASSWORD}@${DATABASE_HOST}:5432/${DATABASE_NAME}"
                }
                steps {
                    withPythonEnv('/usr/bin/python3.6') {
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
                echo "Step: Stopping current container"
                sh 'test ! -z "`docker ps | grep sinamecc_backend_dev`" && (docker stop sinamecc_backend_dev && docker rm sinamecc_backend_dev) || echo "sinamecc_backend_dev does not exists"'

                echo "Step: Running new container"
                sh 'docker run -d -e "DJANGO_SETTINGS_MODULE=config.settings.dev_aws" --name sinamecc_backend_dev -p 8015:8015 sinamecc_backend:dev'
            }   
        }
    }
}
