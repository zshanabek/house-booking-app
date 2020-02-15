import React, { Component } from "react";
import { connect } from "react-redux";

import "./MyHouses.scss";

import { getMyHouses, editActivation } from "../../../actions/house.action";
import { activateHouse, deactivateHouse } from "../../../services/house";
import { defaultImage } from "../../../assets/images/images";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";

import { faInfo, faBan, faCheck } from "@fortawesome/free-solid-svg-icons";

class MyAds extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  componentDidMount() {
    const { getMyHouses } = this.props;
    getMyHouses();
  }
  activationToggle = (id, active, index) => {
    const { editActivation, myHouses } = this.props;
    let myHouse = myHouses[index];
    if (!active) {
      myHouse.status = true;
      activateHouse(id)
        .then(data => {
          editActivation(index, myHouse, false);
        })
        .catch(error => {
          editActivation(index, myHouse, true);
        });
    } else {
      myHouse.status = false;
      deactivateHouse(id)
        .then(data => {
          editActivation(index, myHouse, false);
        })
        .catch(error => {
          editActivation(index, myHouse, true);
        });
    }
  };
  goToNewHouse = () => {
    this.props.history.push("/newhouse");
  };
  openHouse = id => {
    this.props.history.push("/myhouse/" + id);
  };

  render() {
    const { myHouses } = this.props;
    return (
      <div className="MyAds">
        <h1 className="User__title">Мои обьявления</h1>
        <div className="MyAds__orders--list">
          {myHouses &&
            myHouses.map((order, index) => (
              <div key={index} className="MyAds__orders--item">
                <img
                  className="MyAds__orders--image"
                  src={defaultImage}
                  alt=""
                />
                <div className="MyAds__orders--info">
                  <p className="MyAds__orders--title">{order.name}</p>
                  <br />
                  <p className="MyAds__orders--price">{order.price} KZT/ст</p>
                  <p className="MyAds__orders--label">Цена:</p>
                  <br />
                  <p className="MyAds__orders--price">TODO kzt</p>
                  <p className="MyAds__orders--label">Заработок:</p>
                </div>
                <div className="MyAds__orders--buttons">
                  {order.status ? (
                    <button
                      onClick={() =>
                        this.activationToggle(order.id, order.status, index)
                      }
                      className="MyAds__orders--deactivate"
                    >
                      <span className="MyAds__orders--text">
                        Деактивировать
                      </span>
                      <div className="MyAds__orders--icons">
                        <Fa icon={faBan} />
                      </div>
                    </button>
                  ) : (
                    <button
                      onClick={() =>
                        this.activationToggle(order.id, order.status, index)
                      }
                      className="MyAds__orders--activate"
                    >
                      <span className="MyAds__orders--text">Активировать</span>
                      <div className="MyAds__orders--icons">
                        <Fa icon={faCheck} />
                      </div>
                    </button>
                  )}
                  <button
                    onClick={() => this.openHouse(order.id)}
                    className="MyAds__orders--open"
                  >
                    <span className="MyAds__orders--text">Подробнее</span>
                    <div className="MyAds__orders--icons">
                      <Fa icon={faInfo} />
                    </div>
                  </button>
                </div>
              </div>
            ))}
        </div>
        <button onClick={this.goToNewHouse} className="MyAds__newad">
          Добавить ещё обьявление
        </button>
      </div>
    );
  }
}
function mapStateToProps(state) {
  return {
    myHouses: state.house.myHouses.results
  };
}

export default connect(mapStateToProps, { getMyHouses, editActivation })(MyAds);
