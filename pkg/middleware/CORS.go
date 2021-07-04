package middleware

import "net/http"

// CORS sets the Access Control Allow Origin header to '*' so there will be no CORS error
func CORS(next http.Handler) http.Handler {
	return http.HandlerFunc(
		func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Access-Control-Allow-Origin", "*")
			next.ServeHTTP(w, r)
		},
	)
}