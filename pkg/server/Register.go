package server

import (
	"beursspel/pkg/user"
	"encoding/json"
	"log"
	"net/http"
	"strings"
)

type registerRequest struct {
	Username        string `json:"username"`
	Email           string `json:"email"`
	Password        string `json:"password"`
	ConfirmPassword string `json:"confirmPassword"`
}

func (s *Server) Register(w http.ResponseWriter, r *http.Request) {
	request := new(registerRequest)
	err := json.NewDecoder(r.Body).Decode(&request)
	if err != nil {
		w.Header().Set("Status", "500")
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

	if strings.Compare(request.Password, request.ConfirmPassword) != 0 {
		w.Header().Set("Status", "400")
		response := struct {
			Error   bool   `json:"error"`
			Message string `json:"message"`
		}{
			Error:   true,
			Message: "The passwords do not match",
		}
		err = json.NewEncoder(w).Encode(response)
		if err != nil {
			log.Println(err)
		}
		return
	}

	salt := s.Authenticator.CreateSalt()
	hash := s.Authenticator.Hash(request.Password, salt)

	u := user.User{
		Username: request.Username,
		Email:    request.Email,
		Hash:     string(hash),
		Salt:     string(salt),
	}

	err = s.Database.SaveNewUser(u)
	if err != nil {
		w.Header().Set("Status", "500")
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

	response := struct {
		Success bool `json:"success"`
	}{
		Success: true,
	}

	err = json.NewEncoder(w).Encode(response)
	if err != nil {
		log.Println(err)
	}
	return
}
