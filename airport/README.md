# Airport Management API

A Flask-based API for managing airport data, including user authentication and role-based access control. This API allows only admin users to add, update, or delete airport records, while regular users can view airports and search by location or facility.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Endpoints](#endpoints)
  - [Authentication](#authentication)
  - [Airports](#airports)
  - [Admin Access](#admin-access)
- [Data Structure](#data-structure)
- [Security](#security)
- [Technologies Used](#technologies-used)
- [License](#license)

## Features
- **User Authentication**: Secure login using JWT, with roles for admin and regular users.
- **Airport Management**: Create, view, update, and delete airport data.
- **Role-Based Access Control**: Admins only can add, update, and delete airport data.
- **Search Functionality**: Users can search airports by location or facility.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/BrianKimurgor/python
   cd python
   cd airport

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Set up MongoDB: Ensure MongoDB is running on localhost:27017**

4. **Load initial data**:
    ```bash
    python3 load_data.py or python load_data.py depending with the python you are using

**Initialize the app(run the app)**:
    ```bash
    python3 app.py or python app.py

## Endpoints

### Authentication

- **Login**
  - **Endpoint**: `POST /login`
  - **Description**: Logs in a user and returns a JWT token.
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

### Airports

- **Add Airport (Admin only)**
  - **Endpoint**: `POST /airports`
  - **Authorization**: JWT token required (Admin only).
  - **Request Body**:
    ```json
    {
      "name": "string",
      "location": "string",
      "code": "string",
      "gates": "integer",
      "terminals": "integer",
      "facilities": ["string"]
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Airport added successfully"
    }
    ```

- **Get All Airports**
  - **Endpoint**: `GET /airports`
  - **Response**: List of airport objects.
  - **Example Response**:
    ```json
    [
      {
        "name": "Marciaton International Airport",
        "location": "Amberside",
        "code": "VKN",
        "gates": 92,
        "terminals": 5,
        "facilities": ["Car Rental", "Free Wi-Fi", "VIP Lounge"]
      },
      {
        "name": "Skyland Airport",
        "location": "Newark",
        "code": "SLD",
        "gates": 42,
        "terminals": 2,
        "facilities": ["Shuttle Service", "Hotel Booking"]
      }
    ]
    ```

- **Update Airport (Admin only)**
  - **Endpoint**: `PUT /airports/<id>`
  - **Authorization**: JWT token required (Admin only).
  - **Path Parameters**: `id` (string) - ID of the airport to update.
  - **Request Body**: Fields to update.
  - **Response**:
    ```json
    {
      "message": "Airport updated successfully"
    }
    ```

- **Delete Airport (Admin only)**
  - **Endpoint**: `DELETE /airports/<id>`
  - **Authorization**: JWT token required (Admin only).
  - **Path Parameters**: `id` (string) - ID of the airport to delete.
  - **Response**:
    ```json
    {
      "message": "Airport deleted successfully"
    }
    ```

- **Search Airports**
  - **Endpoint**: `GET /airports/search`
  - **Query Parameters**:
    - `location` (string, optional)
    - `facility` (string, optional)
  - **Response**: List of matching airport objects.
  - **Example Query**:
    ```
    GET /airports/search?location=Amberside&facility=Free%20Wi-Fi
    ```
  - **Example Response**:
    ```json
    [
      {
        "name": "Marciaton International Airport",
        "location": "Amberside",
        "code": "VKN",
        "gates": 92,
        "terminals": 5,
        "facilities": ["Car Rental", "Free Wi-Fi", "VIP Lounge"]
      }
    ]
    ```

### Admin Access

Admin users have full access to all CRUD operations on airports, while regular users have read-only access. Admin access is determined by a JWT token, which contains the admin role.

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


## Airports

The  `airports` collection stores airport information.

```json
    {
    "name": "Marciaton International Airport",
    "location": "Amberside",
    "code": "VKN",
    "gates": 92,
    "terminals": 5,
    "facilities": ["Car Rental", "Free Wi-Fi", "VIP Lounge"]
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
