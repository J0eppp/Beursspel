import { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';

export default class App extends Component {
	constructor() {
		super();
		this.state = {
			loggedIn: false,
			session: null,
			redirectToLogin: false,
		};
	}

	componentDidMount() {
		// Check if there is a valid session saved
		(async () => {
			let url = `${process.env.REACT_APP_BASE_BACKEND_URI}/api/v1/session`;
			// const req = await fetch(url, { credentials: "include" });
			const req = await fetch(url, { headers: { "Authentication": localStorage.getItem("session") } })
			const json = await req.json();
			if (json.token) {
				this.setState({ loggedIn: true, session: json.token })
			} else {
				this.setState({ ...this.state, redirectToLogin: true })
			}
		})();
	}

	setRedirectToLogin = b => this.setState({ ...this.state, redirectToLogin: b })

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
						<Login setRedirectToLogin={this.setRedirectToLogin} setSession={this.setSession} setLoggedIn={this.setLoggedIn} getState={this.getState} />
					</Route>
					<Route path="/register">
						<Register setRedirectToLogin={this.setRedirectToLogin} setSession={this.setSession} setLoggedIn={this.setLoggedIn} getState={this.getState} />
					</Route>
				</Switch>
			</Router>
		)
	}
}