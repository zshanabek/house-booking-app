import React, { Component } from "react";
import { resetPasswordConfirm } from "../../services/user";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

export default class ForgotPasswordConfirm extends Component {
  constructor(params) {
    super(params);
    this.state = {
      title: "Введите новый пароль",
      passwordChanged: false,
      new_password: "",
      re_new_password: ""
    };
  }
  componentDidMount() {
    const paramsUrl = new URLSearchParams(this.props.location.search);
    const params = {};
    for (var pair of paramsUrl.entries()) {
      params[pair[0]] = pair[1];
    }
    this.setState(params);
  }

  confirmPassword = e => {
    e.preventDefault();
    let data = new FormData();
    const { uid, token, new_password, re_new_password } = this.state;
    data.append("uid", uid);
    data.append("token", token);
    data.append("new_password", new_password);
    data.append("re_new_password", re_new_password);
    resetPasswordConfirm(data)
      .then(data => {
        this.setState({
          title: "Ваш пароль успешно изменен",
          passwordChanged: true,
          uid: "",
          token: ""
        });
      })
      .catch(error => {
        console.log(error);
      });
  };

  render() {
    const { new_password, re_new_password, passwordChanged } = this.state;

    return (
      <div className="ForgotPassword">
        <Container>
          <Row>
            <Col lg={12} md={12} sm={12}>
              <h1 className="ForgotPassword__title">{this.state.title}</h1>
              {!passwordChanged ? (
                <form
                  onSubmit={this.resetPassword}
                  className="ForgotPassword__form"
                >
                  <p className="ForgotPassword__description">
                    Пароль должен состоять минимум из 8<br /> символов и
                    содержать минимум одну большую
                    <br /> букву и одну маленькую букву.
                  </p>
                  <input
                    value={this.state.new_password}
                    onChange={e => {
                      this.setState({
                        new_password: e.target.value
                      });
                    }}
                    placeholder="Новый пароль"
                    className="ForgotPassword__input"
                    type="password"
                  />
                  <input
                    value={this.state.re_new_password}
                    onChange={e => {
                      this.setState({
                        re_new_password: e.target.value
                      });
                    }}
                    placeholder="Повторите пароль"
                    className="ForgotPassword__input"
                    type="password"
                  />
                  <button
                    className="ForgotPassword__button"
                    onClick={this.confirmPassword}
                    disabled={
                      !new_password ||
                      !re_new_password ||
                      new_password !== re_new_password
                    }
                  >
                    Изменить пароль
                  </button>
                </form>
              ) : (
                <div></div>
              )}
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}
