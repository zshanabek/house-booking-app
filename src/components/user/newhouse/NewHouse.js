import React, { Component } from "react";
import { connect } from "react-redux";
import NumberFormat from "react-number-format";
import { format } from "date-fns";
import { ru as locale } from "date-fns/locale";
import { DatePicker } from "../../UIComponents/DatePicker";
import ReactSlider from "react-slider";
import Select from "react-select";
import Collapse from "react-bootstrap/Collapse";
import styled from "styled-components";
import { YMaps, Map, Placemark } from "react-yandex-maps";
import CheckboxGroup from "../../UIComponents/CheckboxGroup";

import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import {
  faAngleLeft,
  faPlus,
  faCamera
} from "@fortawesome/free-solid-svg-icons";
import { faTimesCircle } from "@fortawesome/free-regular-svg-icons";
import { createHouse } from "../../../services/house";

import "./NewHouse.scss";

const mapData = {
  center: [43.238949, 76.889709],
  zoom: 12
};
const StyledTrack = styled.div`
  top: 6px;
  bottom: 0;
  height: 12px;
  background: #cd3232;
  border-radius: 999px;
`;
const Track = (props, state) => <StyledTrack {...props} index={state.index} />;

const optionsStyle = {
  control: (styles, state) => ({
    ...styles,
    minWidth: "200px",
    backgroundColor: "white",
    height: "50px",
    border: "1px solid rgba(113, 113, 118, 0.9)",
    borderRadius: "6px",
    paddingLeft: "15px"
  }),
  container: (styles, state) => ({
    ...styles,
    marginLeft: "1px",
    marginBottom: "40px"
  })
};

function SampleNextArrow(props) {
  const { onClick, createNewAdClickHandler, step, state } = props;
  let disabled = false;
  switch (step) {
    case 0:
      disabled =
        state.type === "" ||
        state.guests === 0 ||
        state.floor === 0 ||
        state.beds === 0 ||
        state.rooms === 0;
      break;
    case 1:
      disabled =
        state.coordinates.length === 0 ||
        state.country === "" ||
        state.region === "" ||
        state.city === "" ||
        state.address === "";
      break;
    case 3:
      disabled = state.name === "" || state.description === "";
      break;
    case 7:
      disabled = state.policyAgreement === false;
      break;
    case 9:
      disabled = state.price === "" || state.price <= 0 || isNaN(state.price);
      break;
    default:
      break;
  }

  if (9 === step) {
    return (
      <button
        className={`NewAd__slick--arrow NewAd__slick--arrow-next`}
        onClick={createNewAdClickHandler}
      >
        Разместить
      </button>
    );
  } else if (10 === step) {
    return null;
  } else {
    return (
      <button
        disabled={disabled}
        className={`NewAd__slick--arrow NewAd__slick--arrow-next ${
          disabled ? "NewAd__slick--arrow-disabled" : ""
        }`}
        onClick={() => {
          onClick();
          const title = document.getElementById("newAdTitle");
          title.scrollIntoView();
        }}
      >
        Далее
      </button>
    );
  }
}

function SamplePrevArrow(props) {
  const { onClick, step } = props;
  if (step === 0) {
    return "";
  } else {
    return (
      <div
        className="NewAd__slick--arrow NewAd__slick--arrow-prev"
        onClick={onClick}
      >
        <Fa icon={faAngleLeft} /> {"\u00A0"} Назад
      </div>
    );
  }
}

class NewAd extends Component {
  constructor(props) {
    super(props);
    this.state = {
      step: 0,
      disabledToNext: false,
      setSale: false,

      type: "",
      guests: 0,
      floor: 0,
      rooms: 0,
      beds: 0,

      lat: 0,
      lon: 0,
      country: "",
      region: "",
      city: "",
      coordinates: [],
      address: "",
      postCode: "",

      photos: [],

      name: "",
      description: "",

      accommodations: [],
      near_buildings: [],

      policyAgreement: false,

      busy_days: [],

      rules: [],
      price: 0,

      hasSale: false,
      sale: 0,
      saleDays: "7",

      start_date: "",
      end_date: "",
      focusedInput: "startDate"
    };
  }
  componentDidMount() {}
  inputChangeHandler = e => {
    this.setState({
      [e.target.name]: e.target.value
    });
  };
  onMapClick = event => {
    this.setState({
      coordinates: event.get("coords")
    });
  };
  createNewAdClickHandler = e => {
    this.setState({
      step: this.state.step + 1
    });
    const {
      type,
      guests,
      floor,
      rooms,
      beds,
      coordinates,
      city,
      region,
      country,
      address,
      upload,
      name,
      description,
      accommodations,
      near_buildings,
      busy_days,
      rules,
      price,
      sale,
      saleDays
    } = this.state;

    const params = new FormData();
    params.append("house_type_id", type);
    params.append("guests", guests);
    params.append("floor", floor);
    params.append("rooms", rooms);
    params.append("beds", beds);
    params.append("latitude", coordinates[0]);
    params.append("longitude", coordinates[1]);
    params.append("city_id", city);
    params.append("region_id", region);
    params.append("country_id", country);
    params.append("address", address);
    if (upload) {
      for (const file of upload) {
        params.append("photos", file, file.name);
      }
    }
    params.append("name", name);
    params.append("description", description);
    if (accommodations) {
      accommodations.forEach(item => {
        params.append("accommodations", item.name);
      });
    }
    if (near_buildings) {
      near_buildings.forEach(item => {
        params.append("near_buildings", item.name);
      });
    }
    if (rules) {
      rules.forEach(item => {
        params.append("rules", item.name);
      });
    }
    if (busy_days) {
      rules.forEach(item => {
        params.append("blocked_dates", item.name);
      });
    }

    params.append("price", price);
    if (this.state.hasSale) {
      if (saleDays === 7) {
        params.append("discount7days", sale);
      } else {
        params.append("discount30days", sale);
      }
    }

    createHouse(params)
      .then(date => {
        this.props.history.push("/myhouses");
      })
      .catch(e => {
        console.log(e);
      });
  };
  handleFile = e => {
    console.log(e.target.files);
    let images = [];
    Array.from(e.target.files).forEach(image => {
      images.push(URL.createObjectURL(image));
    });
    this.setState({
      photos: images,
      upload: e.target.files
    });
  };
  checkboxChangeHandler = e => {
    this.setState({
      [e.target.name]: this.state[e.target.getAttribute("name")].push(
        e.target.getAttribute("item")
      )
    });
  };
  convert = str => {
    var date = new Date(str),
      mnth = ("0" + (date.getMonth() + 1)).slice(-2),
      day = ("0" + date.getDate()).slice(-2);
    return [date.getFullYear(), mnth, day].join("-");
  };
  removeBusyDate = e => {
    let removed = this.state.busy_days.splice(e.target.getAttribute("item"), 1);
    this.setState({
      busy_days: this.state.busy_days
    });
  };
  saleDaysChangeHandler = e => {
    this.setState({
      saleDays: e.target.getAttribute("name")
    });
  };
  saleSliderChangeHandler = e => {
    this.setState({
      sale: e
    });
  };
  setSale = () => {
    this.setState({
      hasSale: true,
      setSale: false
    });
  };
  cancelSale = () => {
    this.setState({
      hasSale: false,
      setSale: false,
      sale: 0
    });
  };
  counterMinusCLickHandler = e => {
    if (this.state[e.target.getAttribute("name")] - 1 >= 0) {
      let value = this.state[e.target.getAttribute("name")] - 1;
      this.setState({
        [e.target.getAttribute("name")]: value
      });
    }
  };
  counterPlusCLickHandler = e => {
    this.setState({
      [e.target.getAttribute("name")]:
        this.state[e.target.getAttribute("name")] + 1
    });
  };
  prevStepClick = e => {
    this.setState({
      step: this.state.step - 1
    });
  };
  nextStepClick = e => {
    this.setState({
      step: this.state.step + 1
    });
  };
  checkboxGroupChangeHandler = (name, set) => {
    this.setState({
      [name]: set
    });
  };
  policyAgreementChangeHandler = () => {
    this.setState({
      policyAgreement: !this.state.policyAgreement
    });
  };
  goToPrivacyPolicy = () => {
    window.open("https://akv.kz/privacy_policy", "_blank");
  };
  render() {
    const { busy_days } = this.state;
    const { reference } = this.props;
    console.log();
    return (
      <div className="NewAd">
        <h1 id="newAdTitle" className="User__title">
          Разместить обьявление
        </h1>
        {this.state.step !== 10 ? (
          <SamplePrevArrow
            step={this.state.step}
            onClick={this.prevStepClick}
          />
        ) : (
          ""
        )}
        {this.state.step === 0 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">Выберите тип жилья</p>
            <Select
              styles={optionsStyle}
              placeholder="Выбрать"
              onChange={e => {
                this.setState({
                  type: e.value
                });
              }}
              options={
                reference.houseTypes &&
                reference.houseTypes.map(type => {
                  return {
                    value: type.id,
                    label: type.name
                  };
                })
              }
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

            <div className="NewAd__divider" />
            <p className="NewAd__title">Сколько гостей вы принимаете?</p>
            <NewAdCounter
              minus={this.counterMinusCLickHandler}
              plus={this.counterPlusCLickHandler}
              title="Гости"
              name="guests"
              count={this.state.guests}
            />
            <div className="NewAd__divider" />
            <p className="NewAd__title">На каком этаже ваш дом?</p>
            <NewAdCounter
              minus={this.counterMinusCLickHandler}
              plus={this.counterPlusCLickHandler}
              title="Этаж"
              name="floor"
              count={this.state.floor}
            />
            <div className="NewAd__divider" />
            <p className="NewAd__title">Сколько комнат?</p>
            <NewAdCounter
              minus={this.counterMinusCLickHandler}
              plus={this.counterPlusCLickHandler}
              title="Комнаты"
              name="rooms"
              count={this.state.rooms}
            />
            <div className="NewAd__divider" />
            <p className="NewAd__title">Сколько кроватей?</p>
            <NewAdCounter
              minus={this.counterMinusCLickHandler}
              plus={this.counterPlusCLickHandler}
              title="Кровати"
              name="beds"
              count={this.state.beds}
            />
            <div className="NewAd__divider" />
          </div>
        ) : this.state.step === 1 ? (
          <div className="NewAd__item">
            <div style={{ display: "flex", flexDirection: "column" }}>
              <p className="NewAd__title">Адрес вашего жилья</p>

              <div className="NewAd__input-group">
                <label
                  className="NewAd__input-label"
                  htmlFor="newAdCountryInput"
                >
                  Страна
                  <span className="NewAd__input-label-req">{"\u00A0"}*</span>
                </label>
                <Select
                  styles={optionsStyle}
                  id="newAdCityInput"
                  placeholder={"Выбрать"}
                  onChange={e => {
                    this.setState({
                      country: e.value
                    });
                  }}
                  options={
                    reference.countries &&
                    reference.countries.map(country => {
                      return {
                        value: country.id,
                        label: country.name
                      };
                    })
                  }
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
              </div>
              <div className="NewAd__input-group">
                <label
                  className="NewAd__input-label"
                  htmlFor="newAdRegionInput"
                >
                  Область
                  <span className="NewAd__input-label-req">{"\u00A0"}*</span>
                </label>
                <Select
                  styles={optionsStyle}
                  id="newAdCityInput"
                  placeholder={"Выбрать"}
                  onChange={e => {
                    this.setState({
                      region: e.value
                    });
                  }}
                  options={
                    reference.regions &&
                    reference.regions.map(region => {
                      return {
                        value: region.id,
                        label: region.name
                      };
                    })
                  }
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
              </div>
              <div className="NewAd__input-group">
                <label className="NewAd__input-label" htmlFor="newAdCityInput">
                  Город
                  <span className="NewAd__input-label-req">{"\u00A0"}*</span>
                </label>
                <Select
                  styles={optionsStyle}
                  id="newAdCityInput"
                  placeholder={"Выбрать"}
                  onChange={e => {
                    this.setState({
                      city: e.value
                    });
                  }}
                  options={
                    reference.cities &&
                    reference.cities.map(city => {
                      return {
                        value: city.id,
                        label: city.name
                      };
                    })
                  }
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
              </div>
              <label className="NewAd__input-label" htmlFor="newAdCityInput">
                {/* <Fa icon={faMapMarkerAlt} />
                {"\u00A0"} */}
                Указать на карте
                <span className="NewAd__input-label-req">{"\u00A0"}*</span>
              </label>

              <div className="NewAd__map-view">
                <YMaps>
                  <Map
                    width="100%"
                    height="100%"
                    defaultState={mapData}
                    onClick={this.onMapClick}
                  >
                    <Placemark geometry={this.state.coordinates} />
                  </Map>
                </YMaps>
              </div>
              <div className="NewAd__input-group">
                <label
                  className="NewAd__input-label"
                  htmlFor="newAdAddressInput"
                >
                  Адрес
                  <span className="NewAd__input-label-req">{"\u00A0"}*</span>
                </label>
                <input
                  id="newAdAddressInput"
                  className="NewAd__input"
                  name="address"
                  value={this.state.address}
                  onChange={this.inputChangeHandler}
                />
              </div>
              <div className="NewAd__input-group">
                <label className="NewAd__input-label" htmlFor="newAdIndexInput">
                  Почтовый индекс
                </label>
                <input
                  id="newAdIndexInput"
                  className="NewAd__input"
                  type="number"
                  name="postCode"
                  value={this.state.postCode}
                  onChange={this.inputChangeHandler}
                />
              </div>
            </div>
          </div>
        ) : this.state.step === 2 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">Добавьте фото вашего жильяя</p>
            <p className="NewAd__description">максимум 15 фото</p>
            <div className="NewAd__pick-image">
              {this.state.photos.length > 0 ? (
                this.state.photos.map((image, index) => (
                  <div key={index}>
                    <img
                      className="NewAd__pick-image--item"
                      src={image}
                      alt=""
                    />
                  </div>
                ))
              ) : (
                <div className="NewAd__pick-image--empty">
                  <Fa icon={faCamera} />
                </div>
              )}
              <label
                className="NewAd__pick-image--input-label"
                htmlFor="NewAdImagesPicker"
              >
                <Fa icon={faPlus} />
              </label>
              <input
                type="file"
                name="images"
                accept="image/jpeg;image/png"
                id="NewAdImagesPicker"
                className="NewAd__pick-image--input"
                onChange={this.handleFile}
                multiple
              />
            </div>
          </div>
        ) : this.state.step === 3 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">
              Добавте название и описание вашего жилья
            </p>
            <div className="NewAd__input-group">
              <label className="NewAd__input-label" htmlFor="newAdNameInput">
                Название
                <span className="NewAd__input-label-req">{"\u00A0"}*</span>
              </label>
              <input
                id="newAdNameInput"
                className="NewAd__input"
                name="name"
                value={this.state.name}
                onChange={this.inputChangeHandler}
                maxLength="200"
              />
              <span className="NewAd__input-limit">
                {this.state.name.length} / 200
              </span>
            </div>
            <div className="NewAd__input-group">
              <label className="NewAd__input-label" htmlFor="newAdNameInput">
                Описание
                <span className="NewAd__input-label-req">{"\u00A0"}*</span>
              </label>
              <textarea
                rows={5}
                id="newAdNameInput"
                className="NewAd__input"
                name="description"
                value={this.state.description}
                onChange={this.inputChangeHandler}
                maxLength="500"
              />
              <span className="NewAd__input-limit">
                {this.state.description.length} / 500
              </span>
            </div>
          </div>
        ) : this.state.step === 4 ? (
          <div className="NewAd__item">
            {reference.accommodations ? (
              <CheckboxGroup
                onChange={this.checkboxGroupChangeHandler}
                name="accommodations"
                title="Какие удобства вы предлагаете?"
                container={this.state.accommodations}
                array={reference.accommodations}
              />
            ) : null}
          </div>
        ) : this.state.step === 5 ? (
          <div className="NewAd__item">
            {reference.nearBuildings ? (
              <CheckboxGroup
                onChange={this.checkboxGroupChangeHandler}
                container={this.state.near_buildings}
                name="near_buildings"
                title="Что есть рядом с вашим жильем?"
                array={reference.nearBuildings}
              />
            ) : null}
          </div>
        ) : this.state.step === 6 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">Занятые даты</p>
            <p className="NewAd__description">
              Отметьте те дни, когда вы не сможете принимать гостей
            </p>
            {this.state.busy_days.map((item, index) => (
              <div className="NewAd__busy-dates" key={index}>
                <button
                  className="NewAd__busy-dates--close"
                  item={index}
                  onClick={this.removeBusyDate}
                >
                  <Fa icon={faTimesCircle} />
                </button>
                <div className="NewAd__busy-dates--text">
                  {format(new Date(item["check_in"]), "dd MMMM", { locale })}
                  {" - "}
                  {format(new Date(item["check_out"]), "dd MMMM", { locale })}
                </div>
              </div>
            ))}
            <div>
              <DatePicker
                showClose={false}
                showResetDates={false}
                showSelectedDates={false}
                blockedDateRanges={busy_days}
                onDatesChange={data => {
                  this.setState(
                    {
                      ...this.state,
                      start_date: data.startDate,
                      end_date: data.endDate,
                      focusedInput: data.focusedInput
                    },
                    () => {
                      if (data.startDate !== "" && data.endDate !== "") {
                        this.setState({
                          busy_days: [
                            ...busy_days,
                            {
                              check_in: this.convert(new Date(data.startDate)),
                              check_out: this.convert(new Date(data.endDate))
                            }
                          ],
                          start_date: "",
                          end_date: "",
                          focusedInput: "startDate"
                        });
                      }
                    }
                  );
                }}
                startDate={this.state.start_date}
                endDate={this.state.end_date}
                focusedInput={this.state.focusedInput}
              />
            </div>
          </div>
        ) : this.state.step === 7 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">Требования AKV.KZ</p>
            <button
              onClick={this.goToPrivacyPolicy}
              className="NewAd__set-on-map--button"
            >
              Политика конфиденциальности
            </button>
            <label
              className={`Results__filter--label ${
                this.state.policyAgreement
                  ? "Results__filter--label-checked"
                  : null
              }`}
              onClick={this.policyAgreementChangeHandler}
            >
              Я согласен с политикой конфиденциальности
            </label>
          </div>
        ) : this.state.step === 8 ? (
          <div className="NewAd__item">
            {reference.rules ? (
              <CheckboxGroup
                onChange={this.checkboxGroupChangeHandler}
                container={this.state.rules}
                name="rules"
                title="Правила дома"
                array={reference.rules}
              />
            ) : null}
          </div>
        ) : this.state.step === 9 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">Назначте цену за ваше жильё</p>
            <div className="NewAd__price">
              <NumberFormat
                className="NewAd__price--input"
                placeholder="Цена"
                onChange={e => {
                  this.setState({
                    price: parseInt(e.target.value)
                  });
                }}
                // prefix={"₸"}
                // thousandSeparator={true}
                value={this.state.price}
              />
              <span className="NewAd__price--currency">KZT</span>
            </div>

            <div className="NewAd__sale">
              {this.state.hasSale ? (
                <p className="NewAd__sale--display">
                  Скидка {this.state.sale}% на {this.state.saleDays} дней
                  <button
                    className="NewAd__sale--remove"
                    onClick={this.cancelSale}
                  >
                    <Fa icon={faTimesCircle} />
                  </button>
                </p>
              ) : (
                ""
              )}
              <Collapse in={this.state.setSale}>
                <div>
                  <p className="NewAd__sale--title">Назначить скидку</p>

                  <p className="NewAd__sale--item">Выберите кол-во дней</p>
                  <div className="NewAd__sale--radio-block">
                    <label
                      className={`NewAd__sale--radio ${
                        this.state.saleDays === "7"
                          ? "NewAd__sale--radio-active"
                          : ""
                      }`}
                      name="7"
                      onClick={this.saleDaysChangeHandler}
                    >
                      7 дней
                    </label>
                    <label
                      className={`NewAd__sale--radio ${
                        this.state.saleDays === "30"
                          ? "NewAd__sale--radio-active"
                          : ""
                      }`}
                      name="30"
                      onClick={this.saleDaysChangeHandler}
                    >
                      30 дней
                    </label>
                  </div>
                  <div className="NewAd__divider" />
                  <NumberFormat
                    className="NewAd__sale--procent"
                    value={this.state.sale}
                    displayType={"text"}
                    prefix={"%"}
                  />
                  <p className="NewAd__sale--item">Определите процент скидки</p>
                  <p style={{ float: "right" }} className="NewAd__sale--label">
                    100%
                  </p>
                  <p className="NewAd__sale--label">0%</p>
                  <ReactSlider
                    onChange={this.saleSliderChangeHandler}
                    className="NewAd__slider"
                    thumbClassName="NewAd__slider--thumb"
                    renderTrack={Track}
                    ariaValuetext={state => `Thumb value ${state.valueNow}`}
                    pearling
                    step={5}
                    min={0}
                    max={100}
                  />

                  <div className="NewAd__divider" />
                  <button onClick={this.setSale} className="NewAd__sale--set">
                    Добавить
                  </button>
                  <button
                    onClick={this.cancelSale}
                    className="NewAd__sale--cancel"
                  >
                    Отменить
                  </button>
                </div>
              </Collapse>
              {!this.state.setSale && !this.state.hasSale ? (
                <button
                  onClick={() => {
                    this.setState({ setSale: true });
                  }}
                  className="NewAd__sale--add"
                >
                  Назначить скидку
                </button>
              ) : (
                ""
              )}
            </div>
          </div>
        ) : this.state.step === 10 ? (
          <div className="NewAd__item">
            <p className="NewAd__title">Спасибо, что выбрали нас!</p>
          </div>
        ) : (
          ""
        )}
        <SampleNextArrow
          step={this.state.step}
          state={this.state}
          createNewAdClickHandler={this.createNewAdClickHandler}
          onClick={this.nextStepClick}
        />
      </div>
    );
  }
}

function NewAdCounter(props) {
  return (
    <div className="NewAd__counter">
      <p className="NewAd__counter--title">{props.title}</p>
      <div className="NewAd__counter--buttons">
        <button
          onClick={props.minus}
          name={props.name}
          className="NewAd__counter--minus"
        >
          -
        </button>
        <p className="NewAd__counter--count">{props.count}</p>
        <button
          onClick={props.plus}
          name={props.name}
          className="NewAd__counter--plus"
        >
          +
        </button>
      </div>
    </div>
  );
}
function mapStateToProps(state) {
  return {
    // user: state.auth.user,
    reference: state.reference
  };
}

export default connect(mapStateToProps, null)(NewAd);
