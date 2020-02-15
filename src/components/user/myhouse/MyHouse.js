import React, { Component, Fragment } from "react";
import { connect } from "react-redux";

import { getHouse } from "../../../services/house";
import DatePreview from "../../UIComponents/DatePreview/DatePreview";
import { colors } from "../../UIComponents/DatePreview/helpers";
import {
  getMyHouses,
  editActivation,
  deleteMyHouse
} from "../../../actions/house.action";
import { activateHouse, deactivateHouse } from "../../../services/house";

import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import { faAngleLeft } from "@fortawesome/free-solid-svg-icons";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";
import "./MyHouse.scss";

class MyHouse extends Component {
  constructor(props) {
    super(props);
    this.state = {
      house: {}
    };
  }
  componentDidMount() {
    const { id } = this.props.match.params;
    getHouse(id)
      .then(data => {
        this.setState({
          ...this.state,
          ...data.data
        });
      })
      .catch(error => {});
  }
  activationToggle = () => {
    const { id } = this.props.match.params;
    const { status } = this.state;
    if (!status) {
      activateHouse(id)
        .then(data => {
          this.setState({
            status: true
          });
        })
        .catch(error => {});
    } else {
      deactivateHouse(id)
        .then(data => {
          this.setState({
            status: false
          });
        })
        .catch(error => {});
    }
  };
  goToEditHouse = () => {
    this.props.history.push("/edithouse/" + this.state.id);
  };
  goToHouses = () => {
    this.props.history.push("/myhouses");
  };
  render() {
    // reserves.forEach((element, index) => {
    //   reserves[index]["color"] =
    //     colors[Math.floor(Math.random() * colors.length)];
    // });
    return (
      <div>
        <h1 className="User__title">Мои обьявления</h1>
        <div
          className="NewAd__slick--arrow NewAd__slick--arrow-prev"
          onClick={this.goToHouses}
        >
          <Fa icon={faAngleLeft} /> {"\u00A0"} Назад
        </div>
        <div className="MyHouse__date">
          <DatePreview
            reserves={
              this.state.reservations &&
              this.state.reservations.map((item, index) => {
                return {
                  ...item,
                  color: colors[Math.floor(Math.random() * colors.length)]
                };
              })
            }
            // blocked={blocked}
            minBookingDate={new Date()}
            maxBookingDate={
              new Date(new Date().getTime() + 60 * 24 * 60 * 60 * 1000)
            }
          />
          <div className="NewAd__divider" />

          {this.state.name ? (
            <Fragment>
              <div className="MyHouse__info">
                {/* <img className="MyHouse__image" src={defaultImage} alt="" /> */}

                <div className="MyHouse__data">
                  <p className="MyHouse__title">{this.state.name}</p>

                  <p className="MyHouse__price">
                    <span className="MyHouse__pre-price">цена: </span>
                    {"\u00A0"}
                    {this.state.price} KZT/сутки
                  </p>
                </div>

                <div className="MyHouse__buttons">
                  {this.state.status && this.state.status ? (
                    <button
                      className="MyHouse__deactivate"
                      onClick={this.activationToggle}
                    >
                      Деактивировать
                    </button>
                  ) : (
                    <button
                      className="MyHouse__activate"
                      onClick={this.activationToggle}
                    >
                      Активировать
                    </button>
                  )}

                  <button
                    className="MyHouse__change"
                    onClick={this.goToEditHouse}
                  >
                    Изменить
                  </button>
                  <button
                    onClick={() => this.houseDelete()}
                    className="MyHouse__delete"
                  >
                    Удалить
                  </button>
                </div>
              </div>
              <div className="MyHouse__income">
                {this.state.reservations &&
                this.state.reservations.length > 0 ? (
                  this.state.reservations.map((item, index) => (
                    <div className="MyHouse__income--item" key={index}>
                      <p className="MyHouse__income--fullname">
                        {item.user.first_name} {item.user.last_name}
                      </p>
                      <div className="MyHouse__income--info">
                        <p className="MyHouse__income--total">
                          +{item.income} KZT
                        </p>
                        <p className="MyHouse__income--date">{item.check_in}</p>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="MyHouse__title">Нет гостей</p>
                )}
              </div>
            </Fragment>
          ) : (
            <Loader
              type="Puff"
              color="#CD3232"
              height={100}
              width={100}
              timeout={20000}
            />
          )}
        </div>
      </div>
    );
  }
}
function mapStateToProps(state) {
  return {
    myHouses: state.house.myHouses.results
  };
}

export default connect(mapStateToProps, {
  getMyHouses,
  editActivation,
  deleteMyHouse
})(MyHouse);
