import React, { Component } from "react";
import "./Chat.scss";

import { getAllChats, getConversation, sendMessage } from "../../services/chat";
import { format } from "date-fns";
import { FontAwesomeIcon as Fa } from "@fortawesome/react-fontawesome";
import { faPlus, faAngleLeft } from "@fortawesome/free-solid-svg-icons";
import {
  ThemeProvider,
  ChatList,
  Avatar,
  Column,
  ChatListItem,
  Row,
  Title,
  Subtitle,
  MessageList,
  MessageGroup,
  Message,
  MessageText,
  TextComposer,
  IconButton,
  TextInput,
  SendButton,
  MessageMedia
} from "@livechat/ui-kit";
import { connect } from "react-redux";

const theme = {
  vars: {
    "primary-color": "#427fe1",
    "secondary-color": "#fbfbfb",
    "tertiary-color": "#fff",
    "avatar-border-color": "blue"
  },
  ChatList: {
    css: {
      background: "#fff",
      width: "100%",
      borderRight: "1px solid #A4A1A1",
      height: "100vh",
      overflowY: "scroll"
    }
  },
  ChatListItem: {
    css: {
      padding: "20px 15px 10px 20px"
    }
  },
  Title: {
    css: {
      fontFamily: "Montserrat",
      fontStyle: "normal",
      fontWeight: 600,
      fontSize: "20px",
      lineHeight: "24px",
      color: "#1E1D4C"
    }
  },
  Subtitle: {
    css: {
      width: "100%"
    }
  },
  Avatar: {
    size: "75px",
    css: {
      background: "#DE5443",
      fontSize: "32px",
      color: "#fff"
    }
  },

  TextInput: {
    css: {
      border: "1px solid #505050"
    }
  },
  SendButton: {
    css: {
      background: "#cd3232",
      color: "#cd3232"
    }
  },
  MessageList: {
    css: {
      paddingBottom: "180px"
      // position: "relative"
    }
  },
  TextComposer: {
    css: {
      background: "#fff",
      borderTop: "1px solid #1E1D4C",
      position: "absolute",
      width: "100%",
      right: 0,
      bottom: 0,
      color: "#000"
    }
  },
  MessageText: {
    css: {
      marginBottom: "5px",
      marginTop: "5px",
      padding: "10px 15px",
      borderRadius: "30px",
      background: "#CD3232",
      fontFamily: "Montserrat",
      fontStyle: "normal",
      fontWeight: 500,
      fontSize: "16px",
      lineHeight: "20px",
      color: "#FFFFFF",
      position: "relative"
    }
  },
  MessageTitle: {},
  MessageMedia: {
    css: {
      marginBottom: "5px",
      marginTop: "5px",
      padding: "10px 0px",
      borderRadius: "15px",
      background: "#CD3232",
      fontFamily: "Montserrat",
      fontStyle: "normal",
      fontWeight: 500,
      fontSize: "16px",
      lineHeight: "20px",
      color: "#FFFFFF",
      position: "relative",
      maxWidth: "450px",
      maxHeight: "450px"
    }
  }
};
class Chat extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chatList: [],
      currentChat: null,
      chatMessages: {},
      messageMedia: null
    };
  }
  componentDidMount() {
    getAllChats()
      .then(data => {
        this.setState({
          chatList: data.data.results
        });
      })
      .catch(e => {
        console.log(e);
      });
  }
  openChat = chatItem => {
    this.setState({
      currentChat: chatItem
    });
    // this.props.history.push("/chat?sel=" + id);
    let target = {
      target: chatItem.id
    };
    getConversation(target)
      .then(data => {
        this.setState({
          chatMessages: {
            ...this.state.chatMessages,
            [chatItem.id]: data.data.results.reverse()
          }
        });
      })
      .catch(e => {
        console.log(e);
      });
  };
  send = message => {
    const { currentChat, messageMedia } = this.state;
    let data = new FormData();
    data.append("body", message);
    data.append("recipient", currentChat.id);
    if (messageMedia) {
      data.append("images", messageMedia, messageMedia.name);
    }
    sendMessage(data)
      .then(data => {
        let target = {
          target: currentChat.id
        };
        getConversation(target)
          .then(data => {
            this.setState({
              messageMedia: null,
              chatMessages: {
                ...this.state.chatMessages,
                [currentChat.id]: data.data.results.reverse()
              }
            });
          })
          .catch(e => {
            console.log(e);
          });
      })
      .catch(e => {
        console.log(e);
      });
  };
  handleFile = e => {
    this.setState({
      messageMedia: e.target.files[0]
    });
  };
  render() {
    const { chatList } = this.state;
    const { user } = this.props;
    const width = window.innerWidth;
    return (
      <div className="Chat">
        <ThemeProvider theme={theme}>
          {(width <= 700 && this.state.currentChat === null) || width > 700 ? (
            <div className="Chat__list">
              <ChatList>
                {chatList &&
                  chatList.map((chatItem, index) => (
                    <div
                      onClick={() => {
                        this.openChat(chatItem);
                      }}
                      key={index}
                    >
                      <ChatListItem>
                        <Avatar letter={chatItem.first_name[0]} />
                        <Column fill>
                          <Row justify>
                            <Title>
                              {chatItem.first_name} {chatItem.last_name}
                            </Title>
                            <Subtitle nowrap>{""}</Subtitle>
                          </Row>
                          <Subtitle ellipsis>{""}</Subtitle>
                        </Column>
                      </ChatListItem>
                    </div>
                  ))}
              </ChatList>
            </div>
          ) : (
            ""
          )}

          {this.state.currentChat !== null ? (
            <div className="Chat__conversation">
              <div className="Chat__conversation--header">
                <div
                  onClick={() => {
                    this.setState({
                      currentChat: null
                    });
                  }}
                  className="Chat__conversation--back"
                >
                  <Fa icon={faAngleLeft} />{" "}
                </div>
                {"\u00A0"}{" "}
                <Avatar letter={this.state.currentChat.first_name[0]} />
                <p className="Chat__conversation--name">
                  {this.state.currentChat.first_name}{" "}
                  {this.state.currentChat.last_name}
                </p>
              </div>
              <MessageList active>
                {this.state.chatMessages[this.state.currentChat.id] &&
                  this.state.chatMessages[this.state.currentChat.id].map(
                    (chat, index) => (
                      <MessageGroup onlyFirstWithMeta>
                        <Message
                          authorName={
                            chat.user.first_name + " " + chat.user.last_name
                          }
                          isOwn={user.id === chat.user.id}
                          date={format(new Date(chat.created_at), "hh:mm")}
                        >
                          {chat.images !== null ? (
                            <Message>
                              <MessageMedia>
                                <MessageText>{chat.body}</MessageText>
                                <img
                                  style={{
                                    objectFit: "cover",
                                    backgroundPosition: "center"
                                  }}
                                  src={
                                    "https://akv-technopark.herokuapp.com" +
                                    chat.images[0].image
                                  }
                                  alt=""
                                />
                              </MessageMedia>
                            </Message>
                          ) : (
                            <MessageText>{chat.body}</MessageText>
                          )}
                        </Message>
                      </MessageGroup>
                    )
                  )}

                {/* <MessageGroup onlyFirstWithMeta>
                        <Message date="21:38" isOwn={true} authorName="Visitor">
                          <MessageText>
                            I love them
                            sooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
                            much!
                          </MessageText>
                        </Message>
                        <Message date="21:38" isOwn={true} authorName="Visitor">
                          <MessageText>This helps me a lot</MessageText>
                        </Message>
                      </MessageGroup>
                      <MessageGroup onlyFirstWithMeta>
                        <Message authorName="Jon Smith" date="21:37">
                          <MessageText>No problem!</MessageText>
                        </Message>
                        <Message
                          authorName="Jon Smith"
                          imageUrl="https://static.staging.livechatinc.com/1520/P10B78E30V/dfd1830ebb68b4eefe6432d7ac2be2be/Cat-BusinessSidekick_Wallpapers.png"
                          date="21:39"
                        >
                          <MessageText>
                            The fastest way to help your customers - start chatting
                            with visitors who need your help using a free 30-day
                            trial.
                          </MessageText>
                        </Message>
                      </MessageGroup>
                     */}
              </MessageList>
              <TextComposer onSend={this.send}>
                <Row align="center">
                  <IconButton fit>
                    {this.state.messageMedia ? (
                      <span className="Chat__media-badge">{1}</span>
                    ) : (
                      ""
                    )}
                    <label
                      className="Chat__icon"
                      htmlFor="ChatUploadImagesPicker"
                    >
                      <Fa icon={faPlus} />
                    </label>
                    <input
                      type="file"
                      name="images"
                      accept="image/jpeg;image/png"
                      id="ChatUploadImagesPicker"
                      className="NewAd__pick-image--input"
                      onChange={this.handleFile}
                    />
                  </IconButton>
                  <TextInput
                    placeholder="Напишите сообщение..."
                    className="Chat__input"
                    fill
                  />

                  <SendButton color="#4788ef" fit />
                </Row>
              </TextComposer>
            </div>
          ) : (
            <div className="Chat__choose">
              Пожалуйста, выберите беседу или создайте новую
            </div>
          )}
        </ThemeProvider>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    user: state.auth.user
  };
}

export default connect(mapStateToProps, null)(Chat);
