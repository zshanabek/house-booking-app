import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import { format } from "date-fns";
import { ru as locale } from "date-fns/locale";
import Table from "react-bootstrap/Table";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import {
  faPencilAlt,
  faPlus,
  faInfoCircle
} from "@fortawesome/free-solid-svg-icons";
import Select from "react-select";
import { DateSingleInput } from "../../UIComponents/DatePicker";
import { updateUserData, signOut } from "../../../actions/user.action";
import InputMask from "react-input-mask";
import { correctGreen } from "../../../assets/images/images";

import { sendCode } from "../../../services/user";
import {
  verifyPhone,
  toggleConfirmNumberModal
} from "../../../actions/user.action";
import "./Profile.scss";

class Profile extends Component {
  constructor(props) {
    super(props);
    this.state = {
      edit: false,
      date: null,
      showDatepicker: false,
      first_name: null,
      last_name: null,
      user_type: null,
      birth_day: null,
      gender: null,
      phone: null,
      email: null,
      userpic: null,
      updatedUserData: {}
    };
  }
  userPicChangeHanlder = e => {
    const { updateUserData } = this.props;
    let formData = new FormData();
    formData.append("userpic", e.target.files[0], e.target.files[0].name);
    updateUserData(formData);
  };
  updateUserHandler = e => {
    const { updateUserData } = this.props;
    const { updatedUserData } = this.state;
    let formData = new FormData();

    for (let key in updatedUserData) {
      if (updatedUserData.hasOwnProperty(key)) {
        formData.append(key, updatedUserData[key]);
      }
    }
    updateUserData(formData);
    this.setState({
      edit: false,
      updatedUserData: {}
    });
  };
  editHandler = () => {
    this.setState({
      edit: true
    });
  };
  toggleUserType = () => {
    const { updateUserData, user } = this.props;
    let formData = new FormData();
    formData.append("user_type", !user.user_type === false ? 0 : 1);
    updateUserData(formData);
  };
  userProfileInputChangeHandler = e => {
    this.setState({
      [e.target.name]: e.target.value,
      updatedUserData: {
        ...this.state.updatedUserData,
        [e.target.name]: e.target.value
      }
    });
  };
  genderChangeHandler = e => {
    this.setState({
      updatedUserData: {
        ...this.state.updatedUserData,
        gender: e.value
      }
    });
  };
  convertDate = str => {
    var date = new Date(str),
      mnth = ("0" + (date.getMonth() + 1)).slice(-2),
      day = ("0" + date.getDate()).slice(-2);
    return [date.getFullYear(), mnth, day].join("-");
  };
  goToNewHouse = () => {
    this.props.history.push("/newhouse");
  };
  requestCode = () => {
    const { phone } = this.props.user;
    sendCode(phone);
  };
  logOut = () => {
    const { signOut } = this.props;
    signOut();
  };
  confirmPhoneNumber = () => {
    const { toggleConfirmNumberModal } = this.props;
    toggleConfirmNumberModal();
    this.requestCode();
  };
  render() {
    const { user } = this.props;

    if (user !== null) {
      return (
        <div>
          <h1 className="User__title">Мой профиль</h1>
          <div className="Profile__avatar">
            <img className="Profile__avatar--image" src={user.userpic} alt="" />

            <div className="Profile__avatar--overlay">
              <label htmlFor="profileAvatar" className="Profile__avatar--label">
                <Fa icon={faPencilAlt} />
              </label>
              <input
                id="profileAvatar"
                type="file"
                accept="image/png, image/jpeg"
                onChange={this.userPicChangeHanlder}
                className="Profile__avatar--edit"
              />
            </div>
          </div>
          <p className="Profile__username">
            {user.first_name} {user.last_name}
          </p>
          <div onClick={this.toggleUserType} className="Profile__toggle--block">
            <div
              className={`Profile__toggle ${
                user.user_type ? "Profile__toggle--active" : ""
              }`}
            ></div>
            <label className="Profile__toggle--label">Режим хозяина</label>
          </div>
          {this.state.edit ? (
            <button className="Profile__save" onClick={this.updateUserHandler}>
              Сохранить изменения
            </button>
          ) : (
            <button className="Profile__edit" onClick={this.editHandler}>
              Изменить профиль
            </button>
          )}
          {!user.is_active ? (
            <div className="Profile__confirm-phone">
              <p className="Profile__confirm-phone--alert">
                <Fa icon={faInfoCircle} /> Вы не подтвердили номер телефона.
                Нокоторые функции не будут работать.
              </p>
              <button
                onClick={this.confirmPhoneNumber}
                className="Profile__edit"
              >
                Подтвердить
              </button>
            </div>
          ) : (
            ""
          )}
          <Table bordered>
            <tbody>
              {this.state.edit ? (
                <Fragment>
                  <tr>
                    <td>Имя:</td>
                    <td>
                      <input
                        name="first_name"
                        placeholder="Введите имя"
                        className="Profile__input--edit"
                        value={
                          this.state.first_name === null
                            ? user.first_name
                            : this.state.first_name
                        }
                        onChange={this.userProfileInputChangeHandler}
                      />
                    </td>
                  </tr>

                  <tr>
                    <td>Фамилия:</td>
                    <td>
                      <input
                        name="last_name"
                        placeholder="Введите фамилию"
                        className="Profile__input--edit"
                        value={
                          this.state.last_name === null
                            ? user.last_name
                            : this.state.last_name
                        }
                        onChange={this.userProfileInputChangeHandler}
                      />
                    </td>
                  </tr>
                </Fragment>
              ) : null}
              <tr>
                <td>День рождения:</td>
                <td>
                  {this.state.edit ? (
                    <DateSingleInput
                      onDateChange={data =>
                        this.setState({
                          birth_day: data.date,
                          updatedUserData: {
                            ...this.state.updatedUserData,
                            birth_day: this.convertDate(data.date)
                          }
                        })
                      }
                      onFocusChange={focusedInput =>
                        this.setState({
                          showDatepicker: focusedInput
                        })
                      }
                      date={this.state.birth_day}
                      showDatepicker={this.state.showDatepicker}
                    />
                  ) : (
                    format(new Date(user.birth_day), "dd MMMM yyyy", {
                      locale
                    })
                  )}
                </td>
              </tr>
              <tr>
                <td>Пол:</td>
                <td>
                  {this.state.edit ? (
                    <Select
                      onChange={this.genderChangeHandler}
                      defaultValue={[{ value: 1, label: "Мужской" }]}
                      options={[
                        { value: 0, label: "Женский" },
                        { value: 1, label: "Мужской" }
                      ]}
                      theme={theme => ({
                        ...theme,
                        colors: {
                          ...theme.colors,
                          primary: "#CD3232",
                          primary25: "#f5d6d6",
                          neutral0: "#FFF"
                        }
                      })}
                    />
                  ) : user.gender === 0 ? (
                    "Женский"
                  ) : (
                    "Мужской"
                  )}
                </td>
              </tr>
              <tr>
                <td>Номер телефона:</td>
                <td>
                  <InputMask
                    name="phone"
                    onChange={this.userProfileInputChangeHandler}
                    value={
                      this.state.phone === null ? user.phone : this.state.phone
                    }
                    disabled={!this.state.edit}
                    mask="9(999)-999-99-99"
                    maskChar=" "
                  >
                    {inputProps => (
                      <input
                        className={`Profile__input ${
                          this.state.edit ? "Profile__input--edit" : ""
                        }`}
                        {...inputProps}
                        placeholder="+7(   )"
                      />
                    )}
                  </InputMask>
                  {!this.state.edit && user.is_active ? (
                    <img
                      className="Profile__verified"
                      src={correctGreen}
                      alt=""
                    />
                  ) : null}
                </td>
              </tr>
              <tr>
                <td>Email:</td>
                <td>
                  <input
                    name="email"
                    className={`Profile__input ${
                      this.state.edit ? "Profile__input--edit" : ""
                    }`}
                    value={
                      this.state.email === null ? user.email : this.state.email
                    }
                    onChange={this.userProfileInputChangeHandler}
                  />
                </td>
              </tr>
            </tbody>
          </Table>
          {user.user_type === 1 ? (
            <button className="Profile__ad-button" onClick={this.goToNewHouse}>
              <Fa icon={faPlus} />
              {"\u00A0"}
              Разместить обьявление
            </button>
          ) : null}
          <button className="Profile__logout-button" onClick={this.logOut}>
            Выйти из аккаунта
          </button>
        </div>
      );
    } else {
      return null;
    }
  }
}

function mapStateToProps(state) {
  return {
    user: state.auth.user
  };
}

export default connect(mapStateToProps, {
  updateUserData,
  signOut,
  verifyPhone,
  toggleConfirmNumberModal
})(withRouter(Profile));
