# End-to-End CI/CD Pipeline — Sample App to Kubernetes

![CI/CD Pipeline](https://github.com/MReshma575/cicd-pipeline-eks/actions/workflows/ci.yml/badge.svg)

A complete delivery loop for a small Python service: **code → tests → container image →
Kubernetes manifest update → GitOps sync**. Every merge to `main` ships itself.

## The loop

```
push to main
   │
   ├─ 1. TEST        pytest unit tests (GitHub Actions)
   ├─ 2. BUILD       multi-stage Docker image, pushed to GHCR tagged with the commit SHA
   ├─ 3. UPDATE      the pipeline rewrites k8s/deployment.yaml to the new tag and commits it
   └─ 4. SYNC        Argo CD detects the manifest change and rolls the cluster to the new image
                     (GitOps pattern — see the globomantics-gitops repository)
```

A Jenkins equivalent of the same pipeline is included (`Jenkinsfile`) — same stages,
same GitOps hand-off, for Jenkins-based teams.

## What's inside

| Path | What it is |
|---|---|
| `app.py` | Flask service with `/` and `/health` endpoints |
| `tests/test_app.py` | pytest unit tests for both endpoints |
| `Dockerfile` | Multi-stage build, slim runtime image, non-root user, container healthcheck |
| `k8s/deployment.yaml` | Deployment with probes + resource limits; the image tag is pipeline-managed |
| `k8s/service.yaml` | ClusterIP Service |
| `.github/workflows/ci.yml` | The pipeline: test → build/push → manifest update |
| `Jenkinsfile` | The same pipeline in Jenkins declarative syntax |

## Design choices worth knowing

- **Images are tagged with the commit SHA, never just `latest`** — every running pod
  traces back to an exact commit, and rollback is "point the manifest at the old SHA."
- **The pipeline commits the manifest change back to Git** instead of running
  `kubectl apply` — the cluster's desired state stays in version control, where
  Argo CD (and code review) can see it. The `[skip ci]` tag prevents an infinite loop.
- **Tests gate the image build** — a failing test means no image, no manifest change,
  and the cluster keeps the last good version.
- **Multi-stage Dockerfile** — build dependencies stay out of the runtime image:
  smaller image, smaller attack surface.
- **Probes point at `/health`** — readiness gates traffic until the app actually
  responds; liveness restarts it if it wedges.

## Run it locally

```bash
pip install -r requirements-dev.txt
pytest -v                 # run the tests
python app.py             # serve on :8080

docker build -t cicd-demo-app .
docker run -p 8080:8080 cicd-demo-app
curl localhost:8080/health
```

## Skills demonstrated

CI/CD pipeline design · GitHub Actions · Jenkins · Docker (multi-stage builds) ·
Kubernetes deployments & probes · GitOps hand-off to Argo CD · GHCR image registry ·
test-gated delivery · immutable image tagging
