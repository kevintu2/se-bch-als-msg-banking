import { Form } from "react-bootstrap";
import { auth } from "../firebase";
import { useHistory } from "react-router";
import { useAuthState } from "react-firebase-hooks/auth";
import React, { useEffect } from "react";
import axios from "axios";

function Upload() {
  const [user, loading] = useAuthState(auth);
  const [file, setFile] = React.useState();
  const [title] = React.useState();
  const history = useHistory();
  useEffect(() => {
    if (loading) {
      // maybe trigger a loading screen
      return;
    }
    if (!user) history.replace("/home");
  }, [user, loading]);
  const submitAudio = async (event) => {
    event.preventDefault();
    let formData = new FormData();
    formData.append("file", file);
    formData.append("fileName", title);
    console.log(file);
    const token = await auth.currentUser.getIdToken();
    axios
      .post("http://localhost:8080/upload_audio", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: token,
        },
      })
      .then((response) => {
        alert("Uploaded Successfully");
        console.log(response);
      })
      .catch((error) => {
        // error response
        console.log(error);
      });
  };

  return (
    <div>
      <Form enctype="multipart/form-data">
        <Form.Group controlId="formFile" class="col-lg-6 offset-lg-3">
          <div className="row justify-content-center">
            <Form.Label>Upload your data</Form.Label>
            <Form.Control
              type="file"
              style={{ width: "50%" }}
              name="file"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <Form.Control
              type="submit"
              onClick={submitAudio}
              style={{ width: "20%", backgroundColor: "#2ca6a4" }}
            />
          </div>
        </Form.Group>
      </Form>
    </div>
  );
}

export default Upload;
