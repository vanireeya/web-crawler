import React, { Component } from 'react';
import './App.css';
import Main from './components/Main';
import { BrowserRouter } from 'react-router-dom';
import { library } from '@fortawesome/fontawesome-svg-core'
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
// import { faStroopwafel } from '@fortawesome/free-solid-svg-icons'

// library.add(faStroopwafel)


class App extends Component {
  render() {
    // setInterval(function () { console.log("hello interval") }, 10000);
    return (

      <BrowserRouter>
        <div>
          <Main />
        </div>
      </BrowserRouter>

    );
  }
}

export default App;
