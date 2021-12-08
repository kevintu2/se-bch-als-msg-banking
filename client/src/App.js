import "./App.css";
import MainNav from "./components/Navbar";
import Home from "./components/pages/Home";
import Upload from "./components/pages/Upload";
import Dashboard from "./components/pages/Dashboard";
import Login from "./components/pages/Login";
import Register from "./components/pages/Register";
import Reset from "./components/pages/Reset";
import Retrieve from "./components/pages/Retrieve";

import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "bootstrap/dist/css/bootstrap.min.css";

import React from "react";

function App() {
  return (
    <div>
      <Router>
        <MainNav />
        <br />
        <Switch>
          <Route exact path={process.env.PUBLIC_URL + "/"} component={Home} />
          <Route path={process.env.PUBLIC_URL + "/upload"} component={Upload} />
          <Route
            path={process.env.PUBLIC_URL + "/retrieve"}
            component={Retrieve}
          />
          <Route
            path={process.env.PUBLIC_URL + "/dashboard"}
            component={Dashboard}
          />
          <Route path={process.env.PUBLIC_URL + "/login"} component={Login} />
          <Route
            path={process.env.PUBLIC_URL + "/register"}
            component={Register}
          />
          <Route
            path={process.env.PUBLIC_URL + "/reset"}
            component={Reset}
          ></Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
