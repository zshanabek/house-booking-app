import React, { Component } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";

import { mainBackground } from "../../../assets/images/images";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import ReactStars from "react-rating-stars-component";
import { faHeart, faMapMarkerAlt } from "@fortawesome/free-solid-svg-icons";
import { faHeart as faHeartReg } from "@fortawesome/free-regular-svg-icons";
import { createFavourite, deleteFavourite } from "../../../services/favourites";
import { editFavourite } from "../../../actions/house.action";

class House extends Component {
  goToResult = () => {
    this.props.history.push("/housing/" + this.props.id);
  };
  toggleFavs = (event, liked) => {
    event.stopPropagation();
    const { id, index, editFavourite, result } = this.props;
    if (!liked) {
      result.is_favourite = true;
      createFavourite(id)
        .then(data => {
          editFavourite(index, false, result);
        })
        .catch(error => {
          editFavourite(index, true);
        });
    } else {
      result.is_favourite = false;
      deleteFavourite(id, index)
        .then(data => {
          editFavourite(index, false, result);
        })
        .catch(error => {});
    }
  };

  render() {
    const { result, isAuthenticated } = this.props;
    return (
      <div>
        <div className="Results__list--item" onClick={this.goToResult}>
          <div className="Results__list--item-top">
            {isAuthenticated ? (
              <div
                onClick={e => {
                  this.toggleFavs(e, result.is_favourite);
                }}
                className={`Results__list--like ${
                  result.is_favourite === true ? "Results__list--liked" : ""
                }`}
              >
                {result.is_favourite === true ? (
                  <Fa icon={faHeart} />
                ) : (
                  <Fa icon={faHeartReg} />
                )}
              </div>
            ) : (
              ""
            )}

            <img
              className="Results__list--image"
              src={
                result.photos
                  ? "http://185.22.65.18/" + result.photos[0].image
                  : mainBackground
              }
              alt=""
            />
            <p className="Results__list--price">{result.price} тг/сутки</p>
          </div>
          <div className="Results__list--item-bottom">
            <p className="Results__list--type">{result.house_type}</p>
            <p className="Results__list--name">
              {result.name.length > 15
                ? result.name.substring(0, 15) + "..."
                : result.name}
            </p>
            <p className="Results__list--details">
              {result.guests} гость(-я), {result.rooms} комната(-ы),{" "}
              {result.beds} кровать(-и){" "}
            </p>
            <h2 className="Results__list--place">
              <Fa icon={faMapMarkerAlt} />
              {result.city}
            </h2>
            <button className="Results__list--button">Смотреть</button>
            <ReactStars
              edit={false}
              count={5}
              value={result.rating}
              onChange={this.ratingChanged}
              size={22}
              color1={"#bdbcbc"}
              color2={"#CD3232"}
            />
          </div>
        </div>
      </div>
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
  editFavourite
})(withRouter(House));
