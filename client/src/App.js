import { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import Home from './components/Home';
import Login from './components/Login';

export default class App extends Component {
	constructor() {
		super();
		this.state = {
			loggedIn: false,
		}
	}

	setLoggedIn = loggedIn => {
		this.setState({
			...this.state,
			loggedIn: loggedIn,
		})
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
						<Login setLoggedIn={this.setLoggedIn} getState={this.getState} />
					</Route>
				</Switch>
			</Router>
		)
	}
}