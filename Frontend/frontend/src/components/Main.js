import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import Navbar from './chat/Navbar';
//Create a Main Component
class Main extends Component {
    render() {
        return (
            <div>
                <Route exact path="/" component={Navbar} />
            </div>
        )
    }
}
export default Main;