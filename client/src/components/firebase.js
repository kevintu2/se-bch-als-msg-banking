import { getAnalytics } from "firebase/analytics";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";
import "firebase/compat/firestore";
import axios from "axios";

const firebaseConfig = {
  apiKey: "AIzaSyBsq899DDVYofdoPCf2bqVBwHw_lvhejyE",
  authDomain: "als-message-banking.firebaseapp.com",
  projectId: "als-message-banking",
  storageBucket: "als-message-banking.appspot.com",
  messagingSenderId: "490757581389",
  appId: "1:490757581389:web:f9b333a23d6ab25a4cca04",
  measurementId: "G-YX8E8LDL9S",
};

const app = firebase.initializeApp(firebaseConfig);
const auth = app.auth();
const db = app.firestore();
const analytics = getAnalytics(app);
const googleProvider = new firebase.auth.GoogleAuthProvider();
const facebookProvider = new firebase.auth.FacebookAuthProvider();

const signInWithEmailAndPassword = async (email, password) => {
  try {
    await auth.signInWithEmailAndPassword(email, password);
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};

const registerWithEmailAndPassword = async (name, email, password) => {
  try {
    const res = await auth.createUserWithEmailAndPassword(email, password);
    res.user.getIdTokenResult().then(async (idTokenResult) => {
      const user = res.user;
      const token = "Bearer " + idTokenResult.token;
      console.log(token);
      const response = await axios.post(
        "https://api-dev-z2scpwkwva-uc.a.run.app/register",
        {
          uid: user.uid,
          name: name,
          authProvider: "email",
          email: user.email,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: token,
          },
        }
      );
      console.log(response);
    });
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};

const sendPasswordResetEmail = async (email) => {
  try {
    await auth.sendPasswordResetEmail(email);
    alert("Password reset link sent!");
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};

const signInWithGoogle = async () => {
  try {
    const res = await auth.signInWithPopup(googleProvider);
    res.user.getIdTokenResult().then(async (idTokenResult) => {
      const user = res.user;
      const token = "Bearer " + idTokenResult.token;
      console.log(token);
      const response = await axios.post(
        "https://api-dev-z2scpwkwva-uc.a.run.app/register",
        {
          uid: user.uid,
          name: user.displayName,
          authProvider: "google",
          email: user.email,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: token,
          },
        }
      );
      console.log(response);
    });
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};

const signInWithFacebook = async () => {
  try {
    const res = await auth.signInWithPopup(facebookProvider);
    res.user.getIdTokenResult().then(async (idTokenResult) => {
      const user = res.user;
      const token = "Bearer " + idTokenResult.token;
      console.log(token);
      const response = await axios.post(
        "https://api-dev-z2scpwkwva-uc.a.run.app/register",
        {
          uid: user.uid,
          name: user.displayName,
          authProvider: "facebook",
          email: user.email,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: token,
          },
        }
      );
      console.log(response);
    });
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};

const logout = () => {
  auth.signOut();
};

export {
  auth,
  analytics,
  db,
  signInWithGoogle,
  signInWithFacebook,
  signInWithEmailAndPassword,
  registerWithEmailAndPassword,
  sendPasswordResetEmail,
  logout,
};
