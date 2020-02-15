import React, { Component } from "react";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import { faAngleLeft } from "@fortawesome/free-solid-svg-icons";
import "./Report.scss";
export default class Report extends Component {
  backButton = () => {
    this.props.history.push("/support");
  };
  render() {
    return (
      <div className="Report">
        <h1 className="User__title">Сообщить об ошибке</h1>
        <p className="Report__title">
          Nullam ullamcorper mattis purus eu mattis. Nam vel cursus tellus,
          venenatis posuere orci.
        </p>
        <textarea rows="10" className="Report__message" />
        <br />
        <button className="Report__send">Сообщить</button>
        <button onClick={this.backButton} className="Report__back">
          <Fa icon={faAngleLeft} /> {"\u00A0"} Назад
        </button>
      </div>
    );
  }
}
