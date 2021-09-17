pipeline {
    agent any;
    environment {
        DJANGO_SETTINGS_MODULE = "config.settings.ecs_aws"
        DATABASE_HOST = sh (
          script: '/usr/local/bin/aws ssm get-parameters --region us-east-2 --names /stage/backend/db-url --query Parameters[0].Value --with-decryption | sed \'s/"//g\'',
          returnStdout: true
        ).trim()
        DATABASE_NAME = "sinamecc_stage"
        DATABASE_CREDS  = credentials('sinamecc-stage-dba')
        DATABASE_URL    = "postgres://${DATABASE_CREDS}@${DATABASE_HOST}:5432/${DATABASE_NAME}"

        BASE_ECR = "973157324549.dkr.ecr.us-east-2.amazonaws.com"
        ENVIRONMENT = "stage"
        APP = "sinamecc-backend"
        ECS_CLUSTER_NAME = "sinamecc-cluster-$ENVIRONMENT"
        ECS_SERVICE_NAME = "sinamecc-backend-$ENVIRONMENT"
    }

    stages {
        stage("Build and Test") {
            steps {
                withPythonEnv('/bin/python3.7') {
                  echo "Step: Upgrading pip"
                  sh 'pip install --upgrade pip'

                  echo "Step: Updating requirements"
                  sh 'pip install -r requirements.txt'

                  echo "Step: Running Migrations"
                  sh 'python manage.py migrate'
                }
            }
        }

        stage ("Building docker image") {
            steps {
                echo "Step: Cleaning up local docker"
                sh 'docker system prune -a -f'

                echo "Step: Building docker image"
                sh 'docker build -t $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT .'
            }
        }

        stage ("Pushing Images and Updating Service") {
          steps {
            echo "Step: Login ECR"
            sh '/usr/local/bin/aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $BASE_ECR/$ENVIRONMENT/$APP'

            echo "Step: Pushing base image"
            sh 'docker push $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT'

            echo "Step: Restarting ECS Service"
            sh '/usr/local/bin/aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --force-new-deployment'
          }
        }

        stage ("Waiting on Stage to be healthy") {
          steps {
            echo "Step: Waiting on Service to be healthy"
            sh '/usr/local/bin/aws ecs wait services-stable --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME'
          }
        }

        stage("Re-tagging stage images for prod") {
          environment {
            ENVIRONMENT = "prod"
            APP = "sinamecc-backend"
          }

          steps {
            echo "Step: Re-tagging base docker image for web"
            sh 'docker tag $BASE_ECR/stage/$APP:stage $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT'
          }
        }

        stage("Pushing Image to Prod and Updating Service") {
          environment {
              ENVIRONMENT = "prod"
              ECS_CLUSTER_NAME = "sinamecc-cluster-$ENVIRONMENT"
              ECS_SERVICE_NAME = "sinamecc-backend-$ENVIRONMENT"
          }
          steps {
            echo "Step: Login ECR"
            sh '/usr/local/bin/aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $BASE_ECR/$ENVIRONMENT/$APP'

            echo "Step: Pushing base image"
            sh 'docker push $BASE_ECR/$ENVIRONMENT/$APP:$ENVIRONMENT'

            echo "Step: Restarting ECS Service"
            sh '/usr/local/bin/aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --force-new-deployment'
          }
        }

        stage ("Waiting on Prod to be healthy") {
          environment {
              ENVIRONMENT = "prod"
              ECS_CLUSTER_NAME = "sinamecc-cluster-$ENVIRONMENT"
              ECS_SERVICE_NAME = "sinamecc-backend-$ENVIRONMENT"
          }
          steps {
            echo "Step: Waiting on Service to be healthy"
            sh '/usr/local/bin/aws ecs wait services-stable --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME'
          }
        }
    }
}
