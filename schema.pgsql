BEGIN;

CREATE TABLE "users" (
	"user_id" integer,
	"reg_timestamp" TIMESTAMP,
	"address" TEXT,
	"thumbnail" TEXT,
	"username" TEXT,
	"email" TEXT,
	"password" TEXT,
	"gender" BOOLEAN,
	"yob" integer,
	"zip_code" TEXT,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
) WITH (
  OIDS=FALSE
);


CREATE TABLE "bills" (
	"bill_id" integer,
	"session" TEXT,
	"year_start" TIMESTAMP,
	"year_end" TIMESTAMP,
	"official_id" TEXT,
	"title" TEXT,
	"scope_id" integer,
	"state" varchar,
	"city_id" integer,
	"desc" TEXT,
	"tags" TEXT,
	CONSTRAINT bills_pk PRIMARY KEY (bill_id)
) WITH (
  OIDS=FALSE
);





CREATE TABLE "user_bills" (
	"user_bill_id" integer,
	"user_id" integer,
	"bill_id" integer,
	"following_since" timestamp,
	"desired_vote" BOOLEAN,
	CONSTRAINT user_bills_pk PRIMARY KEY (user_bill_id)
) WITH (
  OIDS=FALSE
);


CREATE TABLE "scopes" (
	"scope_id" integer,
	"scope" TEXT,
	CONSTRAINT scopes_pk PRIMARY KEY (scope_id)
) WITH (
  OIDS=FALSE
);




CREATE TABLE "bill_log" (
	"bill_log_id" bigserial,
	"bill_id" integer,
	"status_date" TIMESTAMP,
	"status" integer,
	"last_action_date" TIMESTAMP,
	"last_action" text,
	CONSTRAINT bill_log_pk PRIMARY KEY (bill_log_id,bill_id)
) WITH (
  OIDS=FALSE
);



CREATE TABLE "bill_stati" (
	"status_id" integer,
	"status" TEXT,
	CONSTRAINT bill_stati_pk PRIMARY KEY (status_id)
) WITH (
  OIDS=FALSE
);




CREATE TABLE "legislators" (
	"legislator_id" integer,
	"scope_id" integer,
	"given_names" TEXT,
	"surname" TEXT,
	"state_id" integer,
	"city_id" integer,
	"email" TEXT,
	"phone" TEXT,
	"address" TEXT,
	"thumbnail" TEXT,
	"website" TEXT,
	"fax" TEXT,
	CONSTRAINT legislators_pk PRIMARY KEY (legislator_id)
) WITH (
  OIDS=FALSE
);


CREATE TABLE "states" (
	"state_id" integer,
	"state" TEXT,
	CONSTRAINT states_pk PRIMARY KEY (state_id)
) WITH (
  OIDS=FALSE
);




CREATE TABLE "cities" (
	"city_id" integer,
	"city" TEXT,
	CONSTRAINT cities_pk PRIMARY KEY (city_id)
) WITH (
  OIDS=FALSE
);




CREATE TABLE "bill_legislators" (
	"bill_legislator_id" integer,
	"bill_id" integer,
	"legislator_id" integer,
	CONSTRAINT bill_legislators_pk PRIMARY KEY (bill_legislator_id)
) WITH (
  OIDS=FALSE
);

CREATE TABLE "translations" (
	"translation_id" integer,
	"bill_id" integer,
	"user_id" integer,
	"translation" TEXT,
	"likes" integer DEFAULT '0',
	"dislikes" integer DEFAULT '0',
	"created_timestamp" TIMESTAMP,
	CONSTRAINT translations_pk PRIMARY KEY (translation_id)
) WITH (
  OIDS=FALSE
);


CREATE TABLE "legislator_votes" (
	"legislator_vote_id" integer,
	"legislator_id" integer,
	"bill_id" integer,
	"vote" BOOLEAN,
	CONSTRAINT legislator_votes_pk PRIMARY KEY (legislator_vote_id)
) WITH (
  OIDS=FALSE
);



ALTER TABLE "legislator_votes" ADD CONSTRAINT legislator_votes_fk0 FOREIGN KEY (legislator_id) REFERENCES legislators(legislator_id);
ALTER TABLE "legislator_votes" ADD CONSTRAINT legislator_votes_fk1 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE "translations" ADD CONSTRAINT translations_fk0 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE "translations" ADD CONSTRAINT translations_fk1 FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE "bill_legislators" ADD CONSTRAINT bill_legislators_fk0 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE "bill_legislators" ADD CONSTRAINT bill_legislators_fk1 FOREIGN KEY (legislator_id) REFERENCES legislators(legislator_id);
ALTER TABLE "legislators" ADD CONSTRAINT legislators_fk0 FOREIGN KEY (scope_id) REFERENCES scopes(scope_id);
ALTER TABLE "legislators" ADD CONSTRAINT legislators_fk1 FOREIGN KEY (state_id) REFERENCES states(state_id);
ALTER TABLE "legislators" ADD CONSTRAINT legislators_fk2 FOREIGN KEY (city_id) REFERENCES cities(city_id);
ALTER TABLE "bill_log" ADD CONSTRAINT bill_log_fk0 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
--ALTER TABLE "bill_log" ADD CONSTRAINT bill_log_fk1 FOREIGN KEY (status) REFERENCES bill_stati(status_id);
ALTER TABLE "user_bills" ADD CONSTRAINT user_bills_fk0 FOREIGN KEY (user_id) REFERENCES users(user_id);
ALTER TABLE "user_bills" ADD CONSTRAINT user_bills_fk1 FOREIGN KEY (bill_id) REFERENCES bills(bill_id);
ALTER TABLE "bills" ADD CONSTRAINT bills_fk0 FOREIGN KEY (scope_id) REFERENCES scopes(scope_id);
--ALTER TABLE "bills" ADD CONSTRAINT bills_fk1 FOREIGN KEY (state_id) REFERENCES states(state_id);
ALTER TABLE "bills" ADD CONSTRAINT bills_fk2 FOREIGN KEY (city_id) REFERENCES cities(city_id);

COMMIT;
