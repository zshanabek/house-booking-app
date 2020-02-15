import React, { Component } from "react";
import "./Orders.scss";
import { defaultImage } from "../../../assets/images/images";
import {
  getOrders,
  acceptReservation,
  rejectReservation
} from "../../../services/reservations";
class Orders extends Component {
  constructor(props) {
    super(props);
    this.state = {
      orders: []
    };
  }
  componentDidMount() {
    getOrders().then(data => {
      this.setState({
        orders: data.data.results
      });
    });
  }
  accept = id => {
    acceptReservation(id)
      .then(data => {
        getOrders().then(data => {
          this.setState({
            orders: data.data.results
          });
        });
      })
      .catch(e => {
        console.log(e);
      });
  };
  reject = id => {
    rejectReservation
      .then(data => {
        getOrders().then(data => {
          this.setState({
            orders: data.data.results
          });
        });
      })
      .catch(e => {
        console.log(e);
      });
  };

  render() {
    const { orders } = this.state;
    return (
      <div>
        <h1 className="User__title">Заявки</h1>
        <div className="MyAds__orders--list">
          {orders && orders.length > 0 ? (
            orders.map((order, index) => (
              <div key={index} className="Orders__item">
                <img
                  className="Orders__item--image"
                  src={defaultImage}
                  alt=""
                />
                {order.accepted_house === true ? (
                  <div className="Orders__item--info">
                    <span className="Orders__item--text">
                      Вы приняли заявку от{" "}
                    </span>
                    {order.user.full_name} {order.user.last_name}
                  </div>
                ) : order.accepted_house === false ? (
                  <div className="Orders__item--info">
                    <span className="Orders__item--text">
                      Вы отклонили заявку от{" "}
                    </span>
                    {order.user.full_name} {order.user.last_name}
                  </div>
                ) : (
                  <div className="Orders__item--info">
                    {order.user.full_name} {order.user.last_name}
                    <span className="Orders__item--text">
                      {" "}
                      хочет быть вашем гостем в{" "}
                    </span>
                    {order.house.name}
                  </div>
                )}

                {order.accepted_house === null ? (
                  <div className="MyAds__orders--buttons">
                    <button
                      onClick={() => this.accept(order.id)}
                      className="MyAds__orders--activate"
                    >
                      Принять
                    </button>
                    <button
                      onClick={() => this.reject(order.id)}
                      className="MyAds__orders--deactivate"
                    >
                      Отклонить
                    </button>
                  </div>
                ) : (
                  ""
                )}
              </div>
            ))
          ) : (
            <div className="Orders__empty">Нет заявок</div>
          )}
        </div>
      </div>
    );
  }
}

export default Orders;
