import React, { Component } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { resetPassword } from "../../services/user";
import "./ForgotPassword.scss";
export default class ForgotPassword extends Component {
  constructor(params) {
    super(params);
    this.state = {
      title: "Введите email",
      phone: "",
      email: "",
      code: "",
      mailSent: false
    };
  }
  resetPassword = e => {
    e.preventDefault();
    const { email } = this.state;
    resetPassword(email)
      .then(data => {
        this.setState({
          title: "На вашу почту отправлено письмо с подтверждением",
          mailSent: true
        });
      })
      .catch(error => {
        console.log(error);
      });
  };
  render() {
    return (
      <div classNam="ForgotPassword">
        <Container>
          <Row>
            <Col lg={12} md={12} sm={12}>
              <h1 className="ForgotPassword__title">{this.state.title}</h1>
              {!this.state.mailSent ? (
                <form
                  onSubmit={this.resetPassword}
                  className="ForgotPassword__form"
                >
                  <p className="ForgotPassword__description">
                    для восстановления пароля
                  </p>
                  <input
                    value={this.state.email}
                    onChange={e => {
                      this.setState({
                        email: e.target.value
                      });
                    }}
                    placeholder="Email"
                    className="ForgotPassword__input"
                    type="text"
                  />
                  <button
                    className="ForgotPassword__button"
                    onClick={this.resetPassword}
                  >
                    Отправить код
                  </button>
                </form>
              ) : (
                ""
              )}
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}
