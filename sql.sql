BEGIN;
--
-- Create model Activity
--
CREATE TABLE "afternoon_activity_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activity" varchar(20) NOT NULL);
--
-- Create model Afternoon_Activity
--
CREATE TABLE "afternoon_activity_afternoon_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "second_activity" bool NOT NULL, "perference" integer NOT NULL, "activity_id" bigint NOT NULL REFERENCES "afternoon_activity_activity" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Cabin
--
CREATE TABLE "afternoon_activity_cabin" ("cabin_number" integer NOT NULL PRIMARY KEY);
--
-- Create model Camper
--
CREATE TABLE "afternoon_activity_camper" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Counselor
--
CREATE TABLE "afternoon_activity_counselor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Campers_Afternoon_Relation
--
CREATE TABLE "afternoon_activity_campers_afternoon_relation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "afternoon_activity_id" bigint NOT NULL REFERENCES "afternoon_activity_afternoon_activity" ("id") DEFERRABLE INITIALLY DEFERRED, "camper_id" bigint NOT NULL REFERENCES "afternoon_activity_camper" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create constraint perference_in_range on model afternoon_activity
--
CREATE TABLE "new__afternoon_activity_afternoon_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "second_activity" bool NOT NULL, "perference" integer NOT NULL, "activity_id" bigint NOT NULL REFERENCES "afternoon_activity_activity" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "perference_in_range" CHECK (("perference" >= 0 AND "perference" <= 3)));
INSERT INTO "new__afternoon_activity_afternoon_activity" ("id", "date", "second_activity", "perference", "activity_id") SELECT "id", "date", "second_activity", "perference", "activity_id" FROM "afternoon_activity_afternoon_activity";
DROP TABLE "afternoon_activity_afternoon_activity";
ALTER TABLE "new__afternoon_activity_afternoon_activity" RENAME TO "afternoon_activity_afternoon_activity";
CREATE INDEX "afternoon_activity_camper_cabin_id_cc8ba3d9" ON "afternoon_activity_camper" ("cabin_id");
CREATE INDEX "afternoon_activity_counselor_cabin_id_7f8d6848" ON "afternoon_activity_counselor" ("cabin_id");
CREATE INDEX "afternoon_activity_campers_afternoon_relation_afternoon_activity_id_2611e676" ON "afternoon_activity_campers_afternoon_relation" ("afternoon_activity_id");
CREATE INDEX "afternoon_activity_campers_afternoon_relation_camper_id_3267bca2" ON "afternoon_activity_campers_afternoon_relation" ("camper_id");
CREATE INDEX "afternoon_activity_afternoon_activity_activity_id_61f9396c" ON "afternoon_activity_afternoon_activity" ("activity_id");
COMMIT;

BEGIN;
--
-- Add field week_one to cabin
--
CREATE TABLE "new__afternoon_activity_cabin" ("week_one" bool NOT NULL, "cabin_number" integer NOT NULL PRIMARY KEY);
INSERT INTO "new__afternoon_activity_cabin" ("cabin_number", "week_one") SELECT "cabin_number", 1 FROM "afternoon_activity_cabin";
DROP TABLE "afternoon_activity_cabin";
ALTER TABLE "new__afternoon_activity_cabin" RENAME TO "afternoon_activity_cabin";
COMMIT;


BEGIN;
--
-- Add field max_participants to activity
--
CREATE TABLE "new__afternoon_activity_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "max_participants" integer NOT NULL, "activity" varchar(20) NOT NULL);
INSERT INTO "new__afternoon_activity_activity" ("id", "activity", "max_participants") SELECT "id", "activity", 20 FROM "afternoon_activity_activity";
DROP TABLE "afternoon_activity_activity";
ALTER TABLE "new__afternoon_activity_activity" RENAME TO "afternoon_activity_activity";
--
-- Create model Group
--
CREATE TABLE "afternoon_activity_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_name" varchar(30) NULL);
CREATE TABLE "afternoon_activity_group_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" bigint NOT NULL REFERENCES "afternoon_activity_group" ("id") DEFERRABLE INITIALLY DEFERRED, "cabin_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field allowed_groups to activity
--
ALTER TABLE "afternoon_activity_activity" ADD COLUMN "allowed_groups_id" bigint NULL REFERENCES "afternoon_activity_group" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX "afternoon_activity_group_group_group_id_cabin_id_40f3347f_uniq" ON "afternoon_activity_group_group" ("group_id", "cabin_id");
CREATE INDEX "afternoon_activity_group_group_group_id_db9ba632" ON "afternoon_activity_group_group" ("group_id");
CREATE INDEX "afternoon_activity_group_group_cabin_id_e03ff94c" ON "afternoon_activity_group_group" ("cabin_id");
CREATE INDEX "afternoon_activity_activity_allowed_groups_id_4939a808" ON "afternoon_activity_activity" ("allowed_groups_id");
COMMIT;

BEGIN;
--
-- Alter field allowed_groups on activity
--
CREATE TABLE "new__afternoon_activity_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "allowed_groups_id" bigint NOT NULL REFERENCES "afternoon_activity_group" ("id") DEFERRABLE INITIALLY DEFERRED, "activity" varchar(20) NOT NULL, "max_participants" integer NOT NULL);
INSERT INTO "new__afternoon_activity_activity" ("id", "activity", "max_participants", "allowed_groups_id") SELECT "id", "activity", "max_participants", coalesce("allowed_groups_id", 3) FROM "afternoon_activity_activity";
DROP TABLE "afternoon_activity_activity";
ALTER TABLE "new__afternoon_activity_activity" RENAME TO "afternoon_activity_activity";
CREATE INDEX "afternoon_activity_activity_allowed_groups_id_4939a808" ON "afternoon_activity_activity" ("allowed_groups_id");
COMMIT;

BEGIN;
--
-- Add field email to counselor
--
CREATE TABLE "new__afternoon_activity_counselor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(254) NOT NULL UNIQUE, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__afternoon_activity_counselor" ("id", "first_name", "last_name", "cabin_id", "email") SELECT "id", "first_name", "last_name", "cabin_id", 'test@gmail.com' FROM "afternoon_activity_counselor";
DROP TABLE "afternoon_activity_counselor";
ALTER TABLE "new__afternoon_activity_counselor" RENAME TO "afternoon_activity_counselor";
CREATE INDEX "afternoon_activity_counselor_cabin_id_7f8d6848" ON "afternoon_activity_counselor" ("cabin_id");
--
-- Add field user to counselor
--
CREATE TABLE "new__afternoon_activity_counselor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED, "email" varchar(254) NOT NULL UNIQUE, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__afternoon_activity_counselor" ("id", "first_name", "last_name", "cabin_id", "email", "user_id") SELECT "id", "first_name", "last_name", "cabin_id", "email", 3 FROM "afternoon_activity_counselor";
DROP TABLE "afternoon_activity_counselor";
ALTER TABLE "new__afternoon_activity_counselor" RENAME TO "afternoon_activity_counselor";
CREATE INDEX "afternoon_activity_counselor_cabin_id_7f8d6848" ON "afternoon_activity_counselor" ("cabin_id");
--
-- Alter field max_participants on activity
--
CREATE TABLE "new__afternoon_activity_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activity" varchar(20) NOT NULL, "allowed_groups_id" bigint NOT NULL REFERENCES "afternoon_activity_group" ("id") DEFERRABLE INITIALLY DEFERRED, "max_participants" integer NOT NULL);
INSERT INTO "new__afternoon_activity_activity" ("id", "activity", "allowed_groups_id", "max_participants") SELECT "id", "activity", "allowed_groups_id", "max_participants" FROM "afternoon_activity_activity";
DROP TABLE "afternoon_activity_activity";
ALTER TABLE "new__afternoon_activity_activity" RENAME TO "afternoon_activity_activity";
CREATE INDEX "afternoon_activity_activity_allowed_groups_id_4939a808" ON "afternoon_activity_activity" ("allowed_groups_id");
COMMIT;

BEGIN;
--
-- Alter field email on counselor
--
CREATE TABLE "new__afternoon_activity_counselor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email" varchar(50) NOT NULL UNIQUE, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__afternoon_activity_counselor" ("id", "first_name", "last_name", "cabin_id", "user_id", "email") SELECT "id", "first_name", "last_name", "cabin_id", "user_id", "email" FROM "afternoon_activity_counselor";
DROP TABLE "afternoon_activity_counselor";
ALTER TABLE "new__afternoon_activity_counselor" RENAME TO "afternoon_activity_counselor";
CREATE INDEX "afternoon_activity_counselor_cabin_id_7f8d6848" ON "afternoon_activity_counselor" ("cabin_id");
COMMIT;