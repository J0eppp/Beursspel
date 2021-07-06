package server

import (
	"encoding/json"
	"log"
	"net/http"
)

type loginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

func (s *Server) Login(w http.ResponseWriter, r *http.Request) {
	request := new(loginRequest)
	err := json.NewDecoder(r.Body).Decode(&request)
	if err != nil {
		//w.WriteHeader(500)
		//w.Header().Set("Status", "500")
		response := struct {
			Error   bool   `json:"error"`
			Message string `json:"message"`
		}{
			Error:   true,
			Message: err.Error(),
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}

	correct, err := s.Authenticator.CheckPassword(request.Username, request.Password)
	if err != nil {
		response := struct {
			Error   bool   `json:"error"`
			Message string `json:"message"`
		}{
			Error:   true,
			Message: err.Error(),
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}

	if correct == false {
		//w.Header().Set("Status", "401")
		response := struct {
			Error   bool   `json:"error"`
			Message string `json:"message"`
		}{
			Error:   true,
			Message: "you entered the wrong password or username",
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}

	// Return with a session
	session, err := s.Authenticator.SessionHandler.CreateSession(request.Username)
	if err != nil {
		response := struct {
			Error   bool   `json:"error"`
			Message string `json:"message"`
		}{
			Error:   true,
			Message: err.Error(),
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}

	err = json.NewEncoder(w).Encode(session)
	if err != nil {
		log.Println(err)
	}
}
