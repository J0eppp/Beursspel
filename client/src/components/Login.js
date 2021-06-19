import { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { Form, Button, Input } from 'react-bootstrap';

import '../css/login.css';

export default class Login extends Component {
	render() {
		return (
			<div>
				{this.props.getState().loggedIn === true ? <Redirect to="/" /> : null}
				<Form className="loginForm">
					<Form.Group controlId="username">
						<Form.Label>Username</Form.Label>
						<Form.Control type="text" placeholder="Enter username" />
						<Form.Text className="text-muted">Text</Form.Text>
					</Form.Group>
					<Form.Group controlId="password">
						<Form.Label>Password</Form.Label>
						<Form.Control type="password" placeholder="Password" />
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
}
