package user

type User struct {
	Username string `json:"username" bson:"username"`
	Email string `json:"email" bson:"email"`
	Hash string `json:"hash" bson:"hash"`
	Salt string `json:"salt" bson:"salt"`
}
