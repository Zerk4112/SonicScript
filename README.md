# SonicScript

SonicScript is a web application designed to simplify the process of transcribing audio files. It provides users with an intuitive interface for uploading audio files, normalizing audio quality, and generating accurate transcriptions using Whisper AI.

## Table of Contents

- [Getting Started](#getting-started)
  - [Frontend](#frontend)
  - [Backend](#backend)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Frontend

The frontend of the application is built using React. To set it up, follow these steps:

1. Navigate to the `sonicscript-frontend` directory.
2. Install dependencies with `npm install`.
3. Start the development server with `npm start`.

### Backend

The backend is built using Flask, a Python web framework. Follow these steps to set it up:

1. Navigate to the `backend` directory.
2. Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Flask with `pip install Flask`.
4. Run the Flask app with `flask run`.

## API Endpoints

The following API endpoints are available:

- **File Upload:** `POST /api/upload`
  - Upload an audio file for transcription.

- **Transcription:** `POST /api/transcribe`
  - Initiate the transcription process.

## Contributing

Contributions are welcome! If you'd like to contribute to the development of this project, please follow the guidelines outlined in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
