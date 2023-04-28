BEGIN;
ALTER TABLE friends DROP CONSTRAINT fk_friends_friends;
ALTER TABLE friends ADD CONSTRAINT fk_friends_friends FOREIGN KEY (friend_id) REFERENCES public.pets(id) ON DELETE CASCADE;

ALTER TABLE friends DROP CONSTRAINT fk_friends_pets;
ALTER TABLE friends ADD CONSTRAINT fk_friends_pets FOREIGN KEY (pet_id) REFERENCES public.pets(id) ON DELETE CASCADE;
COMMIT;

BEGIN;
ALTER TABLE posts DROP CONSTRAINT fk_posts_pets;
ALTER TABLE posts ADD CONSTRAINT fk_posts_pets FOREIGN KEY (pet_id) REFERENCES public.pets(id) ON DELETE CASCADE;
COMMIT;

BEGIN;
ALTER TABLE reactions DROP CONSTRAINT fk_reactions_pets;
ALTER TABLE reactions ADD CONSTRAINT fk_reactions_pets FOREIGN KEY (pet_id) REFERENCES public.pets(id) ON DELETE CASCADE;

ALTER TABLE reactions DROP CONSTRAINT fk_reactions_posts;
ALTER TABLE reactions ADD CONSTRAINT fk_reactions_posts FOREIGN KEY (post_id) REFERENCES public.posts(id) ON DELETE CASCADE;
COMMIT;