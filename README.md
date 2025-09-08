# Kaizen Test

A full-stack application with FastAPI Python backend and React frontend.

## Setup and Installation

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
