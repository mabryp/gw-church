// Firebase web-app config for the gw-church project.
//
// This is NOT a secret: every Firebase web app ships this object in its page
// source, and this repo is public. The Firestore security rules
// (firestore.rules) and App Check are what protect the data.
//
// Fill in after registering a Web App on the project:
//   firebase apps:sdkconfig WEB --project gw-church
// The values below are placeholders. The page still works fully against the
// local emulators (firebase emulators:start) with placeholders in place.
export const firebaseConfig = {
  apiKey: "REPLACE_WITH_WEB_APP_API_KEY",
  authDomain: "gw-church.firebaseapp.com",
  projectId: "gw-church",
  appId: "REPLACE_WITH_WEB_APP_ID"
};
