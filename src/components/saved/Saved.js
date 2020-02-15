import React, { Component } from "react";
import { connect } from "react-redux";

import { getFavourites } from "../../actions/favourites.action";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";

import { faHeart } from "@fortawesome/free-solid-svg-icons";
import "./Saved.scss";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import House from "../blocks/house/House";

import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";

class Saved extends Component {
  constructor(props) {
    super(props);
    this.state = {
      favourites: null
    };
  }

  componentDidMount() {
    const { getFavourites } = this.props;
    getFavourites();
  }
  render() {
    const { favourites, auth, loading } = this.props;

    return (
      <Container>
        <div className="Saved">
          <h2 className="Saved__title">Сохранённые</h2>
          {loading === false || (favourites.results && favourites.count > 0) ? (
            <Row>
              {favourites.results.map((result, index) => (
                <Col key={index} lg={4} md={6}>
                  <House
                    index={index}
                    id={result.house.id}
                    result={result.house}
                    isAuthenticated={auth.isAuthenticated}
                  />
                </Col>
              ))}
            </Row>
          ) : favourites.count === 0 ? (
            <Loader
              type="Puff"
              color="#CD3232"
              height={100}
              width={100}
              timeout={20000}
            />
          ) : (
            <div className="Saved__empty">
              <div className="Saved__like">
                <Fa icon={faHeart} />
              </div>
              <button className="Saved__button">Найти жильё</button>

              <p className="Saved__paragraph">
                Сохраняйте понравившиеся вам жилья
                <br /> в одном месте, нажав на
                <br /> сердечку на любом жилье.
              </p>
            </div>
          )}
        </div>
      </Container>
    );
  }
}

function mapStateToProps(state) {
  return {
    auth: state.auth,
    favourites: state.favourites,
    loading: state.favourites.loading
  };
}

export default connect(mapStateToProps, {
  getFavourites
})(Saved);
