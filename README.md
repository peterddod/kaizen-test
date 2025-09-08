# Kaizen Test

A full-stack application with FastAPI Python backend and React frontend.

## Setup and Installation

## Environment Variables

Before running the application, you need to set up environment variable files for both the backend and frontend. Each directory contains a `.env.example` file with example variables.

1. **Copy the example files to create your local environment files:**
   - For the backend:
     ```
     cd backend
     cp .env.example .env.local
     ```
   - For the frontend:
     ```
     cd frontend
     cp .env.example .env.local
     ```

2. **Edit the `.env.local` files** in each directory to provide the appropriate values for your environment.

> **Note:**  
> The application will load environment variables from `.env.local`. Make sure not to commit your `.env.local` files to version control, as they may contain sensitive information.


### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```
   python main.py
   # Or alternatively:
   uvicorn main:app --reload 
   ```

5. Access the API documentation:
   ```
   http://localhost:8000/docs
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```

## Development

- Backend code is in the `backend` directory
  - API endpoints are defined in `app.py`
  - API documentation available at `http://localhost:8000/docs`
- Frontend code is in the `frontend/src` directory

