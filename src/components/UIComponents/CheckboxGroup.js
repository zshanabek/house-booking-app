import React, { Component, Fragment } from "react";
import "./CheckboxGroup.scss";
export default class CheckboxGroup extends Component {
  checkboxChangeHandler = (e, item) => {
    let array = this.props.container;
    if (this.containsObject(item.name, this.props.container)) {
      array = array.filter(
        elem => elem.name.toString() !== item.name.toString()
      );
    } else {
      array.push(item);
    }
    this.props.onChange(this.props.name, array);
  };
  containsObject = (name, list) => {
    let i;
    for (i = 0; i < list.length; i++) {
      if (list[i]["name"] === name) {
        return true;
      }
    }
    return false;
  };
  render() {
    const size = this.props.size
      ? this.props.size
      : window.screen.availWidth <= 450
      ? "sm"
      : "";

    return (
      <Fragment>
        <p className={`CheckboxGroup--title${size === "sm" ? "-sm" : ""}`}>
          {this.props.title}
        </p>
        <div className="CheckboxGroup--group">
          {this.props.array.map((item, index) => (
            <label
              key={index}
              name={this.props.name}
              item={item.name}
              className={`CheckboxGroup--label ${
                this.containsObject(item.name, this.props.container)
                  ? "CheckboxGroup--label-checked"
                  : ""
              } ${size === "sm" ? "CheckboxGroup--sm" : ""}`}
              onClick={e => this.checkboxChangeHandler(e, item)}
            >
              {item.name}
            </label>
          ))}
        </div>
      </Fragment>
    );
  }
}
