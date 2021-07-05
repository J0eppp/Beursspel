package server

import (
	"encoding/json"
	"log"
	"net/http"
)

func (s *Server) Session(w http.ResponseWriter, r *http.Request) {
	c, err := r.Cookie("sessionToken")
	if err != nil {
		w.WriteHeader(500)
		response := struct{
			Error bool `json:"error"`
			Message string `json:"message"`
		}{
			Error: true,
			Message: err.Error(),
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}
	sessionToken := c.Value

	session, err := s.Authenticator.SessionHandler.GetSessionFromDatabase(sessionToken)
	if err != nil {
		w.WriteHeader(500)
		response := struct{
			Error bool `json:"error"`
			Message string `json:"message"`
		}{
			Error: true,
			Message: err.Error(),
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}
	log.Println("Sending session data...")
	err = json.NewEncoder(w).Encode(session)
	if err != nil {
		log.Println(err)
	}
}
