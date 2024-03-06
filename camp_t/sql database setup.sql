BEGIN;
--
-- Create model Activity
--
CREATE TABLE "afternoon_activity_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activity" varchar(20) NOT NULL, "perference" integer NOT NULL);
--
-- Create model Afternoon_Activity
--
CREATE TABLE "afternoon_activity_afternoon_activity" ("date" date NOT NULL PRIMARY KEY, "second_activity" bool NOT NULL, "activity_id" bigint NOT NULL REFERENCES "afternoon_activity_activity" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Cabin
--
CREATE TABLE "afternoon_activity_cabin" ("cabin_number" integer NOT NULL PRIMARY KEY);
--
-- Create model Counselor
--
CREATE TABLE "afternoon_activity_counselor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_number_id" integer NOT NULL UNIQUE REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED, "possition_id" date NULL REFERENCES "afternoon_activity_afternoon_activity" ("date") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Camper
--
CREATE TABLE "afternoon_activity_camper" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(20) NOT NULL, "last_name" varchar(20) NOT NULL, "cabin_number_id" integer NOT NULL REFERENCES "afternoon_activity_cabin" ("cabin_number") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "afternoon_activity_camper_afternoon_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "camper_id" bigint NOT NULL REFERENCES "afternoon_activity_camper" ("id") DEFERRABLE INITIALLY DEFERRED, "afternoon_activity_id" date NOT NULL REFERENCES "afternoon_activity_afternoon_activity" ("date") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "afternoon_activity_camper_counselor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "camper_id" bigint NOT NULL REFERENCES "afternoon_activity_camper" ("id") DEFERRABLE INITIALLY DEFERRED, "counselor_id" bigint NOT NULL REFERENCES "afternoon_activity_counselor" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field camper to cabin
--
CREATE TABLE "new__afternoon_activity_cabin" ("cabin_number" integer NOT NULL PRIMARY KEY, "camper_id" bigint NOT NULL REFERENCES "afternoon_activity_camper" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__afternoon_activity_cabin" ("cabin_number", "camper_id") SELECT "cabin_number", NULL FROM "afternoon_activity_cabin";
DROP TABLE "afternoon_activity_cabin";
ALTER TABLE "new__afternoon_activity_cabin" RENAME TO "afternoon_activity_cabin";
CREATE INDEX "afternoon_activity_afternoon_activity_activity_id_61f9396c" ON "afternoon_activity_afternoon_activity" ("activity_id");
CREATE INDEX "afternoon_activity_counselor_possition_id_b3d3e37b" ON "afternoon_activity_counselor" ("possition_id");
CREATE INDEX "afternoon_activity_camper_cabin_number_id_4a3dfc39" ON "afternoon_activity_camper" ("cabin_number_id");
CREATE UNIQUE INDEX "afternoon_activity_camper_afternoon_activity_camper_id_afternoon_activity_id_558602d9_uniq" ON "afternoon_activity_camper_afternoon_activity" ("camper_id", "afternoon_activity_id");
CREATE INDEX "afternoon_activity_camper_afternoon_activity_camper_id_fc1c570d" ON "afternoon_activity_camper_afternoon_activity" ("camper_id");
CREATE INDEX "afternoon_activity_camper_afternoon_activity_afternoon_activity_id_22e5a043" ON "afternoon_activity_camper_afternoon_activity" ("afternoon_activity_id");
CREATE UNIQUE INDEX "afternoon_activity_camper_counselor_camper_id_counselor_id_f1a3f652_uniq" ON "afternoon_activity_camper_counselor" ("camper_id", "counselor_id");
CREATE INDEX "afternoon_activity_camper_counselor_camper_id_676962be" ON "afternoon_activity_camper_counselor" ("camper_id");
CREATE INDEX "afternoon_activity_camper_counselor_counselor_id_d12a2553" ON "afternoon_activity_camper_counselor" ("counselor_id");
CREATE INDEX "afternoon_activity_cabin_camper_id_35cacdfe" ON "afternoon_activity_cabin" ("camper_id");
--
-- Add field counselor to cabin
--
CREATE TABLE "new__afternoon_activity_cabin" ("cabin_number" integer NOT NULL PRIMARY KEY, "camper_id" bigint NOT NULL REFERENCES "afternoon_activity_camper" ("id") DEFERRABLE INITIALLY DEFERRED, "counselor_id" bigint NOT NULL REFERENCES "afternoon_activity_counselor" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__afternoon_activity_cabin" ("cabin_number", "camper_id", "counselor_id") SELECT "cabin_number", "camper_id", NULL FROM "afternoon_activity_cabin";
DROP TABLE "afternoon_activity_cabin";
ALTER TABLE "new__afternoon_activity_cabin" RENAME TO "afternoon_activity_cabin";
CREATE INDEX "afternoon_activity_cabin_camper_id_35cacdfe" ON "afternoon_activity_cabin" ("camper_id");
CREATE INDEX "afternoon_activity_cabin_counselor_id_8dae47d4" ON "afternoon_activity_cabin" ("counselor_id");
--
-- Add field activity_leader to afternoon_activity
--
CREATE TABLE "new__afternoon_activity_afternoon_activity" ("date" date NOT NULL PRIMARY KEY, "second_activity" bool NOT NULL, "activity_id" bigint NOT NULL REFERENCES "afternoon_activity_activity" ("id") DEFERRABLE INITIALLY DEFERRED, "activity_leader_id" bigint NOT NULL REFERENCES "afternoon_activity_counselor" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__afternoon_activity_afternoon_activity" ("date", "second_activity", "activity_id", "activity_leader_id") SELECT "date", "second_activity", "activity_id", NULL FROM "afternoon_activity_afternoon_activity";
DROP TABLE "afternoon_activity_afternoon_activity";
ALTER TABLE "new__afternoon_activity_afternoon_activity" RENAME TO "afternoon_activity_afternoon_activity";
CREATE INDEX "afternoon_activity_afternoon_activity_activity_id_61f9396c" ON "afternoon_activity_afternoon_activity" ("activity_id");
CREATE INDEX "afternoon_activity_afternoon_activity_activity_leader_id_6f90294c" ON "afternoon_activity_afternoon_activity" ("activity_leader_id");
--
-- Add field camper to afternoon_activity
--
CREATE TABLE "afternoon_activity_afternoon_activity_camper" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "afternoon_activity_id" date NOT NULL REFERENCES "afternoon_activity_afternoon_activity" ("date") DEFERRABLE INITIALLY DEFERRED, "camper_id" bigint NOT NULL REFERENCES "afternoon_activity_camper" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create constraint perference_in_range on model activity
--
CREATE TABLE "new__afternoon_activity_activity" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activity" varchar(20) NOT NULL, "perference" integer NOT NULL, CONSTRAINT "perference_in_range" CHECK (("perference" >= 0 AND "perference" <= 3)));
INSERT INTO "new__afternoon_activity_activity" ("id", "activity", "perference") SELECT "id", "activity", "perference" FROM "afternoon_activity_activity";
DROP TABLE "afternoon_activity_activity";
ALTER TABLE "new__afternoon_activity_activity" RENAME TO "afternoon_activity_activity";
CREATE UNIQUE INDEX "afternoon_activity_afternoon_activity_camper_afternoon_activity_id_camper_id_9fb9d220_uniq" ON "afternoon_activity_afternoon_activity_camper" ("afternoon_activity_id", "camper_id");
CREATE INDEX "afternoon_activity_afternoon_activity_camper_afternoon_activity_id_8ebba333" ON "afternoon_activity_afternoon_activity_camper" ("afternoon_activity_id");
CREATE INDEX "afternoon_activity_afternoon_activity_camper_camper_id_7c6464e5" ON "afternoon_activity_afternoon_activity_camper" ("camper_id");
COMMIT;