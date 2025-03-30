# Deployment Guide for Mirza Mirror

This document provides instructions for deploying the Mirza Mirror thought externalization system both locally for development and on Render for production.

## Local Development Deployment

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mirza-mirror.git
   cd mirza-mirror
   ```

2. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up
   ```

4. Access the application:
   - Backend API: http://localhost:8000
   - Web App: http://localhost:3000

5. To stop the application:
   ```bash
   docker-compose down
   ```

## Production Deployment on Render

### Prerequisites
- A Render account
- OpenAI API key

### Steps

1. Fork or clone the repository to your GitHub account.

2. Log in to your Render account and navigate to the Dashboard.

3. Click on "New" and select "Blueprint" from the dropdown menu.

4. Connect your GitHub repository.

5. Render will automatically detect the `render.yaml` file and configure the services.

6. Set the required environment variables:
   - For the `mirza-mirror-api` service, set `OPENAI_API_KEY` to your OpenAI API key.

7. Click "Apply" to start the deployment process.

8. Once deployment is complete, you can access your application at:
   - Backend API: https://mirza-mirror-api.onrender.com
   - Web App: https://mirza-mirror-web.onrender.com

## Mobile App Deployment

### iOS App
The iOS app is located in the `mobile/ios` directory. To build and deploy:

1. Open the project in Xcode.
2. Update the API URL in `APIService.swift` to point to your deployed backend.
3. Build and archive the app for App Store distribution.

### Android App
The Android app is located in the `mobile/android` directory. To build and deploy:

1. Open the project in Android Studio.
2. Update the API URL in `ApiService.kt` to point to your deployed backend.
3. Build and generate a signed APK or App Bundle for Google Play Store distribution.

## Monitoring and Maintenance

- Monitor application logs through the Render dashboard.
- Set up alerts for service outages or errors.
- Regularly update dependencies to ensure security and performance.

## Troubleshooting

- If the API service fails to start, check the logs for any error messages.
- If the web app cannot connect to the API, verify that the `NEXT_PUBLIC_API_URL` environment variable is set correctly.
- For database issues, check the PostgreSQL logs and ensure the connection string is correct.

For additional support, please refer to the [Render documentation](https://render.com/docs) or contact the development team.
