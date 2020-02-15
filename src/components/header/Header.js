import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import {
  signIn,
  signUp,
  toggleSignInModal,
  toggleSignUpModal,
  toggleLoading,
  verifyPhone,
  toggleConfirmNumberModal,
  updateUserData
} from "../../actions/user.action";
import { sendCode } from "../../services/user";
import InputMask from "react-input-mask";
import logo from "../../assets/images/akv-logo-kz.png";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import { faAngleDown, faPlus } from "@fortawesome/free-solid-svg-icons";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { signOut } from "../../actions/user.action";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Dropdown from "react-bootstrap/Dropdown";
import "./Header.scss";

const CustomToggle = React.forwardRef((props, ref) => (
  <li
    ref={ref}
    className={`Header__nav-item ${
      props.path === "profile" ||
      props.path === "support" ||
      props.path === "about" ||
      props.path === "newhouse" ||
      props.path === "myhouses" ||
      props.path === "myhouse"
        ? "Header__nav-item--active"
        : ""
    }`}
    onClick={e => {
      e.preventDefault();
      props.onClick(e);
    }}
  >
    {props.children}
  </li>
));

class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      signIn: {
        firstCredential: "",
        password: ""
      },
      signUp: {
        email: "",
        phone: "",
        gender: 1,
        first_name: "",
        last_name: "",
        birth_day: "",
        password: "",
        confirmPassword: ""
      },
      nav_expanded: false,
      profileDropdown: false,
      confirmNumberTimer: 60,
      confirmNumberCode: null
    };
  }

  componentDidMount() {
    // document.addEventListener("click", this.handleDocumentClick, true);
  }
  toggleUserType = () => {
    const { updateUserData, user } = this.props;
    let formData = new FormData();
    formData.append("user_type", !user.user_type === false ? 0 : 1);
    updateUserData(formData);
  };
  handleDocumentClick = e => {
    const container = this._element;
    if (e.target !== container && !container.contains(e.target)) {
      this.setState({
        nav_expanded: false
      });
    }
  };
  onSignInChangeHandler = e => {
    let { name, value } = e.target;
    this.setState({
      signIn: {
        ...this.state.signIn,
        [name]: value
      }
    });
  };
  signInHandler = e => {
    e.preventDefault();
    const { signIn, toggleLoading } = this.props;
    const { firstCredential, password } = this.state.signIn;
    let signInFormDate = new FormData();
    signInFormDate.append("phone", firstCredential);
    signInFormDate.append("password", password);
    toggleLoading();
    signIn(signInFormDate);
  };
  onSignUpChangeHandler = e => {
    let { name, value } = e.target;

    switch (name) {
      case "confirmPassword":
        this.setState({
          signUp: {
            ...this.state.signUp,
            [name]: value,
            [name + "Error"]: value !== this.state.signUp.password
          }
        });
        break;
      case "gender":
        let genderValue = value === "Мужской" ? 1 : 0;
        this.setState({
          signUp: {
            ...this.state.signUp,
            [name]: genderValue
          }
        });
        break;
      default:
        this.setState({
          signUp: {
            ...this.state.signUp,
            [name]: value
          }
        });
        break;
    }
  };
  signUpHandler = e => {
    e.preventDefault();
    const { signUp, toggleLoading } = this.props;
    const {
      email,
      phone,
      gender,
      first_name,
      last_name,
      birth_day,
      password,
      confirmPassword
    } = this.state.signUp;

    let signUpFormDate = new FormData();
    signUpFormDate.append("email", email);
    signUpFormDate.append("phone", phone);
    signUpFormDate.append("gender", gender);
    signUpFormDate.append("first_name", first_name);
    signUpFormDate.append("last_name", last_name);
    signUpFormDate.append("birth_day", birth_day);
    signUpFormDate.append("password", password);
    signUpFormDate.append("re_password", confirmPassword);
    toggleLoading();
    localStorage.setItem("verify_phone", phone);
    signUp(signUpFormDate);
    this.startConfirmNumberTimer();
  };
  signUpBlurHandler = e => {
    let name = e.target.name;
    let label = name + "Error";

    this.setState({
      signUp: {
        ...this.state.signUp,
        [label]:
          this.state.signUp[name] === "" ||
          (name === "phone" && this.state.signUp[name] === "+7(   )-   -  -  ")
      }
    });
  };

  startConfirmNumberTimer = () => {
    let confirmNumberInterval = setInterval(() => {
      if (this.state.confirmNumberTimer === 0) {
        clearInterval(confirmNumberInterval);
      } else {
        this.setState({
          confirmNumberTimer: this.state.confirmNumberTimer - 1
        });
      }
    }, 1000);
  };
  requestCode = () => {
    const { phone } = this.props.user;
    sendCode(phone);
  };
  verifyPhone = () => {
    const { phone } = this.props.user;
    const { verifyPhone } = this.props;
    verifyPhone(phone, this.state.confirmNumberCode);
  };

  profileDropdownChangeHandler = () => {
    this.setState({
      profileDropdown: !this.state.profileDropdown
    });
  };

  goToMain = () => {
    this.props.history.push("/");
  };
  goToForgotPassword = e => {
    e.preventDefault();
    this.props.toggleSignInModal();
    this.props.history.push("/forgot_password");
  };
  goToNewHouse = () => {
    this.props.history.push("/newhouse");
  };
  goToSaved = () => {
    this.props.history.push("/saved");
  };
  goToMyAds = () => {
    this.props.history.push("/myhouses");
  };
  goToOrders = () => {
    this.props.history.push("/orders");
  };
  goToReservations = () => {
    this.props.history.push("/reservations");
  };
  goToProfile = () => {
    this.props.history.push("/profile");
  };
  goToSupport = () => {
    this.props.history.push("/support");
  };
  goToAbout = () => {
    this.props.history.push("/about");
  };
  goToChat = () => {
    this.props.history.push("/chat");
  };
  logOut = () => {
    const { signOut } = this.props;
    signOut();
  };
  goToNewHouse = () => {
    this.props.history.push("/newhouse");
  };
  goToPrivacyPolicy = () => {
    this.props.history.push("/privacy_policy");
  };
  render() {
    const { auth, user } = this.props;
    const path = this.props.history.location.pathname.replace("/", "");
    return (
      <Fragment>
        <Navbar
          fixed="top"
          className="Header justify-content-between"
          collapseOnSelect
          expand="lg"
          bg="#fff"
          expanded={this.state.nav_expanded}
          onToggle={() => {
            this.setState({
              nav_expanded: !this.state.nav_expanded
            });
          }}
          id="header"
        >
          <Navbar.Brand href="http://akv.kz">
            <img className="Header__logo" src={logo} alt="logo" />
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ml-auto">
              <li
                onClick={this.goToMain}
                className={`Header__nav-item ${
                  path === "" ? "Header__nav-item--active" : ""
                }`}
              >
                Главная
              </li>
              {user ? (
                <Fragment>
                  <li
                    onClick={this.goToSaved}
                    className={`Header__nav-item ${
                      path === "saved" ? "Header__nav-item--active" : ""
                    }`}
                  >
                    Сохранённые
                  </li>
                  <li
                    onClick={this.goToReservations}
                    className={`Header__nav-item ${
                      path === "reservations" ? "Header__nav-item--active" : ""
                    }`}
                  >
                    Мои бронирования
                  </li>
                  <li
                    onClick={this.goToChat}
                    className={`Header__nav-item ${
                      path === "chat" ? "Header__nav-item--active" : ""
                    }`}
                  >
                    Сообщения
                  </li>
                  <Dropdown>
                    <Dropdown.Toggle
                      as={CustomToggle}
                      path={path}
                      id="dropdown-basic"
                    >
                      Мой профиль {"\u00A0"} <Fa icon={faAngleDown} />
                    </Dropdown.Toggle>

                    <Dropdown.Menu style={{ top: "50px" }}>
                      <div
                        onClick={this.goToProfile}
                        className="Header__collapse--item"
                      >
                        <img
                          className="Header__collapse--avatar"
                          src={user.userpic}
                          alt=""
                        />
                        <p className="Header__collapse--username">
                          {user.first_name}
                        </p>
                      </div>
                      <div
                        onClick={this.toggleUserType}
                        className="Header__collapse--item"
                      >
                        <p className="Header__collapse--title">Режим хозяина</p>
                        <div
                          className={`toggle ${
                            user.user_type ? "toggle--active" : ""
                          }`}
                        ></div>
                      </div>
                      {user && user.user_type === 1 ? (
                        <Fragment>
                          <div
                            onClick={this.goToMyAds}
                            className="Header__collapse--item"
                          >
                            <p className="Header__collapse--title">
                              Мои объявления
                            </p>
                          </div>
                          <div
                            onClick={this.goToOrders}
                            className="Header__collapse--item"
                          >
                            <p className="Header__collapse--title">Заявки</p>
                          </div>
                        </Fragment>
                      ) : null}
                      <div
                        onClick={this.goToSupport}
                        className="Header__collapse--item"
                      >
                        <p className="Header__collapse--title">Поддержка</p>
                      </div>
                      <div
                        onClick={this.goToAbout}
                        className="Header__collapse--item"
                      >
                        <p className="Header__collapse--title">О нас</p>
                      </div>
                      <div
                        onClick={this.logOut}
                        className="Header__collapse--item"
                      >
                        <p className="Header__collapse--title">
                          Выйти из аккаунта
                        </p>
                      </div>
                      {user && user.user_type === 1 ? (
                        <div className="Header__collapse--last">
                          <button
                            className="Header__collapse--button"
                            onClick={this.goToNewHouse}
                          >
                            <Fa icon={faPlus} />
                            {"\u00A0"}
                            Разместить обьявление
                          </button>
                        </div>
                      ) : null}
                    </Dropdown.Menu>
                  </Dropdown>
                </Fragment>
              ) : (
                <li
                  className="Header__nav-item"
                  onClick={() => this.props.toggleSignInModal()}
                >
                  Войти
                </li>
              )}
            </Nav>
          </Navbar.Collapse>
        </Navbar>

        <Modal
          size="lg"
          show={this.props.signInModal}
          onHide={() => this.props.toggleSignInModal()}
          centered={true}
        >
          <Modal.Body>
            <div className="Form__signIn">
              <h1 className="Form__title">Войдите в аккаунт</h1>
              <InputMask
                name="firstCredential"
                onChange={this.onSignInChangeHandler}
                value={this.state.signIn.firstCredential}
                mask="+79999999999"
                maskChar=""
              >
                {inputProps => (
                  <input
                    id="phoneInput"
                    className="Form__input"
                    {...inputProps}
                    type=""
                    placeholder="Номер телефона"
                  />
                )}
              </InputMask>
              <Form.Group
                style={{
                  display: "flex",
                  justifyContent: "flex-end",
                  flexDirection: "column"
                }}
              >
                <input
                  name="password"
                  className="Form__input"
                  type="password"
                  value={this.state.signIn.password}
                  onChange={this.onSignInChangeHandler}
                  placeholder="Пароль"
                />
                <button
                  onClick={this.goToForgotPassword}
                  className="Form__button--secondary Form__button--secondary-forgot"
                >
                  Забыли пароль?
                </button>
                <h6 className="Form__error">{auth.authError}</h6>
              </Form.Group>
              <button
                className="Form__button Form__button--login"
                onClick={this.signInHandler}
                type="submit"
              >
                {this.props.auth.loading ? "Подождите...." : "Войти"}
              </button>

              <button
                style={{ marginTop: "15px", marginBottom: "60px" }}
                className="Form__button--secondary"
                type="submit"
                onClick={e => {
                  e.preventDefault();
                  this.props.toggleSignInModal();
                  this.props.toggleSignUpModal();
                }}
              >
                Создать аккаунт
              </button>
            </div>
          </Modal.Body>
        </Modal>
        <Modal
          size="xl"
          show={this.props.signUpModal}
          onHide={() => this.props.toggleSignUpModal()}
          centered={true}
        >
          <Modal.Body>
            <h1 className="Form__title">Создайте аккаунт</h1>
            <Row>
              <Col>
                <form className="Form__signUp">
                  <Form.Group>
                    <label
                      htmlFor="phoneInput"
                      className={`Form__input-label ${
                        this.state.signUp.phoneError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      Номер телефона
                    </label>

                    <InputMask
                      name="phone"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.phone}
                      mask="+79999999999"
                      maskChar=""
                    >
                      {inputProps => (
                        <input
                          id="phoneInput"
                          className="Form__input"
                          {...inputProps}
                          type=""
                          placeholder="+7()"
                        />
                      )}
                    </InputMask>
                  </Form.Group>
                  <Form.Group>
                    <label
                      htmlFor="emailInput"
                      className={`Form__input-label ${
                        this.state.signUp.emailError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      Электроная почта
                    </label>
                    <input
                      id="emailInput"
                      name="email"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.email}
                      className="Form__input"
                      type="email"
                      placeholder="E-mail"
                    />
                  </Form.Group>
                  <Form.Group>
                    <label
                      className={`Form__input-label ${
                        this.state.signUp.passwordError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      Пароль
                    </label>
                    <input
                      name="password"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.password}
                      className="Form__input"
                      type="password"
                      placeholder="Придумайте пароль"
                    />
                    <Form.Group></Form.Group>
                    <label
                      className={`Form__input-label ${
                        this.state.signUp.confirmPasswordError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      Повторите пароль
                    </label>
                    <input
                      name="confirmPassword"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.confirmPassword}
                      className="Form__input"
                      type="password"
                      placeholder="Повторите свой пароль"
                    />
                  </Form.Group>

                  <h6
                    style={{ width: "300px", marginTop: "20px" }}
                    className=""
                  >
                    <button
                      className="Form__button--secondary"
                      type="submit"
                      onClick={e => {
                        e.preventDefault();
                        this.props.toggleSignInModal();
                        this.props.toggleSignUpModal();
                      }}
                    >
                      Войти в аккаунт
                    </button>
                  </h6>
                </form>
              </Col>
              <Col>
                <form className="Form__signUp">
                  <Form.Group>
                    <label
                      className={`Form__input-label ${
                        this.state.signUp.first_nameError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      Имя
                    </label>
                    <input
                      name="first_name"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.first_name}
                      className="Form__input"
                      type="text"
                      placeholder="Напишите ваше имя"
                    />
                  </Form.Group>
                  <Form.Group>
                    <label
                      className={`Form__input-label ${
                        this.state.signUp.last_nameError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      Фамилия
                    </label>
                    <input
                      name="last_name"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.last_name}
                      className="Form__input"
                      type="text"
                      placeholder="Напишите вашу фамилию"
                    />
                  </Form.Group>
                  <Form.Group>
                    <label
                      className={`Form__input-label ${
                        this.state.signUp.birth_dayError === true
                          ? "Form__input-label--error"
                          : ""
                      }`}
                    >
                      День рождение
                    </label>
                    <input
                      name="birth_day"
                      onBlur={this.signUpBlurHandler}
                      onChange={this.onSignUpChangeHandler}
                      value={this.state.signUp.birth_day}
                      className="Form__input"
                      type="date"
                      placeholder="ДД/ММ/ГГГГ"
                    />
                  </Form.Group>
                  <Form.Group>
                    <label className="Form__input-label">Пол</label>
                    <select
                      name="gender"
                      onChange={this.onSignUpChangeHandler}
                      value={
                        this.state.signUp.gender === 1 ? "Мужской" : "Женский"
                      }
                      className="Form__input"
                      type="password"
                      placeholder="Выберите пол"
                    >
                      <option>Мужской</option>
                      <option>Женский</option>
                    </select>
                  </Form.Group>

                  <p className="Form__policy">
                    Нажимая кнопку Создать, вы
                    <br />
                    соглашаетесь c{" "}
                    <span
                      onClick={this.goToPrivacyPolicy}
                      className="Form__policy--main"
                    >
                      политикой конфеденциальности
                    </span>{" "}
                    и{" "}
                    <span className="Form__policy--main">
                      правилами
                      <br /> пользования.
                    </span>
                  </p>

                  <h6 className="Form__error">{auth.authError}</h6>
                  <button
                    style={{ marginTop: "20px" }}
                    onClick={this.signUpHandler}
                    className="Form__button"
                    type="submit"
                  >
                    {this.props.auth.loading ? "Подождите...." : "Создать"}
                  </button>
                </form>
              </Col>
            </Row>
          </Modal.Body>
        </Modal>
        <Modal
          size="lg"
          show={this.props.confirmNumberModal}
          onHide={() => this.props.toggleConfirmNumberModal()}
          centered={true}
        >
          <Modal.Body>
            <h1 className="Form__title">
              Подтвердите
              <br /> номер телефона
            </h1>
            <Row>
              <Col>
                <div className="Form__confirm-number">
                  <p className="Form__confirm-number--description">
                    Мы отправим на ваш номер телефона
                    <br /> 4-значный код. Введите его для подтверждения
                    <br /> номера телефона.
                  </p>
                  <input
                    type="number"
                    className="Form__confirm-number--input"
                    value={this.state.confirmNumberCode}
                    onChange={e =>
                      this.setState({ confirmNumberCode: e.target.value })
                    }
                  />
                  <button
                    onClick={this.verifyPhone}
                    className="Form__confirm-number--button"
                  >
                    Подтвердить
                  </button>
                  {/* <p className="Form__confirm-number--text">
                    Мне не пришло сообщение с кодом.
                  </p>
                  {this.state.confirmNumberTimer === 0 ? (
                    <button
                      onClick={this.requestCode}
                      className="Form__confirm-number--resend"
                    >
                      Отправить ещё раз
                    </button>
                  ) : (
                    <button className="Form__confirm-number--timer">
                      Отправить можно через {this.state.confirmNumberTimer} сек.
                    </button>
                  )} */}
                </div>
              </Col>
            </Row>
          </Modal.Body>
        </Modal>
      </Fragment>
    );
  }
}

function mapStateToProps(state) {
  return {
    auth: state.auth,
    user: state.auth.user,
    signInModal: state.auth.signInModal,
    signUpModal: state.auth.signUpModal,
    confirmNumberModal: state.auth.confirmNumberModal
  };
}

export default connect(mapStateToProps, {
  signIn,
  signUp,
  toggleSignInModal,
  toggleSignUpModal,
  toggleLoading,
  toggleConfirmNumberModal,
  signOut,
  updateUserData,
  verifyPhone
})(withRouter(Header));
