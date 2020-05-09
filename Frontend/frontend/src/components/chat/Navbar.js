import React, { Component } from 'react';
import { Launcher } from 'react-chat-window'
import axios from 'axios';

//create the Navbar Component
class Navbar extends Component {
    constructor(props) {
        super(props);
        let myData = JSON.parse(localStorage.getItem('myData'));
        this.state = {
            myData: myData,
            messageList: [],
            context: ""
        }
        // this.sendMessage = this.sendMessage.bind(this);
    }

    componentDidMount() {

        let messageList = [{
            author: 'them',
            type: 'text',
            data: {
                text: 'How can I help you today?'
            }
        },
            // {
            //     author: 'them',
            //     type: 'text',
            //     data: {
            //         text: 'some text'
            //     }
            // }, {
            //     author: 'them',
            //     type: 'text',
            //     data: {
            //         text: 'some text'
            //     }
            // }

        ]
        this.setState({ messageList })



    }



    _onMessageWasSent(message) {
        this.setState({
            messageList: [...this.state.messageList, message]
        })
        // let data = {"question":"I am not yet disqualiefied from San Jose State University, do I still need to file for a reinstatement petition"}
        let data = { "question": message.data.text, context: this.state.context }
        axios.post('http://localhost:5003/question/', data)
            .then(response => {
                console.log("Status Code : ", response.status);
                if (response.status === 200) {
                    this._sendMessage(response.data.answer)
                    if (response.data.context !== "" && response.data.context !== null && response.data.context !== undefined) {
                        this.setState({ context: response.data.context })
                        console.log(this.state.context)
                    }
                } else {
                    this._sendMessage("I am sorry I dont understand")

                }
                //     console.log(response.data)
                //     if (response.data) {
                //         if (response.data.status === 1) {
                //             console.log(response.data.info)
                //             localStorage.setItem('myData', JSON.stringify(response.data.info));
                //             let test = JSON.parse(localStorage.getItem('myData'));
                //             // console.log(JSON.parse(test));
                //             console.log(test.firstname);
                //             this.setState({
                //                 authFlag: true,
                //                 invalidFlag: false,
                //                 myData: test
                //             })
                //         } else if (response.data.status === -1) {
                //             this.setState({
                //                 invalidFlag: true
                //             })
                //         }
                //     }

                // } else {
                //     this.setState({
                //         authFlag: false
                //     })
                // }
            });
    }

    _sendMessage(text) {
        if (text.length > 0) {
            this.setState({
                messageList: [...this.state.messageList, {
                    author: 'them',
                    type: 'text',
                    data: { text }
                }]
            })
        }



    }

    render() {
        require('./Navbar.css')
        let redirectVar = null;

        return (
            <div>
                <div style={{ "z-index": "9999999999", position: "relative" }}>
                    <nav className="navbar navbar-expand-sm" style={{ "background-color": "#0038a8", "height": "80px" }}>
                        <div className="container-fluid" style={{ marginTop: "10px" }}>
                            <div class="main-logo-holder">
                                <img src="https://dbukjj6eu5tsf.cloudfront.net/sjsuspartans.com/images/main-logo.png" />

                            </div>
                            <div className="navbar-header">
                                <img style={{ width: "350px" }} src="https://dbukjj6eu5tsf.cloudfront.net/sjsuspartans.com/images/official-header-text.png" alt="San José State Spartans - link to home" />
                            </div>
                        </div>
                    </nav>

                </div>

                <div id="mainDiv3">




                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />

                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />
                    <br />

                </div>

                <div>
                    <Launcher
                        agentProfile={{
                            teamName: 'SJSU chat box',
                            // imageUrl: 'https://dbukjj6eu5tsf.cloudfront.net/sjsuspartans.com/images/main-logo.png'
                        }}
                        onMessageWasSent={this._onMessageWasSent.bind(this)}
                        messageList={this.state.messageList}
                        showEmoji
                    />


                </div>
            </div>
        )
    }
}

export default Navbar;