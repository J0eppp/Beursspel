import { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Form, Button, Alert } from 'react-bootstrap';

import '../css/login.css';

export default class Register extends Component {
	constructor(props) {
		super(props);
		this.state = {
			showErrorMessage: false,
			errorMessage: "",
			username: "",
			// email: "",
			password: "",
			confirmPassword: "",
			setSession: props.setSession,
			setLoggedIn: props.setLoggedIn,
			passwordsNotMatchAlert: false,
			registerSuccessfull: false,
		}
	}

	render() {
		return (
			<div>
				{this.props.getState().loggedIn === true ? <Redirect to="/" /> : null}
				{this.state.registerSuccessfull === true ? <Redirect to="/login" /> : null}
				<Form className="authForm" onSubmit={this.onRegister}>
					{this.state.showErrorMessage && <Alert variant="danger">{this.state.errorMessage}</Alert>}
					{this.state.password !== this.state.confirmPassword && <Alert id="passwordsNotMatch" variant={this.state.passwordsNotMatchAlert ? "danger" : "warning"}>The passwords you entered do not match</Alert>}
					<Form.Group controlId="username">
						<Form.Label>Username</Form.Label>
						<Form.Control type="text" onChange={e => this.setState({ ...this.state, username: e.target.value })} placeholder="Enter username" />
					</Form.Group>
					{/* <Form.Group controlId="Email">
						<Form.Label>Email</Form.Label>
						<Form.Control type="text" onChange={e => this.setState({ ...this.state, email: e.target.value })} placeholder="Enter email" />
					</Form.Group> */}
					<Form.Group controlId="password">
						<Form.Label>Password</Form.Label>
						<Form.Control type="password" onChange={e => this.setState({ ...this.state, password: e.target.value, passwordsNotMatchAlert: false })} placeholder="Enter password" />
					</Form.Group>
					<Form.Group controlId="confirmPassword">
						<Form.Label>Confirm password</Form.Label>
						<Form.Control type="password" onChange={e => this.setState({ ...this.state, confirmPassword: e.target.value, passwordsNotMatchAlert: false })} placeholder="Enter password" />
					</Form.Group>
					<Button className="authButton" variant="primary" type="submit">
						Register
					</Button>
				</Form>
			</div>
		)
	}


	onRegister = (e) => {
		e.preventDefault();
		this.sendRegisterRequest();
	}

	sendRegisterRequest = async () => { 
		// Check if the passwords match
		if (this.state.password !== this.state.confirmPassword) {
			this.setState({...this.state, passwordsNotMatchAlert: true})
			return;
		}
		let url = `${process.env.REACT_APP_BASE_BACKEND_URI}/api/v1/users`;

		let attempt = await fetch(url, {
			"method": "POST",
			"headers": new Headers({
				"Content-Type": "application/json"
			}),
			"body": JSON.stringify({ username: this.state.username, password: this.state.password })
		});
		let json = await attempt.json();
		if (json.error) {
			// Failed to register
			this.setState({ ...this.state, showErrorMessage: true, errorMessage: json.error })
			return;
		}

		this.setState({ ...this.state, registerSuccessfull: true })
	};
}
