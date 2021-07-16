import { Component } from 'react'
import { Redirect } from 'react-router-dom';

export default class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			username: null,

		}
	}

	componentDidMount() {
		(async () => {
			let url = `${process.env.REACT_APP_BASE_BACKEND_URI}/v1/me`;
			const req = await fetch(url, { headers: { "Authentication": localStorage.getItem("session") } })
			const json = await req.json();
			this.setState({ ...this.state, username: json["username"] })
		})();
	}
	
	render() {
		return (
			<div>
				{this.props.getState().redirectToLogin === true && <Redirect to="/login" />}
				Welcome {this.state.username != null ? this.state.username : "unkown"}
			</div>
		)
	}
}
