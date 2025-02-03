# Number Classification API

## Overview
The **Number Classification API** is a RESTful API built using Django and Django REST Framework (DRF). It takes a number as input, including negative numbers, and returns its mathematical properties along with a fun fact retrieved from the Numbers API.

## Backlink
Backlink to python developers: https://hng.tech/hire/python-developers

## Features
- Determines if a number is **prime**
- Checks if a number is **perfect**
- Identifies if a number is an **Armstrong number**
- Classifies the number as **odd or even**
- Computes the **sum of its digits**, handling negative numbers by summing the absolute values and appending a `-` if the original number was negative
- Fetches a **fun fact** about the number from the Numbers API
- Returns responses in **JSON format**
- Handles invalid input with appropriate error messages

## Technologies Used
- **Python** (Django + Django REST Framework)
- **Requests** (for external API calls)
- **CORS Headers** (to allow cross-origin requests)

## API Endpoint

### **Classify a Number**
- **URL**: `/api/classify-number?number=<integer>`
- **Method**: `GET`
- **Query Parameter**:
  - `number` (integer) - The number to classify.

### **Example Request**
```sh
GET /api/classify-number?number=-371
```

### **Success Response (200 OK)**
```json
{
    "number": -371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": "-11",
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}
```

### **Error Response (400 Bad Request)**
```json
{
    "number": "alphabet",
    "error": true
}
```

## Installation & Setup

### **1. Clone the Repository**
```sh
git clone https://github.com/Tonyjr7/Number-Classifier-API.git
cd Number-Classifier-API
```

### **2. Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Run Migrations**
```sh
python manage.py migrate
```

### **5. Start the Development Server**
```sh
python manage.py runserver
```
The API will now be available at `http://127.0.0.1:8000/api/classify-number?number=<integer>`.

## Deployment
1. Deploy on a platform like **Render, Railway, or Fly.io**.
2. Ensure CORS is properly configured.
3. Set up environment variables if needed.
4. Make sure the API is publicly accessible.

## Contribution
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.
