import { Component } from 'react'
import { Redirect } from 'react-router-dom';

export default class Home extends Component {
	render() {
		return (
			<div>
				{this.props.getState().loggedIn === false && <Redirect to="/login" />}
				Home
			</div>
		)
	}
}
