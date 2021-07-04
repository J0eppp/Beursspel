package main

import (
	"beursspel/pkg/database"
	"beursspel/pkg/middleware"
	"beursspel/pkg/server"
	"context"
	"fmt"
	"github.com/J0eppp/goauthenticator"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"time"
)

var authenticator goauthenticator.Authenticator

func main() {
	server := server.Server{}

	db, err := database.NewDatabase("mongodb://localhost/Beursspel", context.Background())
	if err != nil {
		panic(err)
	}

	log.Println("Connected to the database!")

	server.Database = db

	server.Authenticator = goauthenticator.NewAuthenticator(db.GetSessionFromDatabase, db.SaveSessionToDatabase, "/login", 32, 10000, 64, db.GetUserPasswordAndSalt)

	server.Router = mux.NewRouter().StrictSlash(false)

	server.Router.Use(middleware.CORS)
	server.Router.Use(middleware.SetResponseTypeJSON)

	server.Router.HandleFunc("/login", server.Login).Methods("POST")
	server.Router.HandleFunc("/register", server.Register).Methods("POST")

	server.Router.HandleFunc("/get", getHandler)

	server.ProtectedRouter = server.Router.Path("/").Subrouter()

	server.ProtectedRouter.Use(authenticator.SessionHandler.ValidateSession)

	server.ProtectedRouter.HandleFunc("/", indexHandler)


	log.Println("Webserver is running")
	log.Fatal(http.ListenAndServe(":8000", server.Router))
}

// Protected route
func indexHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hi, I'm a protected route!")
}

// Session getter
func getHandler(w http.ResponseWriter, r *http.Request) {
	uid, ok := r.URL.Query()["uid"]
	if !ok {
		w.WriteHeader(400)
		fmt.Fprintf(w, "Bad Request, no uid GET parameter was found")
		return
	}

	session, err := authenticator.SessionHandler.CreateSession(uid[0])
	if err != nil {
		if !ok {
			w.WriteHeader(500)
			fmt.Fprintf(w, err.Error())
			return
		}
	}

	http.SetCookie(w, &http.Cookie{
		Name:       "sessionToken",
		Value:      session.SessionToken,
		Path:       "",
		Domain:     "",
		Expires:    time.Unix(session.Expires, 0),
		RawExpires: "",
		MaxAge:     0,
		Secure:     false,
		HttpOnly:   false,
		SameSite:   0,
		Raw:        "",
		Unparsed:   nil,
	})
	fmt.Fprintf(w, "Added cookie")
}