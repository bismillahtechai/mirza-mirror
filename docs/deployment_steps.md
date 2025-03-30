# Mirza Mirror Deployment Steps

This document provides step-by-step instructions for deploying the Mirza Mirror application to Render and preparing the iOS app for TestFlight testing.

## Deploying to Render

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to a GitHub repository
2. Make sure your repository is either public or connected to your Render account

### Step 2: Deploy Using Render Blueprint

1. Log in to your Render account at [dashboard.render.com](https://dashboard.render.com)
2. Click on the "New" button in the top right corner
3. Select "Blueprint" from the dropdown menu
4. Connect to your GitHub repository containing the Mirza Mirror code
5. Render will automatically detect the `render.yaml` file
6. Review the services and databases to be created:
   - Services:
     - `mirza-mirror-api` (FastAPI backend)
     - `mirza-mirror-web` (Next.js web app)
   - Databases:
     - `mirza-mirror-db` (PostgreSQL database)

### Step 3: Configure Environment Variables

1. Set the required environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key for AI capabilities
   - Any other required secret keys not already in the render.yaml

2. Click "Apply" to start the deployment process

### Step 4: Monitor Deployment

1. Track the deployment progress in the Render dashboard
2. Check logs for any errors or issues
3. Verify all services are up and running correctly

### Step 5: Test Deployed Services

1. Access the API at `https://mirza-mirror-api.onrender.com`
2. Access the web app at `https://mirza-mirror-web.onrender.com`
3. Verify basic functionality works correctly

## Preparing iOS App for TestFlight

### Step 1: Configure Xcode Project

1. Open the iOS project in Xcode:
   ```
   cd mobile/ios/MirzaMirror
   open MirzaMirror.xcodeproj
   ```

2. Select your project in the Project Navigator
3. Go to the "Signing & Capabilities" tab
4. Ensure you have selected your Apple Developer Team
5. Verify the Bundle Identifier is unique and follows your naming convention
6. Set the Version and Build numbers appropriately

### Step 2: Create App in App Store Connect

1. Log in to [App Store Connect](https://appstoreconnect.apple.com)
2. Go to "Apps" and click the "+" button to create a new app
3. Fill in the required information:
   - Platform: iOS
   - App Name: Mirza Mirror
   - Primary Language: English (or your preferred language)
   - Bundle ID: Select the Bundle ID from your Xcode project
   - SKU: A unique identifier for your app (e.g., com.yourcompany.mirzamirror)
   - User Access: Full Access

### Step 3: Build and Archive the App

1. In Xcode, select the "Generic iOS Device" or a connected device as the build target
2. Select Product > Archive from the menu
3. Wait for the archiving process to complete
4. When the Archives window appears, select your new archive
5. Click "Validate App" to check for any issues
6. Once validation is successful, click "Distribute App"
7. Select "App Store Connect" as the distribution method
8. Follow the prompts to upload your app to App Store Connect

### Step 4: Configure TestFlight

1. In App Store Connect, go to your app and select the "TestFlight" tab
2. Wait for the build to finish processing (this may take some time)
3. Once processing is complete, add test information:
   - Beta App Description: Brief description of your app
   - Beta App Feedback Email: Your email for receiving feedback
   - What to Test: Instructions for testers

4. Create a test group:
   - Go to "Groups" and click "+" to create a new group
   - Name the group (e.g., "Internal Testers")
   - Add testers by email address

5. Enable your build for testing:
   - Select your build
   - Click "Enable" under the "TestFlight" column

### Step 5: Invite Testers

1. Go to your test group
2. Click "Add Testers" and enter email addresses
3. Click "Invite"
4. Testers will receive an email invitation to download TestFlight and your app

## Troubleshooting

### Render Deployment Issues

- **Database Connection Errors**: If you encounter database connection issues, verify that:
  - The PostgreSQL database was successfully created in Render
  - The DATABASE_URL environment variable is correctly linked to the database using `fromDatabase` in render.yaml
  - The SQLAlchemy connection string format is correct (our code includes a fix for "postgres://" vs "postgresql://" prefixes)
- **API Service Failures**: Verify all required environment variables are set
- **CORS Issues**: Ensure the CORS_ORIGINS environment variable includes all necessary frontend URLs

### TestFlight Issues

- **Code Signing Problems**: Verify your certificates and provisioning profiles in Xcode
- **Missing Entitlements**: Ensure all required app capabilities are enabled
- **Build Rejection**: Review Apple's guidelines and fix any compliance issues

## Monitoring and Maintenance

1. Set up monitoring in the Render dashboard
2. Review TestFlight crash reports and user feedback
3. Implement fixes and improvements based on testing results