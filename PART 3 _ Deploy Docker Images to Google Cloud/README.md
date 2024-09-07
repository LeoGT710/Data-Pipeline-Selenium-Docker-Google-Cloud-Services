
```markdown
# Docker Image Push & Pull Workflow

This guide explains how to push a Docker image to Docker Hub, pull it, tag it, and then push it to Google Cloud Artifact Registry.

## Prerequisites

- Docker installed on your local machine.
- A Docker Hub account.
- Access to Google Cloud and permission to push images to Google Cloud Artifact Registry.

## Workflow Overview

1. **Push Docker Image to Docker Hub**
2. **Pull Docker Image from Docker Hub in Google Cloud**
3. **Tag Docker Image for Google Cloud Artifact Registry**
4. **Push Docker Image to Google Cloud Artifact Registry**

---

## Step 1: Push Docker Image to Docker Hub

First, build and tag your Docker image. Then, push the image to Docker Hub:

```bash
# Push the image to Docker Hub
docker push ******/webscraping:latest
```

This command pushes the `webscraping:latest` image to your Docker Hub repository (`leogt710`).

---

## Step 2: Pull Docker Image from Docker Hub in Google Cloud

To access this image from Google Cloud (e.g., using Google Cloud Shell or another cloud environment), you can pull the image from Docker Hub:

```bash
# Pull the image from Docker Hub
docker pull **********/webscraping:latest
```

This pulls the Docker image to the Google Cloud environment for further use.

---

## Step 3: Tag Docker Image for Google Cloud Artifact Registry

Once the image is pulled, tag it for Google Cloud Artifact Registry:

```bash
# Tag the image for Google Cloud Artifact Registry
docker tag ****************/webscraping:latest
```

This tags the image so it can be pushed to the Artifact Registry in the `asia-southeast1` region under your `goc-data-**********` project.

---

## Step 4: Push Docker Image to Google Cloud Artifact Registry

Finally, push the tagged image to the Artifact Registry:

```bash
# Push the image to Google Cloud Artifact Registry
docker push *******/webscraping:latest
```

This command uploads the Docker image to the specified Google Cloud Artifact Registry location.

---

## Notes

- Make sure you are authenticated with Google Cloud before pushing to Artifact Registry.
- You can set up authentication by running:

  ```bash
  gcloud auth configure-docker asia-southeast1-docker.pkg.dev
  ```

- Replace the region and project details as needed.

---

## Conclusion

This process helps you manage your Docker images by first pushing them to Docker Hub, then pulling them into a Google Cloud environment, tagging them appropriately, and finally pushing them to Google Cloud Artifact Registry for use in Google Cloud services like Cloud Run, Cloud Functions, or Kubernetes Engine.
```

![alt text](image.png)

