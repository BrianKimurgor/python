
# Full-Stack Backend Application for Bookstore, Carpark, and Airport Management

This repository contains three backend projects: `books`, `carpark`, and `airport`. Each project is structured similarly and uses a Python Flask API with a MongoDB database. These applications demonstrate CRUD operations and more advanced functionality, including user authentication and validation, making them fit for production needs. All three projects share similar features but are tailored to different datasets.

## Project Structure

- **books/**: Backend for a bookstore management system with user accounts (admin and non-admin) and a books catalog.
- **carpark/**: Backend for managing carpark information, including user accounts and carpark data.
- **airport/**: Backend for managing airport information, user accounts, and airport facilities.

Each project directory includes its own `README.md` file for detailed, project-specific instructions.

## Getting Started

### Clone the Repository

To get a copy of this project on your local machine, run:

```bash
git clone https://github.com/BrianKimurgor/python.git
cd python
```

### Create a Virtual Environment

Navigate to the project folder and create a virtual environment to install the required dependencies.

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```

### Install Dependencies

With the virtual environment activated, install the dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Configuration

Each project (`books`, `carpark`, `airport`) has a `data` folder containing JSON files that serve as the dataset. You may need to configure environment variables such as database URIs or JWT secrets. Refer to each project’s `README.md` for specific configuration steps.

## Usage

Once setup is complete, each application can be run individually. Run the Flask server in each project’s root folder to start the API and access available endpoints.

```bash
# Example for the Bookstore API:
cd books
flask run
```

Follow the same steps for `carpark` and `airport`.

---

For additional information on specific API endpoints, database models, and functionality, refer to each project’s `README.md`.

```