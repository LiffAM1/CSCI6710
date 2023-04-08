BEGIN;
-- Represents humans who are logging in. Can have one or more pets created.
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_authenticated BOOLEAN NOT NULL
);
COMMIT;

BEGIN;
-- Represents the "client" who will interact with the app.
CREATE TABLE IF NOT EXISTS pets (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    nicknames VARCHAR,
    species VARCHAR NOT NULL,
    breed VARCHAR,
    profile_pic VARCHAR NOT NULL,
    birthday DATE NOT NULL,
    gender INT NOT NULL,
    is_active BOOLEAN NOT NULL,
    CONSTRAINT fk_pets_users FOREIGN KEY(user_id) REFERENCES users(id)
);
COMMIT;

BEGIN;
-- Represents the relationship between two pets.
CREATE TABLE IF NOT EXISTS friends (
    id VARCHAR PRIMARY KEY,
    pet_id VARCHAR NOT NULL,
    friend_id VARCHAR NOT NULL,
    friend_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_friends_pets FOREIGN KEY(pet_id) REFERENCES pets(id),
    CONSTRAINT fk_friends_friends FOREIGN KEY(friend_id) REFERENCES pets(id)
);
COMMIT;

BEGIN;
-- Represents a post, which can include a photo and/or text.
CREATE TABLE IF NOT EXISTS posts (
    id VARCHAR PRIMARY KEY,
    pet_id VARCHAR NOT NULL,
    message VARCHAR,
    photo VARCHAR,
    post_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_posts_pets FOREIGN KEY(pet_id) REFERENCES pets(id)
);
COMMIT;

BEGIN;
-- Represents a pet's reaction to another pet's post. Can represent treats (type = 1) or comments (type = 2).
CREATE TABLE IF NOT EXISTS reactions (
    id VARCHAR PRIMARY KEY,
    post_id VARCHAR NOT NULL,
    pet_id VARCHAR NOT NULL,
    type INT NOT NULL,
    message VARCHAR,
    CONSTRAINT fk_reactions_posts FOREIGN KEY(post_id) REFERENCES posts(id),
    CONSTRAINT fk_reactions_pets FOREIGN KEY(pet_id) REFERENCES pets(id)
);
COMMIT;