import { Form } from "react-bootstrap";
import { auth } from "../firebase";
import { useHistory } from "react-router";
import { useAuthState } from "react-firebase-hooks/auth";
import React, { useEffect } from "react";
import axios from "axios";
const url=require('../settings')

// Loading Wheel Functions are from: https://stackoverflow.com/questions/19315149/implementing-a-loading-spinning-wheel-in-javascript
// Author: Jared Goodwin
// showLoading() - Display loading wheel.
// removeLoading() - Remove loading wheel.
// Requires ECMAScript 6 (any modern browser).
function showLoading() {
  if (document.getElementById("divLoadingFrame") != null) {
    return;
  }
  var style = document.createElement("style");
  style.id = "styleLoadingWindow";
  style.innerHTML = `
        .loading-frame {
            position: fixed;
            background-color: rgba(0, 0, 0, 0.8);
            left: 0;
            top: 0;
            right: 0;
            bottom: 0;
            z-index: 4;
        }

        .loading-track {
            height: 50px;
            display: inline-block;
            position: absolute;
            top: calc(50% - 50px);
            left: 50%;
        }

        .loading-dot {
            height: 5px;
            width: 5px;
            background-color: white;
            border-radius: 100%;
            opacity: 0;
        }

        .loading-dot-animated {
            animation-name: loading-dot-animated;
            animation-direction: alternate;
            animation-duration: .75s;
            animation-iteration-count: infinite;
            animation-timing-function: ease-in-out;
        }

        @keyframes loading-dot-animated {
            from {
                opacity: 0;
            }

            to {
                opacity: 1;
            }
        }
    `
  document.body.appendChild(style);
  var frame = document.createElement("div");
  frame.id = "divLoadingFrame";
  frame.classList.add("loading-frame");
  for (var i = 0; i < 10; i++) {
    var track = document.createElement("div");
    track.classList.add("loading-track");
    var dot = document.createElement("div");
    dot.classList.add("loading-dot");
    track.style.transform = "rotate(" + String(i * 36) + "deg)";
    track.appendChild(dot);
    frame.appendChild(track);
  }
  document.body.appendChild(frame);
  var wait = 0;
  var dots = document.getElementsByClassName("loading-dot");
  for (var i = 0; i < dots.length; i++) {
    window.setTimeout(function(dot) {
      dot.classList.add("loading-dot-animated");
    }, wait, dots[i]);
    wait += 150;
  }
};

function removeLoading() {
  document.body.removeChild(document.getElementById("divLoadingFrame"));
  document.body.removeChild(document.getElementById("styleLoadingWindow"));
};

document.addEventListener('keydown', function(e) {
  if (e.keyCode === 27) {
    removeLoading();
  }
}, false);

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
    showLoading();
    axios
      .post((url+"/upload_audio"), formData, 
      
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: token,
        },
        
      })
      .then((response) => {
        alert("Uploaded Successfully");
        removeLoading();
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
