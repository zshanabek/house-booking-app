import React, { Component } from "react";
import { connect } from "react-redux";

import { Switch, Route, withRouter } from "react-router-dom";

import Profile from "./profile/Profile";
import MyHouses from "./myhouses/MyHouses";
import MyHouse from "./myhouse/MyHouse";
import EditHouse from "./edithouse/EditHouse";
import NewHouse from "./newhouse/NewHouse";
import Support from "./support/Support";
import Report from "./report/Report";
import About from "./about/About";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import Sidebar from "./sidebar/Sidebar";
import {
  getAccommodations,
  getHouseTypes,
  getNearBuildings,
  getRules,
  getCountries,
  getRegions
} from "../../actions/reference.action";

import "./User.scss";
import Orders from "./orders/Orders";

class User extends Component {
  componentDidMount() {
    const {
      getAccommodations,
      getHouseTypes,
      getNearBuildings,
      getRules,
      getCountries,
      getRegions
    } = this.props;
    getCountries();
    getRegions();
    getAccommodations();
    getHouseTypes();
    getNearBuildings();
    getRules();
  }
  render() {
    return (
      <div className="User">
        <Container>
          <Row>
            <Col lg={3}>
              <Sidebar path={this.props.location.pathname} />
            </Col>
            <Col lg={9}>
              <Switch>
                <Route exact path="/profile" component={Profile} />
                <Route exact path="/myhouses" component={MyHouses} />
                <Route exact path="/orders" component={Orders} />
                <Route exact path="/myhouse/:id" component={MyHouse} />
                <Route exact path="/edithouse/:id" component={EditHouse} />
                <Route exact path="/newhouse" component={NewHouse} />
                <Route exact path="/support" component={Support} />
                <Route exact path="/report" component={Report} />
                <Route exact path="/about" component={About} />
              </Switch>
            </Col>
          </Row>

          <div></div>
        </Container>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    reference: state.reference
  };
}

export default connect(mapStateToProps, {
  getAccommodations,
  getHouseTypes,
  getNearBuildings,
  getRules,
  getCountries,
  getRegions
})(withRouter(User));
