# 🏗 AI Construction Safety Monitoring System

## 🚀 Overview

AI Construction Safety Monitoring System is an AI-powered PPE compliance detection platform that transforms traditional CCTV surveillance into proactive safety intelligence.

The system detects whether workers are wearing required Personal Protective Equipment (PPE) such as helmets and safety vests, calculates compliance scores, classifies risk levels, and generates actionable safety insights through a web dashboard.

## 🎯 Problem

Construction sites rely on manual supervision and passive CCTV monitoring to ensure PPE compliance. Human monitoring is inconsistent and cannot scale across large or multi-site operations, leading to unnoticed safety violations, increased accidents, and regulatory risks.

## 💡 Solution

Our system uses Computer Vision (YOLO-based object detection) to:

Detect helmets and safety vests in images and videos

Calculate PPE compliance score

Classify overall site risk level (Low / Moderate / High)

Generate visual analytics via a Streamlit dashboard

Provide automated compliance summaries

This converts passive surveillance into intelligent, data-driven safety monitoring.

## 🛠 Tech Stack

Python

YOLO (Ultralytics)

OpenCV

Streamlit

PyTorch

NumPy

## 📊 Features

### 🖼 Image-based PPE detection

🎥 Video-based PPE compliance analysis

### 📈 Compliance score calculation

🚨 Risk level classification

### 📋 Automated safety summary generation

🎥 Processed video preview frames

### 🌐 Public web deployment

## 🏗 Architecture

User uploads image or video

YOLO model performs object detection

System checks helmet & vest presence

Compliance score is computed

Risk level is classified

Dashboard displays results

## 💰 Business Model

SaaS subscription per site

Per-camera pricing model

Enterprise annual licensing

Add-on alert & reporting services

## 🎯 Target Audience

Construction companies

Infrastructure contractors

Industrial worksites

Safety compliance officers

## 🔍 Competitive Advantage

Affordable mid-market solution

Simple compliance scoring dashboard

Lightweight deployment

No complex hardware integration required

## 🚀 Deployment

Deployed using Streamlit Cloud.

## 📌 Future Improvements

Fire detection module

Unauthorized entry detection

Zone-based compliance rules

Multi-site analytics dashboard

Real-time CCTV integration
