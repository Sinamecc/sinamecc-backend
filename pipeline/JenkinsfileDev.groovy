pipeline {
	agent any;
	environment {
		MY_VARIABLE = "MY_VALUE"
	}

	stages {
		stage("Build and Test") {
			steps {
				echo "Step: Build and Test"
			}
		}

		stage ("Execute migrations") {
			steps {
				echo "Step: Build and Test"
			}	
		}

		stage ("Restarting service") {
			steps {
				echo "Step: Build and Test"
			}	
		}
	}
}