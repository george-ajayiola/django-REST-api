# DevSecOps and GitOps Documentation for Django CI/CD Pipeline

## Overview
This documentation outlines the DevSecOps and GitOps process for automating the deployment of a Django application using a CI/CD pipeline hosted on GitHub Actions. The pipeline includes code quality checks, vulnerability scanning, Docker image building, and automated updates to Kubernetes manifests. 

The CI/CD pipeline is divided into three main jobs:
1. **Checkout and Scan Code**: Code analysis using SonarQube.
2. **Build and Scan Docker Image**: Build a Docker image, scan it for vulnerabilities using Trivy, and push the image to Docker Hub.
3. **Modify Image Tag in Kubernetes Repository**: Update the image tag in a Kubernetes manifest using GitOps practices.

The following sections provide a detailed walk-through of each job in the pipeline.

---

## Prerequisites
- **GitHub Repository**: A repository containing your Django application code.
- **SonarQube**: A SonarQube server for static code analysis.
- **Docker Hub Account**: To store Docker images.
- **Kubernetes Repository**: A separate repository for Kubernetes manifests.
- **Secrets**: Store these as GitHub secrets:
  - `SONAR_TOKEN`: SonarQube token.
  - `SONAR_HOST_URL`: URL of the SonarQube server.
  - `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`: Docker Hub credentials.
  - `GIT_USERNAME`, `GIT_EMAIL`, and `GIT_TOKEN`: Credentials for accessing the Kubernetes repository.

---

## Job 1: Checkout and Scan Code
This job focuses on retrieving the source code and performing static code analysis using SonarQube.

- **Checkout Code**: Uses the `actions/checkout@v4` action to retrieve the latest code from the repository.
- **SonarQube Scan**: Integrates with SonarQube to analyze the codebase. The scan uses a SonarQube project key (`Django-CRUD-app`) and uploads results to the SonarQube server specified by `SONAR_HOST_URL`.
- **Quality Gate Check**: Verifies that the code meets the quality gate thresholds defined in SonarQube, ensuring that any critical issues are addressed before proceeding.

### Example SonarQube Scan Configuration:
```yaml
      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        with:
          projectBaseDir: .
          args: >
            -Dsonar.projectKey=Django-CRUD-app
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
