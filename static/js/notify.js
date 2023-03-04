import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js";
import {
    getMessaging,
    getToken,
} from "https://www.gstatic.com/firebasejs/9.17.1/firebase-messaging.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCLKYQxIyfLNz34y_Zzvjg9HUHqPncz9VI",
    authDomain: "aquariumsmart-ee6ce.firebaseapp.com",
    databaseURL:
        "https://aquariumsmart-ee6ce-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "aquariumsmart-ee6ce",
    storageBucket: "aquariumsmart-ee6ce.appspot.com",
    messagingSenderId: "992071693011",
    appId: "1:992071693011:web:dd32214cd97120724dda26",
    measurementId: "G-FFSM92VK5Z",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

function requestPermission() {
    console.log("Requesting permission...");
    Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
            console.log("Notification permission granted.");
        }
    });
}
requestPermission();

getToken(messaging, {
    vapidKey:
        "BMUollaI8xqZO2-DQ-8hXbVQN5BBn3bXJtTthglDcsf57QnuGDCUq05gfYdIWPKMuW09o39B9IzHoDdOSYNV6pQ",
})
    .then((currentToken) => {
        if (currentToken) {
            // Send the token to your server and update the UI if necessary
            // ...
        } else {
            // Show permission request UI
            console.log(
                "No registration token available. Request permission to generate one."
            );
            // ...
        }
    })
    .catch((err) => {
        console.log("An error occurred while retrieving token. ", err);
        // ...
    });
