import {Form} from 'react-bootstrap';
import { auth, logout} from "../firebase";
import { useHistory } from "react-router";
import { useAuthState } from "react-firebase-hooks/auth";
import React, {useEffect} from 'react';

function Upload() {
    const [user, loading, error] = useAuthState(auth);
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
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Upload your data</Form.Label>
                <Form.Control type="file" />
            </Form.Group>
        </div>
    );
}

export default Upload;