
# ML Tech Challenge - Phase 1

This project is a solution to a machine learning challenge that involves scraping data from various sections (Production, Processing, Commercialization, Import, and Export) from the Embrapa website, and serving this data via a FastAPI application.

## Project Setup

Follow these steps to set up the project for the first time:

### Prerequisites

1. **Python 3.9+**: Make sure you have Python 3.9 or higher installed. You can check your Python version by running:
    ```bash
    python --version
    ```

2. **Poetry**: The project uses Poetry for dependency management. Install it by following the instructions at: https://python-poetry.org/docs/#installation

3. **Git**: To clone the project repository, you will need Git installed on your machine.

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ml-techchallenge-01.git
    cd ml-techchallenge-01
    ```

2. Create a virtual environment and install dependencies with Poetry:
    ```bash
    poetry install
    ```

3. Activate the virtual environment:
    ```bash
    poetry shell
    ```

4. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

Now, you should be able to access the application at `http://127.0.0.1:8000`.

### Project Structure

- **`app/`**: Main application code
  - **`scraping/`**: Contains the scraping code for each section.
    - **`production.py`**: Scraping logic for the Production section.
    - **`processing.py`**: Scraping logic for the Processing section.
    - **`commercialization.py`**: Scraping logic for the Commercialization section.
    - **`import.py`**: Scraping logic for the Import section.
    - **`export.py`**: Scraping logic for the Export section.
  - **`core/`**: Utility functions and core logic.
    - **`utils.py`**: General utility functions.
  - **`models/`**: Pydantic models and database schemas.
    - **`schemas.py`**: Data models for validation and response structures.
  - **`main.py`**: The entry point for the FastAPI application, defining the routes and endpoints.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.