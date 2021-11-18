import {Form} from 'react-bootstrap';
import { auth, logout} from "../firebase";
import { useHistory } from "react-router";
import { useAuthState } from "react-firebase-hooks/auth";
import React, {useEffect} from 'react';

function Upload() {
    const [user, loading, error] = useAuthState(auth);

    const submitAudio = () => {
        
    }

    const history = useHistory();
    useEffect(() => {
        if (loading) {
          // maybe trigger a loading screen
          return;
        }
        if (!user) history.replace("/home");
      }, [user, loading]);
    return (
        <div>
            <Form.Group controlId="formFile" class="col-lg-6 offset-lg-3" >
                <div className="row justify-content-center">
                    <Form.Label>Label your File</Form.Label>
                    <Form.Control type="input" style={{width:'50%'}} name="title"></Form.Control>
                    <Form.Label>Upload your data</Form.Label>
                    <Form.Control type="file" style={{width:'50%'}} name="fileName"/>
                    <Form.Control type="submit" onClick={submitAudio} style={{width:'20%', backgroundColor:'#2ca6a4'}}/>
                </div>
            </Form.Group>
        </div>
    );
}

export default Upload;