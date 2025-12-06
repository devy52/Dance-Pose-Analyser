# Dance Pose Analyser ( A Cloud-based AI System for Dance Movement & Pose Analysis )

A computer vision and machine learning toolkit for analyzing dance poses from video or image inputs. This repository leverages keypoint detection and pose estimation to help dancers and choreographers assess movement quality, alignment, and performance.

LIVE Server → http://16.176.158.73:8000/

---

# Overview

Dance Pose Analyser is a cloud-deployed AI/ML application that processes short dance videos, extracts human pose keypoints using MediaPipe, and outputs an annotated video showing the dancer's skeleton movement in real time.
The system is fully containerized using Docker and deployed on an AWS EC2 instance with a FastAPI backend and FFmpeg-powered video processing.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Approach](#approach)
- [Requirements](#requirements)
- [Setup](#setup)
- [API Usage](#api-usage)
- [Docker Deployment](#docker-deployment)
- [Deployment on AWS EC2](#deployment-on-aws-ec2)
- [Contributions](#contributions)
- [License](#license)


---

## Features

- Extracts human pose keypoints from uploaded dance videos
- Generates a reconstructed skeleton overlay video
- Converts uploaded videos to H.264 for browser-safe playback
- FastAPI backend for secure file upload and processing
- Video preview + downloadable output
- Dockerized for easy cloud deployment
- Auto-cleanup of temporary files

---

## Architecture

```bash
                                       
                                                +-------------------------------+
                                                |        User Uploads Video     |
                                                +-------------------------------+
                                                               |
                                                               v
                                                +-------------------------------+
                                                |        FastAPI Server         |
                                                |        (/upload API)          |
                                                +-------------------------------+
                                                               |
                                                               v
                                                +-------------------------------+
                                                |    PoseProcessor (Python)     |
                                                | - OpenCV Frame Reading        |
                                                | - MediaPipe Pose Keypoints    |
                                                | - Skeleton Overlay            |
                                                | - FFmpeg Video Encoding       |
                                                +-------------------------------+
                                                               |
                                                               v
                                                +-------------------------------+
                                                |   Annotated Output Video      |
                                                +-------------------------------+
                                                               |
                                                               v
                                                +-------------------------------+
                                                |   AWS EC2 + Docker Runtime    |
                                                +-------------------------------+


```

---

## Approach

Before starting the project, I planned the implementation in three stages:

### 1. Core Movement Analysis Engine

   - Use MediaPipe Pose Landmarker for robust keypoint detection
   - Process video frame-by-frame using OpenCV
   - Compute pose skeletons and overlay them onto frames
   - Reconstruct a new annotated video showing motion dynamics
   - Use FFmpeg to encode/decode videos cleanly

This ensured the technical correctness of movement analysis.

### 2. Containerization & API Development

   - Wrap the pose engine behind a clean FastAPI server
   - Provide a simple API endpoint (POST /upload)
   - Accept raw video → process → return output video name
   - Build a Dockerfile with all system dependencies:
        - FFmpeg
        - MediaPipe
        - OpenCV
   - Expose port 8000 and run via uvicorn

This made the system portable and reproducible.

### 3. Cloud Deployment

   - Deploy to AWS EC2 for public access
   - Use Docker Compose to manage the container
   - Persist processed output videos via volume mounts
   - Serve static files and templates directly from FastAPI
   - Implement cleanup logic and server lifespan hooks
   - Optional: auto-update GitHub Packages image → EC2 container

This satisfied the cloud deployment and DevOps requirement.

---

## Requirements

- Python 3.10+
- OpenCV (`opencv-python`)
- NumPy
- Matplotlib (optional, for visualization)
- mediapipe (for pose estimation)
- Any other dependencies listed in `requirements.txt`

---

## Setup

1. Clone Repo

   ```bash
   git clone https://github.com/devy52/dance_pose_analyser
   cd dance_pose_analyser
   ```
   
2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```
   
3. Run Locally

   ```bash
   python3 server.py
   ```

Visit → http://localhost:8000

---

## API Usage

<img width="1159" height="590" alt="image" src="https://github.com/user-attachments/assets/2ec79cda-3632-4b98-ae17-a2759c2059a4" />

### POST /upload

- Upload MP4/MOV/AVI/MKV video and receive output filename.

#### Request (Python example)
```bash
import requests

files = {"file": open("dance.mp4", "rb")}
res = requests.post("http://<server-ip>:8000/upload", files=files)
print(res.json())
```

#### Sample Response
```bash
{
  "output": "8f3a2e1c1d_annotated.mp4"
}
```

### GET /preview/{file}

- Streams the processed video.

### GET /download/{file}

- Downloads the processed video.

---

## Docker Deployment

### Build locally:
```bash
docker build -t dance-pose-analyser .
```
### Run:
```bash
docker run -d -p 8000:8000 --name pose-api dance-pose-analyser
```
---

## Deployment on AWS EC2

You can deploy and host this application on an [AWS EC2](https://aws.amazon.com/ec2/) instance for remote access and scalability.

### Steps to Deploy:

1. **Launch an EC2 Instance**
   - Recommended: Ubuntu Server (20.04 or later)
   - Choose instance type (e.g. t2.medium for moderate CPU use, GPU instance for faster inference)

2. **Connect to Your Instance**
   - Use SSH:
     ```bash
     ssh -i your-key.pem ubuntu@your-ec2-public-ip
     ```

3. **Install Docker**
   ```bash
   sudo apt update
   sudo apt install docker.io
   ```

4. **Pull Docker Image**
   ```bash
   docker pull ghcr.io/devy52/dance-pose-analyser:latest
   ```

5. **Run Container**
   - For a command-line tool or script:
     ```bash
     docker run -d -p 8000:8000 --name dance_pose_app ghcr.io/devy52/dance-pose-analyser:latest
     ```

6. **Accessing Externally**
   - Visit your server via `http://<EC2-public-IP>:<port>`
   - Port used in this project is 8000


---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

- [AWS EC2 Setup Documentation](https://docs.aws.amazon.com/ec2/)
- [MediaPipe Pose Documentation](https://google.github.io/mediapipe/solutions/pose.html)
