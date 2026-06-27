# Smart IoT Face Recognition Attendance System

## Overview

The **Smart IoT Face Recognition Attendance System** is an end-to-end attendance management solution that combines **Computer Vision**, **Artificial Intelligence**, **IoT**, and **Web Technologies** to automate attendance tracking.

The system uses a webcam to capture faces in real time, identifies registered users using AI-powered facial recognition, automatically records attendance, and communicates with an **ESP32** over Wi-Fi to display the total number of students present on a **7-segment display**.

This project demonstrates the integration of software and embedded hardware to build a practical real-world application.

---

## Features

* 🔍 Real-time face detection and recognition using OpenCV and DeepFace
* 👤 User registration through an image upload interface
* ✅ Automatic attendance marking for recognized users
* ⏱ Duplicate attendance prevention using a configurable cooldown timer
* 🌐 ESP32 communication over HTTP using REST endpoints
* 🔢 Live attendance count displayed on a 7-segment display
* 💾 Attendance records stored locally even if the IoT device loses network connectivity
* 📊 Web dashboard for attendance management

---

## System Architecture

1. A webcam continuously captures live video.
2. OpenCV detects faces from each frame.
3. DeepFace identifies registered users.
4. Attendance is recorded automatically.
5. The application updates the current attendance count.
6. The ESP32 periodically sends an HTTP GET request to retrieve the latest attendance count.
7. The ESP32 updates the connected 7-segment display with the number of students present.

---

## Technologies Used

### Software

* Python
* Flask
* OpenCV
* DeepFace
* HTML
* CSS
* SQLite (or your database)

### Hardware

* ESP32
* 7-Segment Display
* Webcam

---

## Challenges Solved

* Integrating computer vision with embedded hardware
* Real-time communication between Flask and ESP32 over Wi-Fi
* Preventing duplicate attendance entries
* Handling hardware communication independently from attendance storage
* Synchronizing AI inference with IoT display updates

---

## Future Improvements

* Multi-face recognition support
* Improved recognition accuracy using custom-trained models
* Cloud database integration
* Attendance analytics dashboard
* Email/SMS notifications
* QR code fallback authentication
* Docker deployment
* Mobile application support

---

## Learning Outcomes

Through this project I gained practical experience in:

* Computer Vision
* Face Recognition
* REST API development
* Flask backend development
* Embedded systems programming
* ESP32 Wi-Fi communication
* IoT system integration
* AI-powered application development
* End-to-end system architecture
