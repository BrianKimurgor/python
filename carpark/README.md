# Car Park Management API

A Flask-based API for managing car park data, including user authentication and role-based access control. This API allows only admin users to add, update, or delete car park records, while regular users can view car parks and search by location or available services.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Endpoints](#endpoints)
  - [Authentication](#authentication)
  - [Car Parks](#car-parks)
  - [Admin Access](#admin-access)
- [Data Structure](#data-structure)
- [Security](#security)
- [Technologies Used](#technologies-used)
- [License](#license)

## Features
- **User Authentication**: Secure login using JWT, with roles for admin and regular users.
- **Car Park Management**: Create, view, update, and delete car park data.
- **Role-Based Access Control**: Admins only can add, update, and delete car park data.
- **Search Functionality**: Users can search car parks by location or available services.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BrianKimurgor/python
   cd python
   cd carpark

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Load initial data**:
    ```bash
    python3 load_data.py or python load_data.py

4. **Initialize the app (run the app)**:
    python3 app.py or python app.py

## Endpoints

### Authentication

- **Login**
  - **Endpoint**: `POST /login`
  - **Description**: Authenticates a user and returns a JWT token.
  - **Request Body**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "access_token": "string (JWT token)"
    }
    ```

### Car Parks

- **Add Car Park (Admin only)**
  - **Endpoint**: `POST /carparks`
  - **Authorization**: JWT token required (Admin only).
  - **Request Body**:
    ```json
    {
      "name": "string",
      "location": "string",
      "totalSpaces": integer,
      "availableSpaces": integer,
      "ratePerHour": integer,
      "facilities": ["string"]
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Car park added successfully"
    }
    ```

- **Get All Car Parks**
  - **Endpoint**: `GET /carparks`
  - **Response**: List of car park objects.
  - **Example Response**:
    ```json
    [
      {
        "name": "Downtown Parking",
        "location": "Downtown Street, City",
        "totalSpaces": 100,
        "availableSpaces": 50,
        "ratePerHour": 5,
        "facilities": ["Security", "Restrooms", "EV Charging"]
      },
      {
        "name": "Airport Parking",
        "location": "Airport Road, City",
        "totalSpaces": 200,
        "availableSpaces": 20,
        "ratePerHour": 10,
        "facilities": ["Shuttle Service", "24/7 Access"]
      }
    ]
    ```

- **Update Car Park (Admin only)**
  - **Endpoint**: `PUT /carparks/<id>`
  - **Authorization**: JWT token required (Admin only).
  - **Path Parameters**: `id` (string) - ID of the car park to update.
  - **Request Body**: Fields to update.
  - **Response**:
    ```json
    {
      "message": "Car park updated successfully"
    }
    ```

- **Delete Car Park (Admin only)**
  - **Endpoint**: `DELETE /carparks/<id>`
  - **Authorization**: JWT token required (Admin only).
  - **Path Parameters**: `id` (string) - ID of the car park to delete.
  - **Response**:
    ```json
    {
      "message": "Car park deleted successfully"
    }
    ```

- **Search Car Parks**
  - **Endpoint**: `GET /carparks/search`
  - **Query Parameters**:
    - `location` (string, optional)
    - `facility` (string, optional)
  - **Response**: List of matching car park objects.
  - **Example Query**:
    ```
    GET /carparks/search?location=Downtown&facility=Security
    ```
  - **Example Response**:
    ```json
    [
      {
        "name": "Downtown Parking",
        "location": "Downtown Street, City",
        "totalSpaces": 100,
        "availableSpaces": 50,
        "ratePerHour": 5,
        "facilities": ["Security", "Restrooms", "EV Charging"]
      }
    ]
    ```

### Admin Access

Admin users have full access to all CRUD operations on car parks, while regular users have read-only access. Admin access is determined by a JWT token, which contains the admin role.


## Data Structure

### Users

The `users` collection stores user data with admin status for access control.

```json
{
  "username": "nkelley",
  "password": "hashed_password",
  "admin": true
}
```

## Security

Password Hashing: Passwords are hashed before storage for security.
JWT Tokens: All restricted operations require a JWT token for secure access.
Role-Based Access Control: Admin-only restrictions prevent unauthorized access to critical endpoints.

## Technologies Used

- **Backend**: Flask
- **Database**: MongoDB
- **Authentication**: Flask-JWT-Extended
- **Password Hashing**: Werkzeug


