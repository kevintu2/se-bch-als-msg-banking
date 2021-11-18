import React, { useEffect, useState } from "react";
import { Link, useHistory } from "react-router-dom";
import { auth, signInWithFacebook, signInWithGoogle } from "../firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, loading, error] = useAuthState(auth);
  const history = useHistory();
  useEffect(() => {
    if (loading) {
      // maybe trigger a loading screen
      return;
    }
    if (user) history.replace(process.env.PUBLIC_URL + "/dashboard");
  }, [user, loading]);
  return (
    <>
    <div>
      <h1 className="login-header text-center">
        Login to use ALS Message Banking services
      </h1>
    </div>
    <div className="login">
      <div className="login__container">
        <button className="login__btn login__google" onClick={signInWithGoogle}>
          Login with Google
        </button>
        <button className="login__btn login__facebook" onClick={signInWithFacebook} style={{textDecoration:'line-through'}}>
          Login with Facebook
        </button>
      </div>
    </div>
    </>
  );
}
export default Login;