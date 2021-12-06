import React, { useEffect, useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { useHistory } from "react-router";
import { auth, db, logout } from "../firebase";
import axios from "axios";

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
            // console.log(typeoaudio.concat(data.audio));
            setAudio( audio.concat(data.audio));
          }
          else{
            setAudio([])
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
      const downloadClip = async (name) => {
        try {
          const response = await axios.post(
            "https://api-dev-z2scpwkwva-uc.a.run.app/retrieve_audio",
            {
              fileName: name,
            }
          );
          window.open(response.data);
        } catch (err) {
          console.log(err)
        }
      }
      var audioList = audio.map( value => {
            const res = Object.entries(value);
            console.log(res)
            return (
              <button key="{res}" onClick={() => downloadClip(res[0][1])}>
                {res[0][0]}
              </button>
            );
          })
    return (
        <>
        <h1 className="dashboard-header text-center">
            Rediscover your voice
        </h1>
        <h2 className="dashboard-header text-center">
            Click to download your voice!
        </h2>
        <br/>
       {audioList}
        </>
    )

}

export default Retrieve;