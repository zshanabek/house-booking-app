import React, { Component, Fragment } from "react";
import { connect } from "react-redux";

import "./App.scss";

import { Switch, Route, withRouter, Redirect } from "react-router-dom";
import { getCurrentUser } from "../../actions/user.action";
import { getCities, getAccommodations } from "../../actions/reference.action";

import Header from "../header/Header";
import Main from "../main/Main";
import Results from "../results/Results";
import Saved from "../saved/Saved";
import Reservations from "../reservations/Reservations";
import Housing from "../housing/Housing";
import Houses from "../houses/Houses";
import Footer from "../footer/Footer";
import User from "../user/User";
import Chat from "../chat/Chat";
import ForgotPassword from "../forgotPassword/ForgotPassword";
import ForgotPasswordConfirm from "../forgotPassword/ForgotPasswordConfirm";
import PrivacyPolicy from "../privacyPolicy/PrivacyPolicy";
import Dev from "../dev/Dev";

function PrivateRoute({ component: Component, isAuthenticated, ...rest }) {
  return (
    <Route
      {...rest}
      render={props =>
        isAuthenticated === true ? (
          <Component {...props} />
        ) : (
          <Redirect to={{ pathname: "/", state: { signInModal: true } }} />
        )
      }
    />
  );
}

class App extends Component {
  componentDidMount() {
    const token = localStorage.getItem("token");
    const { getCurrentUser, getCities, getAccommodations } = this.props;
    if (token !== null) {
      getCurrentUser();
    }
    getCities();
    getAccommodations();
  }
  render() {
    const { auth } = this.props;
    return (
      <Fragment>
        <Header />
        <div className="App">
          <Switch>
            <Route exact path="/dev" component={Dev} />
            <Route exact path="/" component={Main} />
            <Route exact path="/privacy_policy" component={PrivacyPolicy} />
            <Route exact path="/forgot_password" component={ForgotPassword} />
            <Route
              exact
              path="/forgot_password/confirm"
              component={ForgotPasswordConfirm}
            />
            <Route exact path="/results" component={Results} />
            <Route exact path="/housing/:id" component={Housing} />
            <Route exact path="/houses/:type_id" component={Houses} />

            <PrivateRoute
              exact
              path="/saved"
              component={Saved}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/reservations"
              component={Reservations}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/chat"
              component={Chat}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/profile"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/myhouses"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/orders"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/myhouse/:id"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/edithouse/:id"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/newhouse"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/support"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/report"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
            <PrivateRoute
              exact
              path="/about"
              component={User}
              isAuthenticated={auth.isAuthenticated}
            />
          </Switch>
        </div>
        <Footer />
      </Fragment>
    );
  }
}

function mapStateToProps(state) {
  return {
    auth: state.auth,
    user: state.auth.user
  };
}

export default connect(mapStateToProps, {
  getCurrentUser,
  getCities,
  getAccommodations
})(withRouter(App));
