import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyBGBl16QQlPr6N4P8XCw52yZcV2odKgA4Y",
  authDomain: "my-firebase-site-2a796.firebaseapp.com",
  projectId: "my-firebase-site-2a796",
  storageBucket: "my-firebase-site-2a796.firebasestorage.app",
  messagingSenderId: "1068971399528",
  appId: "1:1068971399528:web:9f4f7e3353aecffdebdedd"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
