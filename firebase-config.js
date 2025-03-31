// Import Firebase SDK
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBzLqzfcBHRctP2S5kZtmgFX093QQQc1Xc",
    authDomain: "recidivision-965ed.firebaseapp.com",
    projectId: "recidivision-965ed",
    storageBucket: "recidivision-965ed.appspot.com",
    messagingSenderId: "71333455858",
    appId: "1:71333455858:web:3e922eb37552ae64e86d6b"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { auth };
