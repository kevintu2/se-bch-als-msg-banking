import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useHistory } from "react-router";
import { auth, db, logout } from "../firebase";

import {Button} from 'react-bootstrap';

function Retrieve() {
    const [user, loading, error] = useAuthState(auth);
    const [audio, setAudio] = useState([]);
    const history = useHistory();
    const fetchUserAudio = async () => {
        try {
          const query = await db
            .collection("users")
            .where("uid", "==", user?.uid)
            .get();
          const data = await query.docs[0].data();
          if ("audio" in data){
            setAudio( data.audio);
          }
          else{
            setAudio(audio => [])
          }
        } catch (err) {
          console.error(err);
          alert("An error occured while fetching user data");
        }
      };
      useEffect(() => {
        if (loading) return;
        if (!user) return history.replace(process.env.PUBLIC_URL +"/");
        fetchUserAudio();
      },[loading]);
      console.log(audio[0])
     if (audio.length >0){
      var audioList = audio.map(clip =>{
            return <li key="{clip}">{clip.key}</li>;
          })
    }
    return (
        <>
        <h1 className="dashboard-header text-center">
            Rediscover your voice
        </h1>
        <h2 className="dashboard-header text-center">
            Click to download your voice!
        </h2>
        <br/>
        {audio ? audio.map(clip =>
             <li key="{clip}">{clip}</li>
          ): 'Loading...'}
        {/* {audio.length > 0 &&
        <ul>{audioList}</ul> */}
{/* } */}
        </>
    )

}

export default Retrieve;