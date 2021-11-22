import React from 'react';
import {Navbar, Nav, Container} from 'react-bootstrap';
import Image from 'react-bootstrap/Image';
import styled from "styled-components";
import BCHlogo from "./assets/BCHlogo.png";
import "./Navbar.css";

import { auth, logout} from "./firebase";
import { useAuthState } from "react-firebase-hooks/auth";

function MainNav() {
    const Styles = styled.div`
      .navbar-custom {
        background-color: #EEF5DB;
      }
      .navbar-light .nav-link {
        color: #2ca6a4;
        &:hover {
          color: black;
        }
      }
    `;

    const [user, loading, error] = useAuthState(auth);
    let button;
    if (user) {
      button = <Nav className="ml-auto"><Nav.Link onClick={logout} className="login-item">Log Out</Nav.Link></Nav>
    } else {
      button = <Nav className="ml-auto"><Nav.Link href={process.env.PUBLIC_URL+"/login"} className="login-item">Log In</Nav.Link></Nav>
    }
    return (
        <>
        <Styles>
          <Navbar className="navbar-custom block-example border-bottom border-dark shadow">
              <Container>
                  <Navbar.Brand href="https://www.childrenshospital.org/" style={{color:'#1b4079'}}>
                  <Image src={BCHlogo} alt="Logo"/>
                  ALS Message Ediging
                  </Navbar.Brand>
                  <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Nav className="me-auto">
                        <Nav.Link href={process.env.PUBLIC_URL + "/"}>Home</Nav.Link>
                        {user && <Nav.Link href={process.env.PUBLIC_URL + "/upload"}>Upload</Nav.Link>}
                        <Nav.Link href={process.env.PUBLIC_URL + "/about"}>About Us</Nav.Link>
                    </Nav>
                    {button}
              </Container>
              </Navbar>
            </Styles>
            </>
    )
}

export default MainNav;