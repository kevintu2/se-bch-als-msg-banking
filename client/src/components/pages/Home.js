import React, { useEffect } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useHistory } from "react-router";
import { auth } from "../firebase";
import "./Home.css";

function Home() {
  const [user, loading] = useAuthState(auth);
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
      <h1 className="home-header text-center">Rediscover your voice</h1>
      <h2 className="home-header text-center">ALS Voice Editing</h2>
    </>
  );
}

export default Home;
