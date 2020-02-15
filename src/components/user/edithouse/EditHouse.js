import React, { Component } from "react";
import { connect } from "react-redux";
import { getHouse, updateHouse } from "../../../services/house";
import CheckboxGroup from "../../UIComponents/CheckboxGroup";
import "./EditHouse.scss";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import {
  faPlus,
  faCamera,
  faAngleLeft
} from "@fortawesome/free-solid-svg-icons";
import { faTimesCircle } from "@fortawesome/free-regular-svg-icons";
import { format } from "date-fns";
import { ru as locale } from "date-fns/locale";
import { DatePicker } from "../../UIComponents/DatePicker";
class EditAd extends Component {
  constructor(params) {
    super(params);
    this.state = {
      photos: [],
      name: "",
      description: "",

      accommodations: [],
      near_buildings: [],

      busy_days: [],
      rules: [],
      start_date: "",
      end_date: "",
      focusedInput: "startDate",
      disableEditButton: false
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
  editHouseHandler = () => {
    const {
      id,
      address,
      upload,
      name,
      description,
      accommodations,
      near_buildings,
      busy_days,
      rules,
      price
    } = this.state;

    const params = new FormData();
    params.append("name", name);
    params.append("description", description);
    if (upload) {
      for (const file of upload) {
        params.append("photos", file, file.name);
      }
    }
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
      busy_days.forEach(item => {
        params.append("blocked_dates", item.name);
      });
    }
    params.append("address", address);
    params.append("price", price);
    updateHouse(id, params)
      .then(date => {
        this.props.history.push("/myhouse/" + id);
      })
      .catch(e => {
        console.log(e);
      });
    this.setState({
      disableEditButton: true
    });
  };
  back = () => {
    this.props.history.push("/myhouse/" + this.state.id);
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
  inputChangeHandler = e => {
    this.setState({
      [e.target.name]: e.target.value
    });
  };
  checkboxGroupChangeHandler = (name, set) => {
    this.setState({
      [name]: set
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
  render() {
    const { busy_days } = this.state;
    const { reference } = this.props;
    return (
      <div className="EditAd">
        <h3 className="EditAd__title">Изменить обьявление</h3>
        <div
          className="NewAd__slick--arrow NewAd__slick--arrow-prev"
          onClick={this.back}
        >
          <Fa icon={faAngleLeft} /> {"\u00A0"} Назад
        </div>
        <p className="EditAd__label">Название</p>
        <div className="EditAd__input--wrapper">
          <input
            className="EditAd__input"
            name="name"
            value={this.state.name}
            maxLength={200}
            onChange={this.inputChangeHandler}
          />
          <span className="EditAd__input--limit">
            {this.state.name.length} / 200
          </span>
        </div>
        <p className="EditAd__label">Описание</p>
        <div className="EditAd__input--wrapper">
          <textarea
            name="description"
            value={this.state.description}
            onChange={this.inputChangeHandler}
            rows={5}
            maxLength={1000}
            className="EditAd__input"
          />
          <span className="EditAd__input--limit">
            {this.state.description.length} / 1000
          </span>
        </div>
        <p className="EditAd__label">Фотографии</p>
        <div className="NewAd__pick-image">
          {this.state.photos && this.state.photos.length > 0 ? (
            this.state.photos.map((image, index) => (
              <div key={index}>
                <img className="NewAd__pick-image--item" src={image} alt="" />
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
        <div className="NewAd__checkbox--group">
          {reference.accommodations ? (
            <CheckboxGroup
              onChange={this.checkboxGroupChangeHandler}
              name="accommodations"
              title="Удобства"
              container={this.state.accommodations}
              array={reference.accommodations}
            />
          ) : null}
        </div>
        {reference.nearBuildings ? (
          <CheckboxGroup
            onChange={this.checkboxGroupChangeHandler}
            container={this.state.near_buildings}
            name="near_buildings"
            title="Рядом есть"
            array={reference.nearBuildings}
          />
        ) : null}
        <p className="EditAd__label">Свободные даты</p>
        {busy_days.map((item, index) => (
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
        <div className="EditAd__datepicker">
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
        {reference.rules ? (
          <CheckboxGroup
            onChange={this.checkboxGroupChangeHandler}
            container={this.state.rules}
            name="rules"
            title="Правила дома"
            array={reference.rules}
          />
        ) : null}
        <p className="EditAd__label">Цена</p>
        <div className="EditAd__input--wrapper">
          <input
            value={this.state.price}
            onChange={e => this.setState({ price: e.target.value })}
            type="number"
            className="EditAd__input"
          />
          <span className="EditAd__input--price">KZT</span>
        </div>
        <p className="EditAd__label">Адрес</p>
        <input
          value={this.state.address}
          onChange={e => this.setState({ address: e.target.value })}
          className="EditAd__input"
        />
        <button
          disabled={this.state.disableEditButton}
          onClick={this.editHouseHandler}
          className="EditAd__submit"
        >
          Изменить
        </button>
      </div>
    );
  }
}
function mapStateToProps(state) {
  return {
    reference: state.reference
  };
}

export default connect(mapStateToProps, null)(EditAd);
