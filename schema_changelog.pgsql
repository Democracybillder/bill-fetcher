ALTER TABLE bills ADD COLUMN  year_start TIMESTAMP;
ALTER TABLE bills ADD COLUMN  year_end TIMESTAMP;

ALTER TABLE bills DROP COLUMN  year_start TIMESTAMP;
ALTER TABLE bills DROP COLUMN  year_end TIMESTAMP;

CREATE TABLE "sessions" (
	"session_id"	BIGSERIAL,
	"session"	TEXT,
	"year_start" SMALLINT,
	"year_end" SMALLINT,
	CONSTRAINT sessions_pk PRIMARY KEY (session_id)
	);

ALTER TABLE bills ADD COLUMN session_id BIGINT;

INSERT INTO sessions(session)
SELECT DISTINCT session
FROM bills;

UPDATE bills b SET b.session_id = s.session_id
FROM session s
WHERE s.session = b.session;

ALTER TABLE bills ADD CONSTRAINT bill_sessions_fk FOREIGN KEY (session_id) REFERENCES sessions(session_id);

ALTER TABLE bills DROP COLUMN session;

ALTER TABLE bills RENAME COLUMN "desc" to descr;



