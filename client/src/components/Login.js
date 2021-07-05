import { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Form, Button, Alert } from 'react-bootstrap';

import '../css/login.css';

export default class Login extends Component {
	constructor(props) {
		super(props);
		this.state = {
			showErrorMessage: false,
			errorMessage: "",
			username: "",
			password: "",
			setSession: props.setSession,
			setLoggedIn: props.setLoggedIn,
		}
	}

	render() {
		return (
			<div>
				{this.props.getState().loggedIn === true ? <Redirect to="/" /> : null}
				{this.state.showErrorMessage && <Alert variant="danger">{this.state.errorMessage}</Alert>}
				<Form className="loginForm" onSubmit={this.onLogin}>
					<Form.Group controlId="username">
						<Form.Label>Username</Form.Label>
						<Form.Control type="text" onChange={e => this.setState({ ...this.state, username: e.target.value })} placeholder="Enter username" />
						<Form.Text className="text-muted">Text</Form.Text>
					</Form.Group>
					<Form.Group controlId="password">
						<Form.Label>Password</Form.Label>
						<Form.Control type="password" onChange={e => this.setState({ ...this.state, password: e.target.value })} placeholder="Password" />
					</Form.Group>
					{/* <Form.Group controlId="formBasicCheckbox">
						<Form.Check type="checkbox" label="Check me out" />
					</Form.Group> */}
					<Button className="loginButton" variant="primary" type="submit">
						Submit
					</Button>
				</Form>
			</div>
		)
	}


	onLogin = (e) => {
		e.preventDefault();
		this.sendLoginRequest();
	}

	sendLoginRequest = async () => {
		console.log(this.state);
		let url = `${process.env.REACT_APP_BASE_BACKEND_URI}/login`;
		let attempt = await fetch(url, {
			"method": "POST",
			// "mode": "no-cors",
			"body": JSON.stringify({ username: this.state.username, password: this.state.password })
		});
		let json = await attempt.json();
		if (json.error === true) {
			// Failed to login
			this.setState({ ...this.state, showErrorMessage: true, errorMessage: json.message })
			return;
		}

		alert(json.sessionToken)
		this.setState({ ...this.state, showErrorMessage: false, errorMessage: "" })
		// Set the token in the "master" state (of App)
		this.state.setSession(json);
		this.state.setLoggedIn(true);
	};
}
