IoT Plant Caring Platform (IPCP)

A lightweight IoT-based plant care system for busy users, gardening beginners, and students. The system monitors temperature, humidity, and brightness, and supports both automatic actions (watering, plant light) and manual remote control via a web interface.

Introduction
1. System Purpose

Provide a simple, user-friendly plant care platform that:

Monitors temperature, humidity, and brightness in real time.

Automatically waters plants or turns on the grow light when thresholds are not met.

Allows users to remotely inspect data and manually trigger watering or lighting.

2. System Scope

Includes hardware, software, and documentation/technical support.

Objectives

Track environmental data (temperature, humidity, brightness).

Automatically or manually adjust humidity and brightness.

Main Features

Humidity: Observe real-time soil moisture.

Temperature: Observe ambient air temperature.

Brightness: Observe environmental light intensity.

Watering: Automated or manual control via pump.

Plant Light: Automated or manual light control.

Users

Anyone who installs/purchases the system.

Interface

Web-based interface for primary operations.

3. Terminology & Abbreviations

System: IoT Plant Caring Platform (IPCP)

User: Person who operates or receives system services

Environmental Indicator: Measured values (humidity, temperature, brightness)

Environmental Condition: Thresholds (preset or user-defined) for each indicator

Humidity: Soil moisture

Temperature: Ambient air temperature

Brightness: Light intensity near the plant

Component: Physical/virtual modules (hardware or software)

Environment Variable: Variables storing runtime/config information

GPIO: General Purpose Input/Output interface on SBC/embedded systems

SMTP Server: Server for sending emails

Token: Credential for identification/secure access

Tunneling: Encapsulating one protocol within another for transport

4. References

Raspberry Pi Documentation

Ngrok Documentation

Flask Documentation (3.0.x)

Raspberry Pi 3 Model B+ Datasheet (2023)

National Archives Administration — Reference Format Guide (2015)

IBM — Test Case Template Reference

System Overview

Goal
Provide a small-scale plant care system that measures temperature, humidity, and brightness, and adjusts them automatically or through manual controls.

Key Components

Hardware

Raspberry Pi 3 Model B+ (with Wi-Fi)

DC 5V submersible water pump

LM393 light sensor module (adjustable threshold)

YL-69 soil moisture sensor (adjustable threshold)

DHT22 temperature/humidity sensor

Tongling JQC-3FF-S-Z 2-channel relay (1 active + 1 spare)

5V grow light strip (purple spectrum, 50 cm, 2.4 W, effective range 0.5–1 m)

Software

Raspberry Pi OS (Linux)

Ngrok (reverse proxy / HTTP tunneling)

Flask (Python micro web framework)

Sensor modules (temperature/humidity/brightness acquisition)

Humidity control module (pump)

Brightness control module (grow light)

Temporary URL update module (notifies users of new access URL)

Web operation module (user interface)

Component Interactions

Users operate the system via a web UI to view/adjust plant conditions or enable automation.

Sensor modules stream indicators to a Flask service on the Pi.

Based on preset/user-defined thresholds, the relay controls the pump and grow light.

URL update module refreshes the Ngrok URL for remote access in different networks.

User Interaction

System emails the current access URL to the configured user address.

Users view temperature, humidity, brightness and operate watering/light from the web UI.

Admin starts the service for user access.

System Description
1. Product Perspective

Designed for small indoor plants (home/office).
Integrates multiple sensors/actuators with a simple web UI (up to 5 metrics, 4 action buttons per view).
Remote operation enabled via Flask + Ngrok with dynamic URL updates.

2. Product Functions

Temperature Monitoring (DHT22): Real-time display; informs automated control.

Humidity Monitoring & Control (YL-69 + pump): Auto/manual watering to maintain ideal moisture.

Brightness Monitoring & Control (LM393 + grow light): Auto/manual light adjustments.

Remote Web Operation (Flask): Live monitoring and control.

Dynamic URL Updates (Ngrok): Periodically refreshed temporary URL emailed to users.

3. System Users

Plant-Care Users: Configure thresholds; use auto/manual adjustments.

System Setup Personnel: Configure parameters and start/maintain services.

4. System Constraints

Requires Wi-Fi coverage; remote features depend on network stability and speed.

Requires stable power.

Grow light effective range: 0.5–1 m (not for large areas).

Supports Raspberry Pi models with networking (Pi 3+).

5. System Assumptions

Users can configure Ngrok and SMTP env variables per docs.

Users can assemble and wire hardware.

Plant species fall within the designed environmental thresholds.

Requirements Specification
1. External Interface Requirements

User Interface

Flask periodically retrieves a new Ngrok URL and emails it to users.

Homepage shows current indicators and action buttons (Water / Light).

Supports mainstream browsers (e.g., Chrome, Edge/Chromium, Firefox).

Hardware Interface

Operates with network connectivity.

Raspberry Pi 3 or newer is required.

GPIO pins must be functional; use jumper wires and a breadboard.

Software Interface

Raspberry Pi OS

Flask 1.1.2

Ngrok 3.8.0

SMTP for email sending

Communication Interface

HTTP for all data transfer

Ngrok tunneling for public access

GPIO for sensor/actuator control

Users visit the system via the Ngrok URL

2. Functional Requirements

User Type 1 — Plant-Care User

R101: Remotely control watering and grow light

R102: Receive periodically updated access URLs

R103: Manually adjust humidity/brightness thresholds

User Type 2 — System Administrator

R201: Configure system parameters

R202: Maintain system services

R203: Start/restart services

User Type 3 — System Logic

R301: Auto-water/enable light when indicators fall below thresholds

R302: Refresh indicators every 3–5 minutes

3. Performance Requirements

Update environmental indicators at least every 3–5 minutes.

4. Design Constraints

Gmail SMTP requires an App Password, configured via environment variables (with the sender email).

Ngrok requires registration and a valid Auth Token set on the host.

Ngrok Free tier limits: 20,000 HTTP(S) requests/month, 1 GB data transfer.

5. Software Attributes

Must sustain continuous operation for at least 2 weeks.

6. Additional Requirements

Provide user documentation and setup/operation guides to assist installation and usage.
