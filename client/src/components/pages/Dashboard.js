import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useHistory } from "react-router";
import { auth, db, logout } from "../firebase";

import { Button } from "react-bootstrap";
import "./Dashboard.css";

function Dashboard() {
  const [user, loading] = useAuthState(auth);
  const [name, setName] = useState("");
  const history = useHistory();
  const fetchUserName = async () => {
    try {
      const query = await db
        .collection("users")
        .where("uid", "==", user?.uid)
        .get();
      if (query.docs.length > 0) {
        const data = await query.docs[0].data();
        setName(data.name);
      }
    } catch (err) {
      console.error(err);
    }
  };
  useEffect(() => {
    if (loading) return;
    if (!user) return history.replace(process.env.PUBLIC_URL + "/");
    fetchUserName();
  }, [user, loading]);
  return (
    <>
      <h1 className="dashboard-header text-center">Rediscover Your Voice</h1>
      <h2 className="dashboard-header text-center">ALS Voice Editing</h2>
      <br />
      <div class="col-md-12 text-center">
        <Button
          className="align-center"
          href={process.env.PUBLIC_URL + "/Upload"}
        >
          Upload your audio
        </Button>
        <br />
        <Button
          className="align-center mt-2"
          href={process.env.PUBLIC_URL + "/retrieve"}
        >
          Retrieve your audio
        </Button>
        <br />
        Logged in as
        <div>{name}</div>
        <div>{user?.email}</div>
        <Button onClick={logout}>Logout</Button>
      </div>
    </>
  );
}

export default Dashboard;
