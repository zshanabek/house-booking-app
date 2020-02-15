import React, { Component, Fragment } from "react";
import "./Reservations.scss";
import Modal from "react-bootstrap/Modal";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { defaultImage } from "../../assets/images/images";
import {
  getReservations,
  cancelReservation
} from "../../services/reservations";
import { createPayment } from "../../services/payment";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";

class Reservations extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      cancelId: null,
      cancelModal: false,
      cancelMessage: ""
    };
  }
  componentDidMount() {
    getReservations()
      .then(data => {
        this.setState({
          reservations: data.data.results,
          loading: false
        });
      })
      .catch(e => {
        console.log(e);
      });
  }
  createPaymentHandler = id => {
    console.log(id);
    createPayment(id).then(data => {
      console.log(data.data.payment_page_url);
      window.open(data.data.payment_page_url, "_blank");
    });
  };
  cancelReservation = () => {
    cancelReservation(this.state.cancelId, this.state.cancelMessage)
      .then(data => {
        getReservations()
          .then(data => {
            this.setState({
              reservations: data.data.results
            });
          })
          .catch(e => {
            console.log(e);
          });
      })
      .catch(e => {
        console.log(e);
      });
    this.setState({
      cancelId: null,
      cancelMessage: "",
      cancelModal: false
    });
  };
  goToResult = id => {
    this.props.history.push("/housing/" + id);
  };
  render() {
    const { reservations, loading } = this.state;
    return (
      <Fragment>
        <Container>
          <div className="Reservations">
            <h2 className="Reservations__title">Мои бронирования</h2>

            {reservations && reservations.length > 0 ? (
              <Row>
                {reservations.map((result, index) => (
                  <Col key={index} lg={6}>
                    <div className="Reservations__list--item" key={index}>
                      <div className="Reservations__list--wrapper">
                        <img
                          className="Reservations__list--image"
                          src={defaultImage}
                          alt=""
                        />
                        <p className="Reservations__list--title">
                          {result.house.name}
                        </p>
                        {result.status === 0 ? (
                          result.accepted_house === null ? (
                            <Fragment>
                              <p className="Reservations__list--status Reservations__list--waiting">
                                Ожидается ответ
                              </p>
                              <p className="Reservations__list--description">
                                Ваша заявка отправлена хозяйну. В течении 24
                                часов вам придет ответ.
                              </p>
                            </Fragment>
                          ) : result.accepted_house ? (
                            <Fragment>
                              <p className="Reservations__list--status Reservations__list--accepted">
                                Ваша заявка принета
                              </p>
                              <p className="Reservations__list--description">
                                Можете связаться с хозяйном через чат через
                                мобильное приложение.
                              </p>
                            </Fragment>
                          ) : (
                            <Fragment>
                              <p className="Reservations__list--status Reservations__list--rejected">
                                Ваша заявка откланена
                              </p>
                              <p className="Reservations__list--response">
                                {result.message}
                              </p>

                              <p className="Reservations__list--description">
                                Можете связаться с хозяйном через чат через
                                мобильное приложение.
                              </p>
                            </Fragment>
                          )
                        ) : (
                          <p className="Reservations__list--status Reservations__list--canceled">
                            Заявка отменена
                          </p>
                        )}
                      </div>
                      {result.status === 0 && result.accepted_house !== null ? (
                        <div className="Reservations__list--button-wrapper">
                          <button
                            onClick={() => this.createPaymentHandler(result.id)}
                            className="Reservations__list--button Reservations__list--accepted"
                          >
                            Оплатить
                          </button>
                          <button
                            onClick={() =>
                              this.setState({
                                cancelId: result.id,
                                cancelModal: true
                              })
                            }
                            className="Reservations__list--button Reservations__list--canceled"
                          >
                            Отменить
                          </button>
                        </div>
                      ) : (
                        ""
                      )}
                    </div>
                  </Col>
                ))}
              </Row>
            ) : loading ? (
              <Loader
                type="Puff"
                color="#CD3232"
                height={100}
                width={100}
                timeout={20000}
              />
            ) : (
              <div className="Reservations__empty">
                <p className="Reservations__paragraph">
                  Бронируйте жильё и проводите
                  <br /> своё лучшее время с нами
                </p>
                <button className="Reservations__button">
                  Забронировать жильё
                </button>
              </div>
            )}
          </div>
        </Container>
        <Modal
          size="md"
          show={this.state.cancelModal}
          onHide={() =>
            this.setState({
              cancelModal: false
            })
          }
          centered={true}
        >
          <Modal.Body>
            <h1 className="Cancel__title">
              Напишите пожалуйста почему <br /> вы отменяете заявку
            </h1>
            <form className="Cancel__form">
              <label className="Cancel__label">Сообщение:</label>
              <textarea
                value={this.state.cancelMessage}
                onChange={e => {
                  this.setState({
                    cancelMessage: e.target.value
                  });
                }}
                placeholder="Ваш текст"
                rows={5}
                maxLength={200}
                className="Cancel__input"
              />
              <span className="Cancel__input--limit">
                {this.state.cancelMessage.length} / 200
              </span>
              <button
                onClick={this.cancelReservation}
                className="Cancel__button"
                disabled={this.state.cancelMessage.length === 0}
              >
                Отправить
              </button>
            </form>
          </Modal.Body>
        </Modal>
      </Fragment>
    );
  }
}

export default Reservations;
