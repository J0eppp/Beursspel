import { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import Home from './components/Home';
import Login from './components/Login';

export default class App extends Component {
	constructor() {
		super();
		// Check if there is a valid session saved
		let url = `${process.env.REACT_APP_BASE_BACKEND_URI}`;
		fetch(url, { credentials: "include", mode: "no-cors" }).then(data => data.json()).then(json => console.log(json)).catch(err => console.error(err));

		this.state = {
			loggedIn: false,
			session: null,
		}
	}

	setLoggedIn = loggedIn => {
		this.setState({
			...this.state,
			loggedIn: loggedIn,
		})
	}

	setSession = session => {
		this.setState({
			...this.state,
			session: session,
		});

		// Set the session cookie
		document.cookie = `sessionToken=${session.sessionToken}`;
	}

	getState = () => this.state;

	render() {
		return (
			<Router>
				<Switch>
					<Route path="/" exact>
						<Home getState={this.getState} />
					</Route>
					<Route path="/login">
						<Login setSession={this.setSession} setLoggedIn={this.setLoggedIn} getState={this.getState} />
					</Route>
				</Switch>
			</Router>
		)
	}
}