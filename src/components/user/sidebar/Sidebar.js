import React, { Component, Fragment } from "react";
import { connect } from "react-redux";

import { withRouter } from "react-router-dom";

import "./Sidebar.scss";
class Sidebar extends Component {
  goToProfile = () => {
    this.props.history.push("/profile");
  };
  goToMyAds = () => {
    this.props.history.push("/myhouses");
  };
  goToOrders = () => {
    this.props.history.push("/orders");
  };
  goToSupport = () => {
    this.props.history.push("/support");
  };
  goToAbout = () => {
    this.props.history.push("/about");
  };

  render() {
    const { user } = this.props;
    const path = this.props.path.replace("/", "");
    return (
      <div className="Sidebar">
        <button
          onClick={this.goToProfile}
          className={`Sidebar__button ${
            path === "profile" ? "Sidebar__active" : ""
          }`}
        >
          Мой профиль
        </button>
        {user && user.user_type === 1 ? (
          <Fragment>
            <button
              onClick={this.goToMyAds}
              className={`Sidebar__button ${
                path === "myhouses" || path === "newhouse"
                  ? "Sidebar__active"
                  : ""
              }`}
            >
              Мои объявления
            </button>
            <button
              onClick={this.goToOrders}
              className={`Sidebar__button ${
                path === "orders" ? "Sidebar__active" : ""
              }`}
            >
              Заявки
            </button>
          </Fragment>
        ) : null}

        <button
          onClick={this.goToSupport}
          className={`Sidebar__button ${
            path === "support" || path === "report" ? "Sidebar__active" : ""
          }`}
        >
          Поддержка
        </button>
        <button
          onClick={this.goToAbout}
          className={`Sidebar__button ${
            path === "about" ? "Sidebar__active" : ""
          }`}
        >
          О нас
        </button>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    user: state.auth.user
  };
}

export default connect(mapStateToProps, null)(withRouter(Sidebar));
