import { getAnalytics } from "firebase/analytics";
import firebase from "firebase/compat/app";
import 'firebase/compat/auth';
import 'firebase/compat/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyBsq899DDVYofdoPCf2bqVBwHw_lvhejyE",
    authDomain: "als-message-banking.firebaseapp.com",
    projectId: "als-message-banking",
    storageBucket: "als-message-banking.appspot.com",
    messagingSenderId: "490757581389",
    appId: "1:490757581389:web:f9b333a23d6ab25a4cca04",
    measurementId: "G-YX8E8LDL9S"
  };
  
  const app = firebase.initializeApp(firebaseConfig);
  const auth = app.auth();
  const db = app.firestore();
  const analytics = getAnalytics(app);
  const googleProvider = new firebase.auth.GoogleAuthProvider();
  
  const signInWithGoogle = async () => {
    try {
      const res = await auth.signInWithPopup(googleProvider);
      const user = res.user;
      const query = await db
        .collection("users")
        .where("uid", "==", user.uid)
        .get();
      if (query.docs.length === 0) {
        await db.collection("users").add({
          uid: user.uid,
          name: user.displayName,
          authProvider: "google",
          email: user.email,
        });
      }
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
    logout,
  };