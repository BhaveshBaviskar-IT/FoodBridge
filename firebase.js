
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyColhR_XJB2UE8UivQ4InrNkW6BlQMThJo",
  authDomain: "food-bridge-c7c44.firebaseapp.com",
  projectId: "food-bridge-c7c44",
  storageBucket: "food-bridge-c7c44.firebasestorage.app",
  messagingSenderId: "348679898788",
  appId: "1:348679898788:web:700a1fa4dbbbbe9fd40831",
  measurementId: "G-XRSV7DJQGD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Services
const auth = getAuth(app);
const db = getFirestore(app);

// Export for use in other files
export { app, auth, db };