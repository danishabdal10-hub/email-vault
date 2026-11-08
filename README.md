# Email Vault

A containerized email collection application built with Python, Flask, MongoDB, Docker, Kubernetes, and GitHub Actions.

Email Vault provides a simple web interface where users can submit email addresses. The application stores submitted addresses in MongoDB, prevents duplicate entries, and displays saved addresses.

## Features

- Collect and store email addresses.
- Normalize email addresses before storage.
- Prevent duplicate entries using MongoDB unique indexing.
- Store submission timestamps in UTC.
- Display saved email addresses.
- Health-check endpoint for application and database connectivity.
- Persistent MongoDB storage.
- Automated testing and Docker image publishing.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| MongoDB | Database |
| Docker | Containerization |
| Docker Compose | Local multi-container environment |
| Kubernetes | Container orchestration |
| GitHub Actions | CI/CD automation |
| Pytest | Automated testing |
| Ruff | Python linting |

## Project Structure

```text
email-vault/
├── .github/
│   └── workflows/
│       └── ci.yml
├── k8s/
│   ├── email-vault-config.yaml
│   ├── email-vault.yaml
│   ├── host-pv.yaml
│   ├── host-pvc.yaml
│   └── mongodb.yaml
├── static/
│   └── styles.css
├── templates/
│   └── index.html
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
└── .gitignore
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/danishabdal10-hub/email-vault.git
cd email-vault
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

Make sure MongoDB is running locally.

```bash
export MONGO_URI="mongodb://localhost:27017/"
```

### 5. Start the application

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## Run with Docker Compose

Create the persistent volume:

```bash
docker volume create email-vault-mongo-data
```

Build and start the services:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f app
```

Stop the services:

```bash
docker compose down
```

## Kubernetes Deployment

The project includes Kubernetes manifests for:

- Flask application Deployment and NodePort Service.
- MongoDB Deployment and ClusterIP Service.
- ConfigMap for database configuration.
- PersistentVolume and PersistentVolumeClaim.

Apply the manifests:

```bash
kubectl apply -f k8s/host-pv.yaml
kubectl apply -f k8s/host-pvc.yaml
kubectl apply -f k8s/email-vault-config.yaml
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/email-vault.yaml
```

Check resources:

```bash
kubectl get pods
kubectl get services
kubectl get pv,pvc
```

Access the application through the Minikube IP and configured NodePort:

```text
http://MINIKUBE-IP:30080
```

## CI/CD Pipeline

GitHub Actions automates testing and Docker image publishing.

The workflow triggers on pushes and pull requests targeting `main`.

### Test Job

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies.
4. Runs automated tests using Pytest.
5. Builds the Docker image.

### Publish Job

After successful testing, pushes to `main` trigger the publishing job.

1. Authenticates with Docker Hub.
2. Builds the application image.
3. Publishes Docker images with `latest`, Git commit SHA, and version tags.

Required GitHub repository configuration:

- Variable: `DOCKERHUB_USERNAME`
- Secret: `DOCKERHUB_TOKEN`

## Health Check

The application provides a health endpoint:

```text
GET /health
```

It checks connectivity to MongoDB and reports the database connection status.

## Future Improvements

- Add Kubernetes readiness and liveness probes.
- Improve application logging.
- Strengthen input validation.
- Add monitoring and observability.
- Improve deployment security.

## Author

**Danish Abdal**

Aspiring DevOps Engineer

GitHub: [danishabdal10-hub](https://github.com/danishabdal10-hub)

---

*Personal project developed to practice Python application deployment, containerization, CI/CD automation, database integration, and Kubernetes orchestration.*
