import React, { Component, Fragment } from "react";

import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";
import { YMaps, Map, Placemark } from "react-yandex-maps";
import { getHouses } from "../../actions/house.action";
import {
  getAccommodations,
  getHouseTypes
} from "../../actions/reference.action";
import { toggleFavourite } from "../../services/favourites";
import "./Results.scss";
import Collapse from "react-bootstrap/Collapse";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import ReactSlider from "react-slider";
import CheckboxGroup from "../UIComponents/CheckboxGroup";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";

import { Options, TypeOptions } from "../UIComponents/Select";

import { START_DATE, END_DATE } from "@datepicker-react/styled";
import styled from "styled-components";
import { DatePicker } from "../UIComponents/DatePicker";
import Container from "react-bootstrap/Container";
import House from "../blocks/house/House";
const mapData = {
  center: [43.238949, 76.889709],
  zoom: 12
};

const StyledTrack = styled.div`
  top: 6px;
  bottom: 0;
  height: 12px;
  background: ${props =>
    props.index === 2 ? "#E5E5E5" : props.index === 1 ? "#cd3232" : "#E5E5E5"};
  border-radius: 999px;
`;

const Track = (props, state) => <StyledTrack {...props} index={state.index} />;

class Results extends Component {
  constructor(props) {
    super(props);
    this.state = {
      city__id: null,
      city_name: "",
      start_date: "",
      end_date: "",
      guests: null,
      accommodations: [],
      focusedInput: null,
      mapVisibility: true,

      certifiedHouse: false,
      house_type__name: null,
      type: {
        value: 0,
        label: "Любой"
      },
      sort: "none",
      price__gte: 100,
      price__lte: 20000,
      rooms__gte: 1,
      rooms__lte: 10,
      beds__gte: 1,
      beds__lte: 20,

      filterOpen: false,
      loading: true
    };
  }
  componentWillMount() {
    // TODO: results in url address
    const { getAccommodations, getHouseTypes } = this.props;
    getAccommodations();
    getHouseTypes();

    const paramsUrl = new URLSearchParams(this.props.location.search);
    const params = {};
    for (var pair of paramsUrl.entries()) {
      params[pair[0]] = pair[1];
    }
    const { getHouses } = this.props;
    getHouses(params);
    this.setState({
      ...params
    });
  }
  onAccommodationsChange = (name, set) => {
    this.setState({
      [name]: set
    });
  };
  mapVisibilityChangeHandler = () => {
    this.setState({
      mapVisibility: !this.state.mapVisibility
    });
  };
  goToResult = id => {
    this.props.history.push("/housing/" + id);
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
  priceSliderChangeHandler = e => {
    this.setState({
      price__gte: e[0],
      price__lte: e[1]
    });
  };
  roomsSliderChangeHandler = e => {
    this.setState({
      rooms__gte: e[0],
      rooms__lte: e[1]
    });
  };
  bedsSliderChangeHandler = e => {
    this.setState({
      beds__gte: e[0],
      beds__lte: e[1]
    });
  };
  toggleFilter = () => {
    this.setState({
      filterOpen: !this.state.filterOpen
    });
  };
  toggleSortOption = e => {
    this.setState({
      sort: e.target.name
    });
  };
  citySelectChangeHandler = e => {
    this.setState({
      city__id: e.value,
      city_name: e.label
    });
  };
  onInputChange = (inputValue, { action }) => {
    console.log(inputValue, action);
    switch (action) {
      case "input-change":
        this.setState({ inputValue });
        return;
      case "menu-close":
        console.log(this.state.inputValue);
        let menuIsOpen = undefined;
        if (this.state.inputValue) {
          menuIsOpen = true;
        }
        this.setState({
          menuIsOpen
        });
        return;
      default:
        return;
    }
  };
  typeChangeHanlder = e => {
    console.log(e);
    this.setState({
      type: e
    });
  };
  resetFilter = e => {
    e.preventDefault();
    this.setState({
      certifiedHouse: false,
      type: {
        value: 0,
        label: "Любой"
      },
      sort: "none",
      accommodations: [],
      price__gte: 100,
      price__lte: 20000,
      rooms__gte: 1,
      rooms__lte: 10,
      beds__gte: 1,
      beds__lte: 20
    });
  };
  queryStringParse = function(string) {
    let parsed = {};
    if (string !== "") {
      string = string.substring(string.indexOf("?") + 1);
      let p1 = string.split("&");
      p1.array.forEach(element => {
        let params = element.split("=");
        parsed[params[0]] = params[1];
      });
    }
    return parsed;
  };
  search = e => {
    const { city__id, start_date, end_date, guests } = this.state;
    let params = {
      city__id,
      start_date,
      end_date,
      guests
    };
    const { getHouses } = this.props;
    getHouses(params);
  };
  applyFilter = e => {
    const {
      city__id,
      start_date,
      end_date,
      guests,
      price__gte,
      price__lte,
      beds__gte,
      beds__lte,
      rooms__gte,
      rooms__lte
    } = this.state;
    let params = {
      city__id,
      start_date,
      end_date,
      guests,
      price__gte,
      price__lte,
      beds__gte,
      beds__lte,
      rooms__gte,
      rooms__lte
    };
    if (this.state.type.value !== 0)
      params["house_type__name"] = this.state.type.label;
    if (this.state.accommodations.length > 0)
      params["accommodations"] = this.state.accommodations.map(item => item.id);
    const paramString = new URLSearchParams(params);
    this.props.history.push({
      pathname: "/results",
      search: `?${paramString.toString()}`
    });
    const { getHouses } = this.props;
    getHouses(params);
    this.setState({
      filterOpen: false
    });
  };
  toggleFavs = (event, liked, id) => {
    event.stopPropagation();
    toggleFavourite(liked, id).then(d => {
      const paramsUrl = new URLSearchParams(this.props.location.search);
      const params = {};
      for (var pair of paramsUrl.entries()) {
        params[pair[0]] = pair[1];
      }
      const { getHouses } = this.props;
      getHouses(params);
    });
  };

  render() {
    const { loading } = this.state;
    const { houses, reference, auth } = this.props;

    return (
      <Fragment>
        <div className="Results__filter">
          <label
            className={`Results__filter--label ${
              this.state.mapVisibility ? "Results__filter--label-checked" : null
            }`}
            onClick={this.mapVisibilityChangeHandler}
            htmlFor="mapVisibility"
          >
            Показать на карте
          </label>
          <Options
            marginRight={10}
            marginBottom={15}
            placeholder="Куда угодно"
            defaultValue={{
              value: this.state.city__id,
              label: this.state.city_name
            }}
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
          <input
            className="Results__filter--input"
            name="from"
            type="text"
            readOnly="readonly"
            onFocus={this.dateFocusHandler}
            placeholder="дд/мм/гггг"
            value={
              this.state.start_date === ""
                ? ""
                : this.convert(new Date(this.state.start_date))
            }
          />
          <input
            className="Results__filter--input"
            name="to"
            type="text"
            readOnly="readonly"
            onFocus={this.dateFocusHandler}
            placeholder="дд/мм/гггг"
            value={
              this.state.end_date === ""
                ? ""
                : this.convert(new Date(this.state.end_date))
            }
          />

          {this.state.focusedInput !== null ? (
            <div className="Results--datepicker">
              <DatePicker
                onClose={e => {
                  e.preventDefault();
                  this.setState({
                    focusedInput: null
                  });
                }}
                onDatesChange={data => {
                  console.log(data);
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
          <input
            className="Results__filter--input"
            type="number"
            placeholder="Гости"
            value={this.state.guests}
            onChange={e => this.setState({ guests: e.target.value })}
          />
          <button onClick={this.search} className="Results__filter--button">
            Найти
          </button>
          <button
            onClick={this.toggleFilter}
            className="Results__filter--filter-button"
            aria-controls="collapse-filter"
            aria-expanded={this.state.filterOpen}
          >
            Фильтры{" "}
            {this.state.filterOpen ? (
              <Fa icon={faAngleUp} />
            ) : (
              <Fa icon={faAngleDown} />
            )}
          </button>
        </div>
        <Collapse in={this.state.filterOpen}>
          <div id="collapse-filter" className="Results__big-filter">
            <p className="Results__big-filter--title">Применить фильтры</p>
            <Row>
              <Col sm={12} md={6} lg={4}>
                <label
                  onClick={() => {
                    this.setState({
                      certifiedHouse: !this.state.certifiedHouse
                    });
                  }}
                  className={`Results__big-filter--label Results__filter--label ${
                    this.state.certifiedHouse
                      ? "Results__filter--label-checked"
                      : null
                  }`}
                >
                  Проверенное жильё
                </label>
                <br />
                <div className="Results__big-filter--select">
                  <TypeOptions
                    placeholder="Выбрать"
                    value={this.state.type}
                    onInputChange={this.onInputChange}
                    onChange={this.typeChangeHanlder}
                    defaultValue={this.state.type}
                    options={
                      reference.houseTypes &&
                      reference.houseTypes.map(type => {
                        return {
                          value: type.id,
                          label: type.name
                        };
                      })
                    }
                  />
                </div>
                <p className="Results__big-filter--label">Тип жилья</p>
                <div className="Results__big-filter--sort">
                  <button
                    name="none"
                    onClick={this.toggleSortOption}
                    className={`Results__big-filter--sort-option ${
                      this.state.sort === "none"
                        ? "Results__big-filter--sort-selected"
                        : null
                    }`}
                  >
                    нет
                  </button>
                  <button
                    name="raiting"
                    onClick={this.toggleSortOption}
                    className={`Results__big-filter--sort-option  ${
                      this.state.sort === "raiting"
                        ? "Results__big-filter--sort-selected"
                        : null
                    }`}
                  >
                    по рейтингу
                  </button>
                  <button
                    name="price"
                    onClick={this.toggleSortOption}
                    className={`Results__big-filter--sort-option  ${
                      this.state.sort === "price"
                        ? "Results__big-filter--sort-selected"
                        : null
                    }`}
                  >
                    по цене
                  </button>
                </div>
                <p className="Results__big-filter--label">Сортировка</p>
              </Col>
              <Col sm={12} md={6} lg={4}>
                <div className="Results__big-filter--range-block">
                  <div className="Results__big-filter--range-block-wrapper">
                    <p className="Results__big-filter--range-label">Цена</p>
                    <p className="Results__big-filter--small">
                      {this.state.price__gte}-{this.state.price__lte} kzt
                    </p>
                  </div>
                  <ReactSlider
                    onChange={this.priceSliderChangeHandler}
                    className="Results__slider"
                    thumbClassName="Results__slider--thumb"
                    renderTrack={Track}
                    defaultValue={[
                      this.state.price__gte,
                      this.state.price__lte
                    ]}
                    value={[this.state.price__gte, this.state.price__lte]}
                    ariaLabel={["Lower thumb", "Upper thumb"]}
                    ariaValuetext={state => `Thumb value ${state.valueNow}`}
                    pearling
                    min={100}
                    max={50000}
                    minDistance={10000}
                  />
                </div>
                <div className="Results__big-filter--range-block">
                  <div className="Results__big-filter--range-block-wrapper">
                    <p className="Results__big-filter--range-label">
                      Кол-во комнат
                    </p>
                    <p className="Results__big-filter--small">
                      {this.state.rooms__gte}-{this.state.rooms__lte}
                    </p>
                  </div>
                  <ReactSlider
                    onChange={this.roomsSliderChangeHandler}
                    className="Results__slider"
                    thumbClassName="Results__slider--thumb"
                    renderTrack={Track}
                    value={[this.state.rooms__gte, this.state.rooms__lte]}
                    ariaLabel={["Lower thumb", "Upper thumb"]}
                    ariaValuetext={state => `Thumb value ${state.valueNow}`}
                    pearling
                    min={1}
                    max={20}
                    minDistance={5}
                  />
                </div>
                <div className="Results__big-filter--range-block">
                  <div className="Results__big-filter--range-block-wrapper">
                    <p className="Results__big-filter--range-label">
                      Кол-во кроватей
                    </p>
                    <p className="Results__big-filter--small">
                      {this.state.beds__gte}-{this.state.beds__lte}
                    </p>
                  </div>
                  <ReactSlider
                    onChange={this.bedsSliderChangeHandler}
                    className="Results__slider"
                    thumbClassName="Results__slider--thumb"
                    renderTrack={Track}
                    value={[this.state.beds__gte, this.state.beds__lte]}
                    ariaLabel={["Lower thumb", "Upper thumb"]}
                    ariaValuetext={state => `Thumb value ${state.valueNow}`}
                    pearling
                    min={1}
                    max={50}
                    minDistance={10}
                  />
                </div>
              </Col>
              <Col sm={12} md={6} lg={4}>
                {reference.accommodations ? (
                  <CheckboxGroup
                    container={this.state.accommodations}
                    title="Удобства:"
                    size="sm"
                    name="accommodations"
                    onChange={this.onAccommodationsChange}
                    array={reference.accommodations}
                  />
                ) : (
                  ""
                )}
              </Col>
              <Col md={6} lg={12} className="flex">
                <button
                  onClick={this.applyFilter}
                  className="Results__big-filter--button"
                >
                  Применить
                </button>
                <button
                  onClick={this.resetFilter}
                  className="Results__big-filter--reset-button"
                >
                  Сбросить всё
                </button>
              </Col>
            </Row>
          </div>
        </Collapse>
        <div className="Results">
          {this.state.mapVisibility ? (
            <div className="Results__map">
              <YMaps>
                <Map width="100%" height="100%" defaultState={mapData}>
                  {houses.results &&
                    houses.results.map(coordinate => (
                      <Placemark
                        geometry={[coordinate.latitude, coordinate.longitude]}
                      />
                    ))}
                </Map>
              </YMaps>
            </div>
          ) : null}
          <Container>
            <h3 className="Results__list--title">Более 300 вариантов жилья</h3>

            <Row>
              {loading === false || (houses && houses.count > 0) ? (
                houses.results.map((result, index) => (
                  <Col key={index} xl={4} md={6}>
                    <House
                      id={result.id}
                      result={result}
                      isAuthenticated={auth.isAuthenticated}
                      index={index}
                    />
                  </Col>
                ))
              ) : houses.count === 0 ? (
                <div className="Results__empty">Не найдено</div>
              ) : (
                <Loader
                  type="Puff"
                  color="#CD3232"
                  height={100}
                  width={100}
                  timeout={20000}
                />
              )}
            </Row>
          </Container>
        </div>
      </Fragment>
    );
  }
}
function mapStateToProps(state) {
  return {
    auth: state.auth,
    user: state.auth.user,
    houses: state.house.houses,
    reference: state.reference
  };
}

export default connect(mapStateToProps, {
  getHouses,
  getAccommodations,
  getHouseTypes
})(withRouter(Results));
