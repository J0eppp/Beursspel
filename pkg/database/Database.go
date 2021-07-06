package database

import (
	"beursspel/pkg/user"
	"context"
	"log"

	"github.com/J0eppp/goauthenticator"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// The database structure contains all the information about the MongoDB database
type Database struct {
	Client   *mongo.Client
	Database *mongo.Database
	Ctx      context.Context
}

func NewDatabase(uri string, ctx context.Context) (Database, error) {
	var db Database
	client, err := mongo.NewClient(options.Client().ApplyURI(uri))
	if err != nil {
		return db, err
	}

	db.Ctx = ctx

	db.Client = client
	err = client.Connect(ctx)
	if err != nil {
		return db, err
	}

	db.Database = client.Database("Beursspel")

	return db, nil
}

// Database functions

// GetUserPasswordAndSalt gets the hash and salt from the database corresponding to the users name
func (db *Database) GetUserPasswordAndSalt(username string) (string, string, error) {
	var u user.User
	err := db.Database.Collection("users").FindOne(db.Ctx, bson.M{
		"username": username,
	}).Decode(&u)
	if err != nil {
		return "", "", err
	}

	return u.Hash, u.Salt, nil
}

func (db *Database) GetSessionFromDatabase(sessionToken string) (goauthenticator.Session, error) {
	var session goauthenticator.Session
	err := db.Database.Collection("sessions").FindOne(db.Ctx, bson.M{
		"sessionToken": sessionToken,
	}).Decode(&session)
	return session, err
}

func (db *Database) SaveSessionToDatabase(uid string, session goauthenticator.Session) error {
	//_, err := db.Database.Collection("sessions").UpdateOne(db.Ctx, bson.M{
	//	"username": uid,
	//}, bson.M{
	//	"$set": bson.M{"session": session},
	//})
	_, err := db.Database.Collection("sessions").InsertOne(db.Ctx, session)
	return err
}

func (db *Database) RemoveSession(uid string) error {
	_, err := db.Database.Collection("sessions").DeleteMany(db.Ctx, bson.M{
		"uid": uid,
	})
	return err
}

func (db *Database) SaveNewUser(u user.User) error {
	log.Println("Saving the user to the DB")
	_, err := db.Database.Collection("users").InsertOne(db.Ctx, u)
	return err
}
