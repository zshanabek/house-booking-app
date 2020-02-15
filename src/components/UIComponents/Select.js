import React, { Component } from "react";
import Select from "react-select";

const optionsStyle = {
  control: (styles, state) => ({
    ...styles,
    minWidth: "200px",
    backgroundColor: "white",
    height: "35px",
    border: state.isFocused ? "" : "solid 0.5px rgba(0, 0, 0, 0.7)",
    borderRadius: "3px"
  })
};

export class Options extends Component {
  render() {
    return (
      <div
        style={{
          marginRight: `${this.props.marginRight}px`,
          marginBottom: `${this.props.marginBottom}px`,
          zIndex: "10"
        }}
      >
        <Select
          styles={optionsStyle}
          placeholder={this.props.placeholder}
          onInputChange={this.props.onInputChange}
          onChange={this.props.onChange}
          defaultValue={this.props.defaultValue}
          value={this.props.value}
          theme={theme => ({
            ...theme,
            colors: {
              ...theme.colors,
              primary: "#CD3232",
              primary25: "#f5d6d6",
              neutral0: "#FFF"
            }
          })}
          options={this.props.options}
        />
      </div>
    );
  }
}
const typeSelectStyle = {
  control: (styles, state) => ({
    ...styles,
    minWidth: "90px",
    backgroundColor: "white",
    height: "24px",
    border: state.isFocused ? "" : "solid 0.8px #000",
    borderRadius: "5px",
    fontSize: "14px"
  }),
  indicatorSeparator: (styles, state) => ({
    display: "none"
  }),
  valueContainer: (styles, state) => ({
    paddingLeft: "10px",
    height: "24px"
  }),
  menuPortal: (styles, state) => ({
    zIndex: "10"
  })
};

export class TypeOptions extends Component {
  render() {
    return (
      <Select
        placeholder="Выбрать"
        styles={typeSelectStyle}
        onChange={this.props.onChange}
        defaultValue={this.props.defaultValue}
        theme={theme => ({
          ...theme,
          colors: {
            ...theme.colors,
            primary: "#CD3232",
            primary25: "#f5d6d6",
            neutral0: "#FFF"
          }
        })}
        options={this.props.options}
      />
    );
  }
}
