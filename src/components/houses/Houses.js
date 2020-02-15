import React, { Component } from "react";
import "./Houses.scss";
import { mainBackground } from "../../assets/images/images";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
export default class Houses extends Component {
  constructor(params) {
    super(params);
    this.state = {
      type_id: 1
    };
  }
  componentDidMount() {
    const { type_id } = this.props.match.params;
    this.setState({
      type_id
    });
  }
  render() {
    return (
      <div className="Houses">
        <div>
          <img className="Houses__image" src={mainBackground} alt="" />
        </div>

        <Container>
          <div className="Houses__main">
            <Row>
              <Col lg={8}>
                <div className="Houses__block">
                  <h1 className="Houses__title">
                    {this.state[this.state.type_id]} в Алмате
                  </h1>
                  <p className="Houses__description">
                    Алматы - жилье на AKV. Чувствуйте себя как дома в любом
                    уголке мира. Бронируйте уникальное жилье, превосходящее все
                    ожидания! Проверенные фотографии. Клиентский сервис 24/7.
                    Гостеприимство хозяев. Более 6М предложений. Служба
                    поддержки.
                  </p>
                </div>
              </Col>
              <Col lg={4}>
                <div className="Houses__sidebar">
                  <div className="Houses__sidebar--item">
                    <img
                      className="Houses__sidebar--image"
                      src="https://techcrunch.com/wp-content/uploads/2019/03/blueground-apartment-2-2-2.jpg?w=730&crop=1"
                      alt=""
                    />
                    <h3 className="Houses__sidebar--title">Modern</h3>
                    <button className="Houses__sidebar--button">
                      Смотреть
                    </button>
                  </div>
                  <div className="Houses__sidebar--item">
                    <img
                      className="Houses__sidebar--image"
                      src="https://techcrunch.com/wp-content/uploads/2019/03/blueground-apartment-2-2-2.jpg?w=730&crop=1"
                      alt=""
                    />
                    <h3 className="Houses__sidebar--title">Apartment</h3>
                    <button className="Houses__sidebar--button">
                      Смотреть
                    </button>
                  </div>
                  <div className="Houses__sidebar--item">
                    <img
                      className="Houses__sidebar--image"
                      src="https://techcrunch.com/wp-content/uploads/2019/03/blueground-apartment-2-2-2.jpg?w=730&crop=1"
                      alt=""
                    />
                    <h3 className="Houses__sidebar--title">With Pool</h3>
                    <button className="Houses__sidebar--button">
                      Смотреть
                    </button>
                  </div>
                </div>
              </Col>
            </Row>
          </div>
        </Container>
      </div>
    );
  }
}
