import React from 'react';
import {Navbar, Nav, Container} from 'react-bootstrap';
import Image from 'react-bootstrap/Image';
import styled from "styled-components";
import BCHlogo from "./assets/BCHlogo.png";
import "./Navbar.css";

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
    return (
        <>
        <Styles>
          <Navbar className="navbar-custom block-example border-bottom border-dark shadow">
              <Container>
                  <Navbar.Brand href="https://www.childrenshospital.org/" style={{color:'#1b4079'}}>
                  <Image src={BCHlogo} alt="Logo"/>
                  ALS Message Ediging</Navbar.Brand>
                    <Nav className="me-auto">
                        <Nav.Link href="/">Home</Nav.Link>
                        <Nav.Link href="/upload">Upload</Nav.Link>
                        <Nav.Link href="/about">About Us</Nav.Link>
                    </Nav>
                    <Nav className="ml-auto">
                      <Nav.Link href="/login" className="login-item" style={{}}>Log In</Nav.Link>
                    </Nav>
              </Container>
              </Navbar>
            </Styles>
            </>
    )
}

export default MainNav;