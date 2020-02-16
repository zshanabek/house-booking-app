import React, { Component, Fragment } from "react";
import { connect } from "react-redux";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { START_DATE, END_DATE } from "@datepicker-react/styled";
import { DatePicker } from "../UIComponents/DatePicker";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { Options } from "../UIComponents/Select";

import { signIn, signUp, signOut } from "../../actions/user.action";

import {
  bao,
  charyn,
  emel,
  ile,
  shym,
  medeu,
  koktobe,
  kaindy,
  apartments,
  dacha,
  houses,
  hotels,
  eventsImage1,
  eventsImage2,
  eventsImage3,
  eventsImage4,
  eventsImage5,
  eventsImage6
} from "../../assets/images/images";
import { getHouses } from "../../actions/house.action";

import "./Main.scss";

class Main extends Component {
  constructor() {
    super();
    this.state = {
      error: "",
      city__id: null,
      city_name: null,
      start_date: "",
      end_date: "",
      guests: null,
      focusedInput: null,
      optionsCards: [
        {
          id: 1,
          src: apartments,
          title: "Квартиры"
        },
        {
          id: 2,
          src: dacha,
          title: "Дачи"
        },
        {
          id: 3,
          src: houses,
          title: "Дома"
        },
        {
          id: 4,
          src: hotels,
          title: "Отели"
        }
      ],
      eventsCards: [
        {
          id: 1,
          src: eventsImage1,
          title: "Семейная вечеринка!",
          description:
            "Лондон однако забывать, что начало повседневной работы по формированию флейта, которая отсутсвует.",
          price: "20 000kzt",
          location: "Англия, Лондон"
        },
        {
          id: 2,
          src: eventsImage2,
          title: "Сказочная свадьба",
          description:
            "Лондон однако забывать, что начало повседневной работы по формированию флейта, которая отсутсвует.",
          price: "20 000kzt",
          location: "Англия, Лондон"
        },
        {
          id: 3,
          src: eventsImage3,
          title: "Семейная вечеринка!",
          description:
            "Лондон однако забывать, что начало повседневной работы по формированию флейта, которая отсутсвует.",
          price: "20 000kzt",
          location: "Англия, Лондон"
        },
        {
          id: 4,
          src: eventsImage4,
          title: "Семейная вечеринка!",
          description:
            "Лондон однако забывать, что начало повседневной работы по формированию флейта, которая отсутсвует.",
          price: "20 000kzt",
          location: "Англия, Лондон"
        },
        {
          id: 5,
          src: eventsImage5,
          title: "Семейная вечеринка!",
          description:
            "Лондон однако забывать, что начало повседневной работы по формированию флейта, которая отсутсвует.",
          price: "20 000kzt",
          location: "Англия, Лондон"
        }
      ],
      slickSettings: {
        dots: false,
        infinite: true,
        speed: 500,
        slidesToShow: 3,
        slidesToScroll: 3,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 3
            }
          },
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 2
            }
          },
          {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
      }
    };
  }
  componentDidMount() {}
  searchButtonHandler = e => {
    e.preventDefault();
    let { city__id, city_name, start_date, end_date, guests } = this.state;
    let params = {};
    if (city__id !== null) {
      params["city__id"] = city__id;
    }
    if (city_name !== null) {
      params["city_name"] = city_name;
    }
    if (start_date !== "") {
      start_date = this.convert(start_date);
      params["start_date"] = start_date;
    }
    if (end_date !== "") {
      end_date = this.convert(end_date);
      params["end_date"] = end_date;
    }
    if (guests !== null) {
      params["guests"] = guests;
    }
    if (
      city__id === null &&
      city_name === null &&
      start_date === "" &&
      end_date === "" &&
      guests === null
    ) {
      this.setState({
        error: "Поля не должны быть пустыми"
      });
    } else {
      const paramString = new URLSearchParams(params);

      this.props.history.push({
        pathname: "/results",
        search: `?${paramString.toString()}`
      });
    }
  };
  scrollTop = () => {
    window.scrollTo(0, 0);
  };
  goToHouses = type => {
    this.props.history.push("/houses/" + type);
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
  citySelectChangeHandler = e => {
    this.setState({
      city__id: e.value,
      city_name: e.label
    });
  };
  openCity = city_id => {
    let params = {
      city__id: city_id
    };
    const paramString = new URLSearchParams(params);

    this.props.history.push({
      pathname: "/results",
      search: `?${paramString.toString()}`
    });
  };
  openType = house_type__id => {
    let params = {
      city__id: 75,
      house_type__id
    };
    const paramString = new URLSearchParams(params);

    this.props.history.push({
      pathname: "/results",
      search: `?${paramString.toString()}`
    });
  };

  render() {
    let { reference } = this.props;
    let { slickSettings, optionsCards, eventsCards } = this.state;
    return (
      <Fragment>
        <section id="mainSection" className="Main">
          <Container>
            <Row>
              <Col sm={12} md={6} lg={7}>
                <div className="Main__details">
                  <h1 className="Main__title">akv.kz</h1>
                  <p className="Main__description">
                    • Быстрый поиск жилья и возможность бронирования 24/7
                    <br /> • Удобная онлайн платформа для размещения вашего
                    жилья
                  </p>
                </div>
              </Col>
              <Col sm={12} md={6} lg={5}>
                <div className="Main__search-block">
                  <div className="Main__form">
                    <h2 className="Main__search--title">Найти жильё</h2>
                    <div className="form-group">
                      <label htmlFor="placeInput" className="Main__form--label">
                        Место
                      </label>
                      <Options
                        placeholder="Куда угодно"
                        onChange={this.citySelectChangeHandler}
                        options={
                          reference.cities &&
                          reference.cities.map(city => {
                            return {
                              value: city.id,
                              label: city.name
                            };
                          })
                        }
                      />
                    </div>
                    <div className="Main__form--row">
                      <div className="form-group">
                        <label
                          htmlFor="dateInputFrom"
                          className="Main__form--label"
                        >
                          Прибытие
                        </label>
                        <input
                          type="text"
                          name="from"
                          readOnly="readonly"
                          onFocus={this.dateFocusHandler}
                          value={
                            this.state.start_date === ""
                              ? ""
                              : this.convert(this.state.start_date)
                          }
                          className="form-control Main__form--input-date-from"
                          placeholder="дд/мм/гггг"
                        />
                      </div>
                      <div className="form-group">
                        <label
                          className="Main__form--label"
                          htmlFor="dateInputTo"
                        >
                          Отбывание
                        </label>
                        <input
                          name="to"
                          type="text"
                          readOnly="readonly"
                          onFocus={this.dateFocusHandler}
                          value={
                            this.state.end_date === ""
                              ? ""
                              : this.convert(this.state.end_date)
                          }
                          className="form-control Main__form--input-date-to"
                          placeholder="дд/мм/гггг"
                        />
                      </div>
                      {this.state.focusedInput !== null ? (
                        <div className="Main--datepicker">
                          <DatePicker
                            onClose={e => {
                              e.preventDefault();
                              this.setState({
                                focusedInput: null
                              });
                            }}
                            onDatesChange={data => {
                              this.setState({
                                ...this.state,
                                start_date: data.startDate,
                                end_date: data.endDate,
                                focusedInput: data.focusedInput
                              });
                            }}
                            startDate={this.state.start_date}
                            endDate={this.state.end_date}
                            focusedInput={this.state.focusedInput}
                          />
                        </div>
                      ) : null}
                    </div>

                    <div className="form-group">
                      <label
                        className="Main__form--label"
                        htmlFor="guestsInput"
                      >
                        Гости
                      </label>
                      <input
                        type="number"
                        className="form-control Main__form--input"
                        id="guestsInput"
                        placeholder="Гости"
                        value={this.state.guests}
                        onChange={e => {
                          this.setState({
                            guests: e.target.value
                          });
                        }}
                      />
                    </div>
                    <p className="Main__form--error">{this.state.error}</p>
                    <button
                      onClick={this.searchButtonHandler}
                      className="Main__form--button"
                    >
                      Найти
                    </button>
                  </div>
                </div>
              </Col>
            </Row>
          </Container>
        </section>
        <section className="Options">
          <Container>
            <h1 className="Section__title">
              Что мы можем вам
              <br /> предложить
            </h1>
            <Row>
              {optionsCards.map(({ id, src, title }) => (
                <Col md={6} lg={3} key={id}>
                  <div
                    className="Options__item"
                    onClick={() => this.openType(id)}
                  >
                    <img
                      className="Options__item--image"
                      src={src}
                      alt={title}
                    />
                    <h5 className="Options__item--title">{title}</h5>
                  </div>
                </Col>
              ))}
            </Row>
          </Container>
        </section>
        <section className="Middle Middle--offer">
          <p className="Middle__title">Отдых с близким человеком!</p>
          <p className="Middle__text">
            Проведи со своим близким человеком отличные выходные и получи 35%
            скидки!
          </p>
          <button onClick={this.scrollTop} className="Middle__button">
            Получить
          </button>
        </section>
        <section className="Events">
          <Container>
            <h1 className="Section__title">Предстоящие события</h1>
            <div className="Events__top">
              <Row>
                {eventsCards.map(
                  ({ id, src, title, description, price, location }) => (
                    <EventItem
                      onClick={this.scrollTop}
                      key={id}
                      image={src}
                      title={title}
                      description={description}
                      price={price}
                      location={location}
                    />
                  )
                )}
                <Col md={6} lg={4}>
                  <div className="Events__item">
                    <img
                      className="Events__item--image"
                      src={eventsImage6}
                      alt=""
                    />
                    <div className="Events__more--border">
                      <button onClick={this.scrollTop} className="Events__more">
                        Смотреть все
                        <br /> предстоящие
                        <br /> события ->
                      </button>
                    </div>
                  </div>
                </Col>
              </Row>
            </div>
          </Container>
        </section>
        <section className="Middle Middle--feedback">
          <p className="Middle__title">
            Проведите лучшие выходные с AKV и поделитесь
            <br /> впечатлениями с нами
          </p>
          <button onClick={this.scrollTop} className="Middle__button">
            Оставить отзыв
          </button>
        </section>
        <section className="Recomendations">
          <div className="container">
            <h1 className="Section__title">Рекомендуем вам</h1>
            <Slider {...slickSettings}>
              <SlickItem
                image={bao}
                city__id={75}
                onClick={this.openCity}
                title="Большое Алматинское озеро"
                description="Настоящая лагуна в обрамлении снежных вершин. Название Большое Алматинское озеро говорит за себя, большое озеро захватывающее дух и впечатляющее размахом, расположенное среди заснеженных вершин."
              />
              <SlickItem
                image={koktobe}
                city__id={74}
                onClick={this.openCity}
                title="Гора Кок Тобе"
                description="город как “на ладони”.
                Аттракционы, скалодром, мини-зоопарк, кафе и рестораны, венчающиеся огромным единственным высокогорным колесом обозрения в мире и телевизионной башней, всё это - Кок тобе."
              />
              <SlickItem
                image={shym}
                city__id={32}
                onClick={this.openCity}
                title="Горнолыжный курорт «Чимбулак»"
                description="Самый быстрый снег
                Расположенный в живописном ущелье Заилийского Алатау на высоте 2260 м над уровнем моря в 25 км от центра города Алматы, горнолыжный курорт “Чимбулак” справа и слева окружен величественными горами со снежными склонами и вечно зелеными елями."
              />
              <SlickItem
                image={medeu}
                city__id={12}
                onClick={this.openCity}
                title="Каток Медео"
                description="“Сказка” на льду
                Высокогорный ледовый каток находится в урочище Медео и  является уникальной достопримечательностью Алматы, Медео — крупнейший в мире высокогорный комплекс для зимних видов спорта с самой большой площадью искусственного ледового поля — 10,5 тыс."
              />
              <SlickItem
                image={emel}
                city__id={47}
                onClick={this.openCity}
                title="Алтын-Эмель"
                description="Настоящая пустыня
                Алтын-Эмель это красные горы, желтые пески, зеленые тугайные джунгли, дикие пейзажи и завораживающие закаты. Притягательная энергия этого места вовлечет вас в интересное и практически мистическое путешествие по степям."
              />
              <SlickItem
                image={ile}
                city__id={47}
                onClick={this.openCity}
                title="Иле-Алатауский национальный парк"
                description="Первозданная природа

                Иле-Алатауский национальный парк является прародителем всех яблок, в парке всё еще произрастают предки сегодняшних яблок, целые рощи, вследствие город назван в честь этого фрукта и знаменит благодаря сорту яблок “Апорт” который не имеет равных в аромате и вкусе."
              />
              <SlickItem
                image={kaindy}
                city__id={47}
                onClick={this.openCity}
                title="Озеро Каинды"
                description="Мачты затонувших кораблей

                Название озера происходит от казахского Кайин — береза.Вода в Березовом озере очень холодная и тем не менее его обожают дайверы — подводные съемки очень красивы."
              />
              <SlickItem
                image={charyn}
                city__id={47}
                onClick={this.openCity}
                title="Чарынский каньон"
                description="Долина замков

                Чарынский каньон - памятник природы, сложенный из осадочных пород, привлекает к себе много взглядов и является местом куда стекается тысячи туристов со всего мира."
              />
            </Slider>
          </div>
        </section>
      </Fragment>
    );
  }
}
function SlickItem(props) {
  return (
    <div className="Recomendations__slider--item">
      <div className="Recomendations__slider--overlay" />
      <img
        className="Recomendations__slider--image"
        src={props.image}
        alt={props.title}
      />
      <div className="Recomendations__slider--details">
        <h4 className="Recomendations__slider--title">{props.title}</h4>
        <p className="Recomendations__slider--description">
          {props.description}
        </p>
        <button
          onClick={() => props.onClick(props.city__id)}
          className="Recomendations__slider--button"
        >
          Посмотреть
        </button>
      </div>
    </div>
  );
}
function EventItem(props) {
  return (
    <Col md={6} lg={4}>
      <div onClick={props.onClick} className="Events__item">
        <img className="Events__item--image" src={props.image} alt="" />
        <div className="Events__item--details">
          <h5 className="Events__item--title">{props.title}</h5>
          <p className="Events__item--description">
            {props.description.substring(0, 50)}
          </p>
          <p className="Events__item--date-place">
            <span style={{ fontWeight: 300 }}>Цена:</span> {props.price}
          </p>
          <div style={{ display: "inline-block", width: "100%" }}>
            <p className="Events__item--date-place">
              <span style={{ fontWeight: 300 }}>Место:</span> {props.location}
            </p>
            <button className="Events__item--more">Подробнее</button>
          </div>
        </div>
      </div>
    </Col>
  );
}
function mapStateToProps(state) {
  return {
    auth: state.auth,
    user: state.auth.user,
    reference: state.reference
  };
}

export default connect(mapStateToProps, {
  signIn,
  signUp,
  signOut,
  getHouses
})(Main);
