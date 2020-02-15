import React, { Component } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import { toggleSignInModal } from "../../actions/user.action";
import Carousel from "react-bootstrap/Carousel";
import Modal from "react-bootstrap/Modal";
import { mainBackground } from "../../assets/images/images";
import { url } from "../../services/config";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { YMaps, Map, Placemark } from "react-yandex-maps";
import { getHouse, getBlockedDates } from "../../services/house";
import { getReviews } from "../../services/review";
import { sendMessage } from "../../services/chat";
import NumberFormat from "react-number-format";
import { START_DATE, END_DATE } from "@datepicker-react/styled";
import { DatePicker } from "../UIComponents/DatePicker";
import { format } from "date-fns";
import { ru as locale } from "date-fns/locale";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import {
  faMapMarkerAlt,
  faUserFriends,
  faBed
} from "@fortawesome/free-solid-svg-icons";
import { faEnvelope } from "@fortawesome/free-regular-svg-icons";
import ReactStars from "react-rating-stars-component";
import { createReservation } from "../../services/reservations";
import "./Housing.scss";

class Housing extends Component {
  constructor(props) {
    super(props);
    this.state = {
      totalDetailsIsOpen: false,
      totalPrice: 0,
      center: [43.238949, 76.889709],
      house: {
        id: "",
        name: "",
        rooms: 3,
        floor: 6,
        address: "Omarova",
        description: "",
        longitude: 3.077363,
        latitude: 50.644228,
        city: "",
        photos: [],
        house_type: 1,
        price: 213,
        status: 1,
        user: {
          email: "",
          id: "",
          first_name: "",
          last_name: "",
          userpic: ""
        }
      },
      guests: 0,
      startDate: "",
      endDate: "",
      focusedInput: null,
      zoom: 15,
      sendMessage: false,
      sendMessageText: ""
    };
  }
  componentDidMount() {
    const { id } = this.props.match.params;

    getHouse(id)
      .then(data => {
        this.setState({
          house: {
            ...this.state.house,
            ...data.data
          }
        });
      })
      .catch(error => {});
    getBlockedDates(id)
      .then(data => {
        this.setState({ blockedDates: data.data });
      })
      .catch(e => {});
    getReviews(id)
      .then(data => {
        this.setState({
          reviews: data.data.results
        });
      })
      .catch(error => {});
  }
  handleDatesChange = data => {
    if (!data.focusedInput) {
      this.setState({
        ...data,
        focusedInput: START_DATE
      });
    } else {
      this.setState(data);
    }
  };
  ratingChanged = newRating => {
    this.setState({
      rating: newRating
    });
  };
  dateFocusHandler = e => {
    this.setState({
      focusedInput: e.target.name === "from" ? START_DATE : END_DATE
    });
  };
  convert = str => {
    var date = new Date(str),
      mnth = ("0" + (date.getMonth() + 1)).slice(-2),
      day = ("0" + date.getDate()).slice(-2);
    return [date.getFullYear(), mnth, day].join("-");
  };
  datesChangeHandler = data => {
    this.setState(
      {
        ...this.state,
        ...data
      },
      () => {
        this.calculatePrice();
      }
    );
  };
  calculatePrice = () => {
    const { price } = this.state.house;
    const start = this.state.startDate;
    const end = this.state.endDate;

    if (start !== "" && end !== "") {
      let time = end.getTime() - start.getTime();
      let days = time / (1000 * 3600 * 24);
      this.setState({
        totalPrice: days * price
      });
    }
  };
  guestsChangeHandler = e => {
    e.preventDefault();
    this.setState({
      guests: e.target.value
    });
  };
  createReservation = e => {
    e.preventDefault();
    const { auth, toggleSignInModal } = this.props;
    if (!auth.isAuthenticated) {
      toggleSignInModal();
    } else {
      const params = new FormData();
      params.append("check_in", this.convert(this.state.startDate));
      params.append("check_out", this.convert(this.state.endDate));
      params.append("guests", parseInt(this.state.guests));
      params.append("house_id", parseInt(this.state.house.id));
      console.log(this.state.house.id);
      createReservation(params);
      this.props.history.push("/reservations");
    }
  };
  openSendMessage = () => {
    const { auth, toggleSignInModal } = this.props;
    if (!auth.isAuthenticated) {
      toggleSignInModal();
    } else {
      this.setState({ sendMessage: true });
    }
  };
  messageSend = e => {
    e.preventDefault();
    let data = new FormData();
    data.append("body", this.state.sendMessageText);
    data.append("recipient", this.state.house.user.id);
    sendMessage(data).then(data => {
      this.setState({
        sendMessage: false
      });
    });
  };
  render() {
    const { blockedDates } = this.state;

    return (
      <div className="Housing">
        <div className="Housing__carousel">
          <Carousel>
            {this.state.house.photos && this.state.house.photos.length > 0 ? (
              this.state.house.photos.map((item, index) => (
                <Carousel.Item key={index}>
                  <img
                    height="500px"
                    className="d-block w-100"
                    src={url + item.image}
                    alt=""
                  />
                </Carousel.Item>
              ))
            ) : (
              <Carousel.Item>
                <img
                  height="500px"
                  className="d-block w-100"
                  src={mainBackground}
                  alt=""
                />
              </Carousel.Item>
            )}
          </Carousel>
        </div>

        <section className="Housing__main">
          <Container>
            <Row>
              <Col lg={8}>
                <div className="Housing__header">
                  <img
                    className="Housing__header--avatar"
                    src={this.state.house.user.userpic}
                    alt={this.state.user}
                  />

                  <h1 className="Housing__header--title">
                    {this.state.house.name}
                  </h1>

                  <h2 className="Housing__header--place-rating">
                    <Fa icon={faMapMarkerAlt} />
                    {this.state.house.city}
                  </h2>
                  <h6 className="Housing__header--username">
                    {this.state.house.user.first_name}{" "}
                    {this.state.house.user.last_name}
                  </h6>
                  <h2 className="Housing__header--place-rating">
                    {/* <Fa icon={faStar} /> */}
                    <ReactStars
                      edit={false}
                      count={5}
                      value={this.state.house.rating}
                      onChange={this.ratingChanged}
                      size={24}
                      color1={"#bdbcbc"}
                      color2={"#CD3232"}
                    />
                    {/* {this.state.rating} */}
                  </h2>
                </div>
                <div className="Housing__cards">
                  <div className="Housing__cards--item">
                    {/* <Fa className="Housing__cards--icon" icon={faHome} /> */}
                    <h4 className="Housing__cards--icon">тип</h4>
                    <h4 className="Housing__cards--title">
                      {this.state.house.house_type}
                    </h4>
                  </div>
                  <div className="Housing__cards--item">
                    <Fa className="Housing__cards--icon" icon={faUserFriends} />
                    <h4 className="Housing__cards--title">
                      {this.state.house.guests} гости
                    </h4>
                  </div>
                  <div className="Housing__cards--item">
                    <Fa className="Housing__cards--icon" icon={faBed} />
                    <h4 className="Housing__cards--title">
                      {this.state.house.rooms} комнаты,
                      <br />
                      {this.state.house.beds} кровати
                    </h4>
                  </div>
                </div>
                <p className="Housing__description">
                  {this.state.house.description}
                </p>
                <div className="Housing__map">
                  <h6 className="Housing__map--title">Адрес</h6>
                  <h6 className="Housing__map--address">
                    {this.state.house.address}
                  </h6>
                  <YMaps>
                    <Map
                      width="100%"
                      defaultState={{
                        zoom: this.state.zoom,
                        center: [
                          this.state.house.latitude,
                          this.state.house.longitude
                        ]
                      }}
                    >
                      <Placemark
                        geometry={[
                          this.state.house.latitude,
                          this.state.house.longitude
                        ]}
                      />
                    </Map>
                  </YMaps>
                </div>
                <div className="Housing__rules">
                  <div className="Housing__rules--side">Удобста</div>
                  <div className="Housing__rules--list">
                    {this.state.house.accommodations &&
                      this.state.house.accommodations.map((item, index) => (
                        <p key={index} className="Housing__rules--item">
                          {index + 1 + ". " + item.name}
                        </p>
                      ))}
                  </div>
                </div>
                <div className="Housing__rules">
                  <div className="Housing__rules--side">
                    Правила
                    <br /> дома
                  </div>
                  <div className="Housing__rules--list">
                    {this.state.house.rules &&
                      this.state.house.rules.map((item, index) => (
                        <p key={index} className="Housing__rules--item">
                          {index + 1 + ". " + item.name}
                        </p>
                      ))}
                  </div>
                </div>
                <div className="Housing__rules">
                  <div className="Housing__rules--side">
                    Рядом
                    <br /> есть
                  </div>
                  <div className="Housing__rules--list">
                    {this.state.house.near_buildings &&
                      this.state.house.near_buildings.map((item, index) => (
                        <p key={index} className="Housing__rules--item">
                          {index + 1 + ". " + item.name}
                        </p>
                      ))}
                  </div>
                </div>
                <DatePicker
                  onClose={e => {
                    e.preventDefault();
                    this.setState({
                      focusedInput: null
                    });
                  }}
                  blockedDateRanges={blockedDates && blockedDates}
                  onDatesChange={data => {
                    this.setState({
                      ...this.state,
                      ...data
                    });
                  }}
                  startDate={this.state.startDate}
                  endDate={this.state.endDate}
                  focusedInput={this.state.focusedInput}
                  showClose={false}
                  showResetDates={false}
                  showStartDateCalendarIcon={false}
                  showEndDateCalendarIcon={false}
                  showSelectedDates={false}
                />

                <div className="Housing__reviews">
                  <h6 className="Housing__reviews--title">Отзывы</h6>
                  {this.state.reviews && this.state.reviews[0] ? (
                    this.state.reviews.map((review, index) => (
                      <div className="Housing__reviews--item" key={index}>
                        <img
                          className="Housing__reviews--avatar"
                          src="https://p7.hiclipart.com/preview/336/946/494/avatar-user-medicine-surgery-patient-avatar.jpg"
                          alt={this.state.user}
                        />

                        <h6 className="Housing__reviews--username">
                          {review.user.first_name}
                        </h6>
                        <ReactStars
                          className="Housing__reviews--rating"
                          edit={false}
                          count={5}
                          value={review.stars}
                          onChange={this.ratingChanged}
                          size={18}
                          color1={"#bdbcbc"}
                          color2={"#CD3232"}
                        />
                        <p className="Housing__reviews--date">
                          {format(
                            new Date(review.created_at),
                            "dd MMMM hh:mm",
                            { locale }
                          )}
                        </p>
                        <br />
                        <p className="Housing__reviews--body">{review.body}</p>
                      </div>
                    ))
                  ) : (
                    <div>Нет отзывов</div>
                  )}
                </div>
              </Col>

              <Col lg={4}>
                <div className="Housing__order--block">
                  <h2 className="Housing__order--title">
                    <NumberFormat
                      value={this.state.house.price}
                      displayType={"text"}
                      thousandSeparator={true}
                      prefix={"₸"}
                    />
                    {"\u00A0"}
                    тг/сутки
                  </h2>

                  <form className="Housing__order">
                    <div className="Housing__order--row">
                      <div
                        className="form-group"
                        style={{ position: "relative" }}
                      >
                        <input
                          type="text"
                          name="from"
                          readOnly
                          value={
                            this.state.startDate === ""
                              ? ""
                              : this.convert(this.state.startDate)
                          }
                          onFocus={this.dateFocusHandler}
                          className="form-control Housing__order--input-date"
                          placeholder="Прибытие"
                        />
                      </div>
                      <div className="form-group">
                        <input
                          type="text"
                          name="to"
                          readOnly
                          onFocus={this.dateFocusHandler}
                          value={
                            this.state.endDate === ""
                              ? ""
                              : this.convert(this.state.endDate)
                          }
                          className="form-control Housing__order--input-date"
                          placeholder="Отбытие"
                        />
                      </div>
                      {this.state.focusedInput !== null ? (
                        <div className="Housing__order--datepicker">
                          <DatePicker
                            onClose={e => {
                              e.preventDefault();
                              this.setState({
                                focusedInput: null
                              });
                            }}
                            onDatesChange={this.datesChangeHandler}
                            startDate={this.state.startDate}
                            endDate={this.state.endDate}
                            focusedInput={this.state.focusedInput}
                          />
                        </div>
                      ) : null}
                    </div>

                    <div className="form-group">
                      <input
                        type="number"
                        className="form-control Housing__order--input"
                        value={this.state.guests}
                        onChange={this.guestsChangeHandler}
                        placeholder="Гости"
                      />
                    </div>
                    <div>
                      <p className="Housing__order--total-price">
                        {this.state.totalPrice} тг
                      </p>
                      <p className="Housing__order--total">Итого:</p>
                      <p className="Housing__order--total-details">
                        включая услуги
                      </p>
                    </div>
                    <button
                      onClick={this.createReservation}
                      className="Housing__order--button"
                    >
                      Забронировать
                    </button>
                  </form>

                  <button
                    onClick={this.openSendMessage}
                    className="Housing__send-message"
                  >
                    Написать хозяйну{"\u00A0"}
                    <Fa icon={faEnvelope} />
                  </button>
                </div>
              </Col>
            </Row>
          </Container>
        </section>
        <Modal
          size="md"
          show={this.state.sendMessage}
          onHide={() =>
            this.setState({
              sendMessage: false
            })
          }
          centered={true}
        >
          <Modal.Body>
            <form className="Cancel__form">
              <label className="Cancel__label">Сообщение:</label>
              <textarea
                value={this.state.sendMessageText}
                onChange={e => {
                  this.setState({
                    sendMessageText: e.target.value
                  });
                }}
                placeholder="Ваш текст"
                rows={5}
                maxLength={200}
                className="Cancel__input"
              />
              <span className="Cancel__input--limit">
                {this.state.sendMessageText.length} / 200
              </span>
              <button
                onClick={this.messageSend}
                className="Cancel__button"
                disabled={this.state.sendMessageText.length === 0}
              >
                Отправить
              </button>
            </form>
          </Modal.Body>
        </Modal>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    auth: state.auth,
    user: state.auth.user
  };
}

export default connect(mapStateToProps, { toggleSignInModal })(
  withRouter(Housing)
);
