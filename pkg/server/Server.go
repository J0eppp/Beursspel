package server

import (
	"beursspel/pkg/database"
	"github.com/J0eppp/goauthenticator"
	"github.com/gorilla/mux"
)

type Server struct {
	Database database.Database
	Router *mux.Router
	ProtectedRouter *mux.Router
	Authenticator goauthenticator.Authenticator
}
