# Chatbot Appointment Manager

This project provides a chatbot that can manage appointments, utilizing both a console application and a Flask web application interface. The chatbot is capable of extracting entities, intentions, dates, start times, and end times from user input.

## Getting Started

### Requirements
- Python 3.11.

### Installation
1. Clone the repository:
```bash
git clone https://github.com/meinemeinung/appointment-booking-agent.git
cd chatbot-appointment-manager
```
2. Create a virtual environment:
```bash
python -m venv venv
```
3. Activate the virtual environment:
```bash
venv\Scripts\activate
```
4. Install the required packages:
```bash
pip install -r requirements.txt
```
5. Set up environment variables:
Create a `.env` file in the root directory of the project by copying the `.env.example` file. Update the `.env` file with your configuration.

### Running the Console App
```bash
cd src/
python main.py
```

### Running the Flask Application
```bash
cd src/
python app.py
```